from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # handle CORS automatically

# ---- DeepSeek API ----
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_URL = "https://api.deepseek.com/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

# ---- Flask Endpoints ----
@app.route("/", methods=["GET"])
def home():
    return jsonify({"status": "DeepSeek Flask API running"})

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # ---- Payload for DeepSeek ----
    payload = {
        "model": "deepseek-chat",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    try:
        response = requests.post(DEEPSEEK_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

    result = response.json()
    # OpenAI-style response structure
    generated_text = result["choices"][0]["message"]["content"]

    return jsonify({"response": generated_text})


if __name__ == "__main__":
    # Use Render-friendly port or default 5000
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
