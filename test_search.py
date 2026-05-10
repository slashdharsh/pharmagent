from dotenv import load_dotenv
import os
from tavily import TavilyClient

# Load your API keys
load_dotenv()

# Connect to Tavily
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

# Search for a drug
drug_name = "Jardiance competitor analysis"

results = tavily.search(
    query=drug_name,
    max_results=5,          # Get top 5 articles
    search_depth="advanced" # Deeper, more relevant results
)

# Print what we found
for i, result in enumerate(results["results"]):
    print(f"\n--- Result {i+1} ---")
    print(f"Title:   {result['title']}")
    print(f"URL:     {result['url']}")
    print(f"Content: {result['content'][:300]}...")  # First 300 characters