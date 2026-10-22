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

    conversation_history.append({
        "role": "user",
        "content": user_message
    })

    try:
        response = requests.post(GROQ_API_URL,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "compound-beta-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    *conversation_history
                ],
                "max_tokens": 1024
            }
        )

        result = response.json()
       print("STATUS:", response.status_code)
       print("FULL RESPONSE:", result)
       assistant_message = result["choices"][0]["message"]["content"]

        conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })

        return jsonify({"response": assistant_message})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "cleared"})

if __name__ == "__main__":
    app.run(debug=True)
