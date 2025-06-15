import os
from firecrawl import FirecrawlApp, ScrapeOptions
from dotenv import load_dotenv

load_dotenv()

# this is a simple service to interact with Firecrawl API
class FirecrawlService:
    def __init__(self):
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is not set")
        self.app = FirecrawlApp(api_key=api_key)

    # specific method to search for companies related to developer tools and pricing with specific markdown format
    # this method will return a list of companies with their pricing information
    def search_companies(self, query: str, num_results: int = 5):
        try:
            result = self.app.search(
                query=f"{query} company pricing",
                limit=num_results,
                scrape_options=ScrapeOptions(
                    formats=["markdown"]
                )
            )
            return result
        
        except Exception as e:
            print(f"Error during search: {e}")
            return []

    # specific method to scrape company pages and return their content in markdown format
    # this method will take a URL and return the scraped content    
    def scrape_company_pages(self, url: str):
        try:
            result = self.app.scrape_url(
                url,
                formats=["markdown"],
            )
            return result
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None