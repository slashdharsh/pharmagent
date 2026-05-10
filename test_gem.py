from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

# Print the key (first 10 chars only) so we can confirm it's loading
api_key = os.getenv("GEMINI_API_KEY")
print(f"Key loaded: {api_key[:10]}..." if api_key else "ERROR: No API key found in .env")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3-flash-live",
    contents="What is Keytruda used for in pharma marketing? Give me 3 bullet points."
)

print(response.text)