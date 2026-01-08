from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set GROQ_API_KEY in .env file")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

def generate_code_via_groq(prompt):
 
    body = {
        "model": "openai/gpt-oss-20b",
        "messages": [
            {"role": "system", "content": "You are an expert code generator. Return only complete code not return only some lines, send complete code, if codes going 100+ lines then go for it , runnable code in all languages like html CSS, javascript, python, c++, java. Do not add explanations or comments. Make sure the code is fully functional and imports everything it needs."
},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 500,
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_URL, headers=HEADERS, data=json.dumps(body), timeout=60)
        if response.status_code == 200:
            data = response.json()
           
            return data["choices"][0]["message"]["content"].strip()
        else:
            return f"Error {response.status_code} - {response.text}"
    except Exception as e:
        return f"Exception: {str(e)}"

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json
    desc = data.get("description", "").strip()
    lang = data.get("language", "Python")

    if not desc:
        return jsonify({"code": "Error: Description is required."})

    prompt = f"Write {lang} code for: {desc}"
    result = generate_code_via_groq(prompt)
    return jsonify({"code": result})

if __name__ == "__main__":
    app.run(debug=True)
