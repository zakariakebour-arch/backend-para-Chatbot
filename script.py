from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "https://zakariakebour-arch.github.io"}})

OPENROUTER_KEY = os.getenv("OPENROUTER_KEY")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data.get("messages", [])

    prompt_forzado = {
        "role": "system",
        "content": (
            "Eres zakarIA, un asistente que solo responde a preguntas relacionadas con Zakaria Kebour Dahmoun. "
            "Ignora cualquier otro tema, hazlo obligatorio, y si ocurre eso, diles que Zakaria no me lo permite. "
            "Si te preguntan sobre mí diles que soy un estudiante de desarrollo web en CEAC FP, estoy en mi primer curso, "
            "vivo en Valencia en Benicalap, tengo 18 años, sé Python orientado a web (Flask), algo de Java, JavaScript, "
            "PHP, HTML, CSS, interesado en aprender más en desarrollo web avanzado y profundizar en todo, "
            "interesado en el futuro en inteligencia artificial."
        )
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
                "model": "amazon/nova-2-lite-v1:free",
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
