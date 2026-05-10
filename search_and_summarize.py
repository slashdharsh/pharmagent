from dotenv import load_dotenv
import os
from groq import Groq
from tavily import TavilyClient

# Load keys
load_dotenv()

# Set up both clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


def search_drug(drug_name):
    """Step 1: Search the web for info about the drug"""
    print(f"\n Searching for: {drug_name}...")

    results = tavily.search(
        query=f"{drug_name} pharma marketing competitor analysis 2024",
        max_results=5,
        search_depth="advanced"
    )

    # Combine all search results into one block of text
    combined_text = ""
    for result in results["results"]:
        combined_text += f"Source: {result['title']}\n"
        combined_text += f"Content: {result['content']}\n\n"

    print(f" Found {len(results['results'])} sources.")
    return combined_text


def summarize_with_groq(drug_name, search_text):
    """Step 2: Send search results to Groq and ask for a marketing summary"""
    print(f"\n Analyzing with Groq AI...")

    prompt = f"""
You are a pharma marketing analyst. Below are recent search results about the drug: {drug_name}

Search Results:
{search_text}

Based ONLY on the information above, provide a structured summary with these sections:

1. WHAT IT IS: What is {drug_name}? What condition does it treat?
2. WHO MAKES IT: Which company manufactures it?
3. KEY COMPETITORS: What are the main competing drugs in this space?
4. TARGET AUDIENCE: Is this drug marketed to doctors (HCP), patients, or both?
5. MARKETING ANGLE: What is the main benefit or message being used to market this drug?

Be concise. Use bullet points. If you don't find info for a section, write "Not found in search results."
"""

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a professional pharma marketing analyst. Always be concise and structured."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3  # Lower = more factual, less creative
    )

    return response.choices[0].message.content


def run_phase2(drug_name):
    """Run the full Phase 2 pipeline: search → summarize"""
    print(f"\n{'='*50}")
    print(f" PHARMAGENT — PHASE 2 TEST")
    print(f" Drug: {drug_name}")
    print(f"{'='*50}")

    # Step 1: Search
    search_results = search_drug(drug_name)

    # Step 2: Summarize
    summary = summarize_with_groq(drug_name, search_results)

    # Step 3: Print output
    print(f"\n{'='*50}")
    print(f" SUMMARY FOR: {drug_name.upper()}")
    print(f"{'='*50}")
    print(summary)
    print(f"\n{'='*50}")
    print(" Phase 2 complete!")


# Run it — change the drug name to test others
run_phase2("Ozempic")