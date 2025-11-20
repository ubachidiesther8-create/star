from flask import Flask, request, render_template
import requests 
app = Flask(__name__)
# Groq API details
API_URL = "https://api.groq.com/openai/v1/chat/completions"
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GROQ_API_KEY")
def query(question):
    url = API_URL

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
    response = requests.post(url, headers=headers, json=payload)

    print("STATUS:", response.status_code)
    print("RESPONSE:", response.text)

    return response.json()
@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""
    if request.method == "POST":
        question = request.form["question"]
        output = query(question)

        try:
            answer = output["choices"][0]["message"]["content"]
        except Exception as e:
            print("ERROR:", e)
            answer = "Sorry, I couldn't generate a response."

    return render_template("index.html", answer=answer, question=question)
if __name__ == '__main__':
    app.run(debug=True)