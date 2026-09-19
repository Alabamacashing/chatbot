# 🤖 AI Chatbot

A conversational AI assistant powered by Llama3.2 running locally via Ollama.

## How it works
- Type any question or task
- Llama3.2 generates a response locally
- Full conversation history maintained

## Tech Stack
- Python, Flask
- Ollama, Llama3.2:1b
- No API keys needed — runs 100% offline!

## Run locally
1. Install Ollama from https://ollama.com
2. Pull the model: `ollama pull llama3.2:1b`
3. Install dependencies: `pip install flask requests`
4. Run: `python app.py`
