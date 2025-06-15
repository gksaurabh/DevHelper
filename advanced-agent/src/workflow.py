from typing import List, Dict, Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


from .models import ResearchState, CompanyInfo, CompanyAnalysis
from .firecrawl import FirecrawlService
from .prompts import DeveloperToolsPrompts


# This is the main workflow class that orchestrates the research process
class Workflow:
    def __init__(self):
        self.firecrawl = FirecrawlService()
        self.llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
        self.prompts = DeveloperToolsPrompts()
        self.workflow = self._build_workflow()

    # This method builds the workflow graph for the langFlow
    def _build_workflow(self):
        #initialize the state graph
        graph = StateGraph(ResearchState)
        
        # add the nodes to the graph
        graph.add_node("extract_tools", self._extract_tools_step)
        graph.add_node("research", self._research_step)
        graph.add_node("analyze", self._analyze_step)

        # set the entry point and start node
        graph.set_entry_point("extract_tools")
        
        # define the edges between the nodes/path
        graph.add_edge("extract_tools", "research")
        graph.add_edge("research", "analyze")
        graph.add_edge("analyze", END)

        
        return graph.compile()


    # This method defines the tool extraction step of the workflow
    def _extract_tools_step(self, state: ResearchState) -> Dict[str, Any]:
        print(f"Finding articles related to: {state.query}")

        # Search for articles related to the query and 
        article_query = f"{state.query} tools comparison best alternatives"
        search_results = self.firecrawl.search_companies(article_query, num_results=5)

        all_content = ""

        # Scrape the content of each article found in the search results
        for result in search_results.data:
            url = result.get("url", "")
            scraped = self.firecrawl.scrape_company_pages(url)
            if scraped:
                all_content + scraped.markdown[:2000] + "\n\n"

        messages = [
            SystemMessage(content=self.prompts.TOOL_EXTRACTION_SYSTEM),
            HumanMessage(content=self.prompts.tool_extraction_user(state.query, all_content))
        ]

        # Call the LLM to extract tools
        try:
            response = self.llm.invoke(messages)
            tools_names = [
                name.strip()
                for name in response.content.splitlines() if name.strip("\n")
                if name.strip()
            ]
            print(f"Extracted tools: {','.join(tools_names[:5])}")
            return {"extracted_tools": tools_names[:5]}
        
        except Exception as e:
            print(f"Error extracting tools: {e}")
            return {"extracted_tools": []}
        
    # This method analyzes the content of each company page using the LLM and returns a structured analysis    
    def _analyze_company_content(self, company_name: str, content: str) -> CompanyAnalysis:
        structured_llm = self.llm.with_structured_output(CompanyAnalysis)

        messages = [
            SystemMessage(content=self.prompts.TOOL_ANALYSIS_SYSTEM),
            HumanMessage(content=self.prompts.tool_analysis_user(company_name, content))
        ]

        try:
            analysis = structured_llm.invoke(messages)
            return analysis
        except Exception as e:
            print(f"Error analyzing company content for {company_name}: {e}")
            return CompanyAnalysis(
                pricing_model="Unknown",
                is_open_source=None,
                tech_stack=[],
                description="",
                api_available=None,
                language_support=[],
                integration_capabilities=[]
            )
    
    def _research_step(self, state: ResearchState) -> ResearchState:

        # extract all the tools from the state
        extracted_tools = getattr(state, "extracted_tools", []) # look in the state for extracted tool attribute, if we have it give it, if not return empty list

        # if we don't have any extracted tools, then fall direct search
        if not extracted_tools:
            print("No tools extracted, falling back to direct search...")
            search_results = self.firecrawl.search_companies(state.query, num_results=5)
            tool_names = [
                result.get("metadata", {}).get("title", "Unkown")
                for result in search_results.data
            ]

        # if we have extracted tools, then use them
        else:
            tool_names = extracted_tools[:5]
        
        print(f"Researching companies for tools: {', '.join(tool_names)}")

        # Search for companies related to the extracted tools
        companies = []

        # Iterate over each tool name and search for its official website
            # for every tool, look up the tool and its official website
        for tool in tool_names:
            tool_search_results = self.firecrawl.search_companies(tool + 'official website', num_results=1)

            if tool_search_results:
                result = tool_search_results.data[0]
                url = result.get("url", "")

                # set up the company info object with the tool name, description, website, and empty tech stack and competitors

                company = CompanyInfo(
                    name = tool,
                    description=result.get("markdown", ""),
                    website=url,
                    tech_stack=[],
                    competitors=[]
                )

                # Scrape the company page for more details
                scraped_content = self.firecrawl.scrape_company_pages(url)

                if scraped_content:
                    content = scraped_content.markdown
                    analysis = self._analyze_company_content(tool, content) # scrape the content using our llm.

                    # Update the company info with the analysis results
                    company.pricing_model = analysis.pricing_model
                    company.is_open_source = analysis.is_open_source
                    company.tech_stack = analysis.tech_stack
                    company.description = analysis.description
                    company.api_available = analysis.api_available
                    company.language_support = analysis.language_support
                    company.integration_capabilities = analysis.integration_capabilities
                    
                companies.append(company)

        return {"companies": companies}
        
    # This method generates recommendations based on the research findings and the user's query    
    def _analyze_step(self, state: ResearchState) -> Dict[str, Any]:
        print("Generating Recommendations...")

        company_data = ", ".join([
            company.json() for company in state.companies
        ])

        messages = [
            SystemMessage(content=self.prompts.RECOMMENDATIONS_SYSTEM),
            HumanMessage(content=self.prompts.recommendations_user(state.query, company_data))
        ]

        response = self.llm.invoke(messages)
        return {"analysis": response.content}

    # This method runs the entire workflow with the given query and returns the final state
    def run(self, query: str) -> ResearchState:
        initial_state = ResearchState(query=query)
        final_state = self.workflow.invoke(initial_state)

        return ResearchState(**final_state)