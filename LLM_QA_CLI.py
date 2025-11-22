from groq import Groq
import re
import os
from dotenv import load_dotenv
# Load .env file
load_dotenv()
# Read API key from environment
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text
while True:
    question = input("\nAsk a question (or type 'quit'): ")
    if question.lower() == "quit":
        break
    processed = preprocess(question)
    print("\nProcessed Question:", processed)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[{"role": "user", "content": processed}]
    )
    print("\nAnswer:", response.choices[0].message["content"])