from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

OPENROUTER_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "HTTP-Referer": "https://zakariakebour-arch.github.io/Portafolio/",
            "X-Title": "Chat de Zakaria"
        },
        json={
            "model": "deepseek/deepseek-chat:free",
            "messages": messages
        }
    )

    r = response.json()
    asistente_mensaje = r["choices"][0]["message"]["content"]

    return jsonify({"response": asistente_mensaje})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

