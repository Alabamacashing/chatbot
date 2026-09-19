from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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
        response = requests.post("http://localhost:11434/api/chat", json={
            "model": "llama3.2:1b",
            "messages": conversation_history,
            "stream": False
        })

        result = response.json()
        assistant_message = result["message"]["content"]

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