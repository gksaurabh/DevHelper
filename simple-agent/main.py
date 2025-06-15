from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

# initalize our LLM model
model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")
)

#server params for our MCP server
server_params = StdioServerParameters(
    command="npx",
    env={
        "FIRECRAWL_API_KEY": os.getenv("FIRECRAWL_API_KEY"),
    },
    args={"firecrawl-mcp"}
)

async def main():
    # Connect to our MCP server, and create a session, load tools, and create an agent
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            agent = create_react_agent(model, tools)

            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that can scrape websites, crawl pages, and extract information using Firecrawl tool. Think step by step and use the appropriate tools to help the user."
                }
            ]

            print("Available tools:", *[tool.name for tool in tools])
            print("-" * 60)

            # Start the conversation loop 
            while True:
                user_input = input("\nYou: ")
                if user_input == "quit":
                    print("Exiting...TYFUMP!")
                    break

                messages.append({"role": "user", "content": user_input[:175000]})
                
                
                try:
                    agent_response = await agent.ainvoke({"messages": messages})
                    
                    ai_message = agent_response["messages"][-1].content
                    print("Agent:" ,ai_message)

                except Exception as e:
                    print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())