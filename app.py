import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

HF_API_TOKEN = os.environ.get("HF_API_TOKEN")
MODEL_URL = "https://router.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

@app.route("/generate", methods=["POST"])
def generate():
    data = request.json or {}
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }

    response = requests.post(MODEL_URL, headers=HEADERS, json=payload)
    if response.status_code != 200:
        return jsonify({"error": response.text}), response.status_code

    result = response.json()
    return jsonify({"response": result[0]["generated_text"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
