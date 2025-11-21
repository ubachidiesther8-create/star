from flask import Flask, request, render_template
import requests
import os
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()
API_URL = "https://api.groq.com/openai/v1/chat/completions"
API_KEY = os.getenv("GROQ_API_KEY")
def query(question):
    if not API_KEY:
        return {"error": "Missing GROQ_API_KEY in .env file"}
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": question}
        ]
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text)
    # Handle non-JSON responses safely
    try:
        return response.json()
    except:
        return {"error": "Invalid JSON returned from API", "raw": response.text}
@app.route("/", methods=["GET", "POST"])
def index():
    print("API KEY LOADED:", API_KEY)
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form["question"]
        output = query(question)
        # If API returned an error
        if "error" in output:
            answer = f"API Error: {output.get('error')} | Details: {output.get('raw', '')}"
        else:
            try:
                answer = output["choices"][0]["message"]["content"]
            except Exception as e:
                print("PARSING ERROR:", e)
                answer = "Sorry, I couldn't generate a response."
    return render_template("index.html", answer=answer, question=question)
if __name__ == '__main__':
    app.run(debug=True)
print("Loaded API Key:", API_KEY)
