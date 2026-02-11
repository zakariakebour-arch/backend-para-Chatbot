from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://zakariakebour-arch.github.io"}})
sistema_prompt = os.getenv("prompt_forzado")
OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    messages = data.get("messages", [])

    prompt_forzado = {
        "role": "system",
        "content": sistema_prompt
    }

    mensaje_entero = [prompt_forzado] + messages

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENROUTER_KEY}",
                "HTTP-Referer": "https://zakariakebour-arch.github.io/Portafolio/",
                "X-Title": "Chat de Zakaria"
            },
            json={
                "model": "openrouter/free",
                "messages": mensaje_entero
            }
        )

        r = response.json()
        if "choices" in r:
            asistente_mensaje = r["choices"][0]["message"]["content"]
        else:
            asistente_mensaje = f"Error del modelo: {r}"

        return jsonify({"response": asistente_mensaje})

    except Exception as e:
        return jsonify({"response": f"Error en el servidor: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
