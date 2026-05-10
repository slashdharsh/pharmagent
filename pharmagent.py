import os
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
import streamlit as st

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or st.secrets.get("GROQ_API_KEY", "")
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY") or st.secrets.get("TAVILY_API_KEY", "")
client = Groq(api_key=GROQ_API_KEY)
tavily = TavilyClient(api_key=TAVILY_API_KEY)


def ask_llm(prompt):
    """Send a prompt to Llama and get a response."""
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are a senior pharma marketing strategist with deep expertise in competitive analysis and brand positioning."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_tokens=1000
    )
    return response.choices[0].message.content


def search_drug_info(drug_name):
    """Search the web for competitive and market info about a drug."""
    print(f"\n🔍 Searching for info on: {drug_name}...")

    results = tavily.search(
        query=f"{drug_name} pharma competitive analysis market positioning 2024",
        search_depth="advanced",
        max_results=5
    )

    search_text = ""
    for i, result in enumerate(results['results'], 1):
        search_text += f"\nSource {i}: {result['title']}\n"
        search_text += f"{result['content']}\n"
        search_text += "-" * 40 + "\n"

    return search_text


def research_drug(drug_name):
    """Phase 2 pipeline: search → quick AI summary."""
    search_results = search_drug_info(drug_name)

    prompt = f"""
    You are a pharma marketing analyst. Based on the following real web search results 
    about {drug_name}, provide a concise 5-bullet summary covering:
    
    1. What the drug treats (indication)
    2. Who makes it and the brand positioning
    3. Key competitors in this space
    4. Target audience (doctors, patients, or both)
    5. One strategic marketing insight
    
    Keep it sharp and professional — like a briefing for a brand manager.
    
    SEARCH RESULTS:
    {search_results}
    """

    print(f"\n🤖 Analyzing {drug_name} data with AI...")
    summary = ask_llm(prompt)
    return summary, search_results  # returns BOTH so brief_writer can use the raw search data