from groq import Groq
from dotenv import load_dotenv
import os

# Load API keys
load_dotenv()

# Connect to Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Ask a question
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "What is Keytruda used for in pharma marketing?"}
    ]
)

# Print the answer
print(response.choices[0].message.content)