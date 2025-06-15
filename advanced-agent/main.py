from dotenv import load_dotenv
from src.workflow import Workflow

load_dotenv()

def main():
    # Initialize the workflow
    workflow = Workflow()

    print(f"Starting DevHelper : your AI-powered Developer Research Agent!")
    
    while True:
        query = input("\n Developer Query: ").strip()
        if query.lower() in ["exit", "quit"]:
            print("Exiting... Thank you for using DevHelper!")
            break
        if query:
            # Run the workflow with the user query
            result = workflow.run(query)
            print(f"Research Result for query: {query}")
            print("=" * 60)

            for i, company in enumerate(result.companies, start=1):
                print(f"{i}. {company.name} - {company.description}")
                print(f"   Website: {company.website}")
                print(f"   Pricing Model: {company.pricing_model}")
                print(f"   Open Source: {company.is_open_source }")
                print(f"   API Available: {company.api_available}")
                print(f"   Language Support: {', '.join(company.language_support)}")
                print(f"   Integration Capabilities: {', '.join(company.integration_capabilities)}")
                print("-" * 60)

if __name__ == "__main__":
    main()