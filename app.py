from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

conversation_history = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data["message"]

    if not user_message.strip():
        return jsonify({"error": "Please enter a message"})

    conversation_history.append({"role": "user", "content": user_message})

    response = requests.post(GROQ_API_URL,
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "llama3-8b-8192",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                *conversation_history
            ],
            "max_tokens": 1024
        }
    )

    result = response.json()
    assistant_message = result["choices"][0]["message"]["content"]

    conversation_history.append({"role": "assistant", "content": assistant_message})

    return jsonify({"response": assistant_message})

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
