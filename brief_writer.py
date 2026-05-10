import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def write_marketing_brief(drug_name, search_text):
    """
    Takes a drug name and raw search results.
    Returns a structured pharma marketing brief.
    """

    prompt = f"""
You are a senior pharma brand strategist with 15 years of experience at top consulting firms.
You have been given raw market research about the drug: {drug_name}

Your job is to turn this raw research into a professional competitive marketing brief
that a Brand Manager could use directly in a strategy meeting.

---
RAW RESEARCH:
{search_text}
---

Write the brief using EXACTLY this structure. Do not skip any section.
Use professional marketing language. Be specific — use drug names, company names,
percentages, and figures wherever the research supports it.

════════════════════════════════════════════════════════
COMPETITIVE MARKETING BRIEF: {drug_name.upper()}
════════════════════════════════════════════════════════

1. DRUG OVERVIEW
   - Generic name and drug class
   - Approved indication(s) — what condition(s) it treats
   - How it works (1 sentence, plain language)
   - FDA approval status

2. MANUFACTURER & COMMERCIAL POSITION
   - Which company makes it
   - Any revenue or market share signals found in the research
   - How long it has been on the market

3. COMPETITIVE LANDSCAPE
   Identify the top 2-3 competing drugs. For each competitor write:
   - Drug name + company
   - Key differentiator vs {drug_name}
   - Who it is winning with (doctors, patients, payers)

4. TARGET AUDIENCE STRATEGY
   - HCP MESSAGE: What are doctors being told? What clinical proof points are used?
   - PATIENT MESSAGE: What are patients being told? What emotional or lifestyle benefits are highlighted?
   - PAYER MESSAGE: Based on the drug class and search data available, what cost, 
     outcomes, or formulary arguments would payers likely respond to? If no direct 
     data was found, reason from the drug's clinical profile.

5. CORE MARKETING ANGLE
   Write 1-2 sentences summarizing the single most powerful message
   {drug_name} is using in the market right now. This is the "headline" of their strategy.

6. STRATEGIC OPPORTUNITY
   Based on what you found, identify ONE specific gap or weakness in {drug_name}'s
   current positioning that a competitor could exploit — or that {drug_name} should
   address. This is your strategic recommendation.

════════════════════════════════════════════════════════
CONFIDENCE NOTE: For any section where the research did not provide enough information,
write: [Insufficient data — recommend primary research]
════════════════════════════════════════════════════════
"""

    print("\n✍️  Writing your marketing brief...")

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # ← FIXED from llama3-70b-8192
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior pharma brand strategist. "
                    "You write precise, professional marketing briefs. "
                    "You never make up data. If research doesn't support a claim, you say so. "
                    "You always complete every section of the brief template."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=2000
    )

    return response.choices[0].message.content