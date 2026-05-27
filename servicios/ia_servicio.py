import google.generativeai as genai
import json
import os
import re

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

modelo = genai.GenerativeModel("gemini-2.0-flash")

# wordle prompt
def generar_palabra_por_tematica(tematica: str) -> dict:
    prompt = f"""
Eres un generador de palabras para un juego tipo Wordle en español.

El usuario eligió la temática: "{tematica}"

Tu tarea:
1. Elegir UNA palabra en español de EXACTAMENTE 5 letras, relacionada con esa temática.
2. La palabra debe ser un sustantivo o adjetivo común, sin tildes, sin la letra Ñ.
3. Devolver SOLO un JSON con este formato exacto, sin explicaciones ni markdown:
{{"palabra": "XXXXX", "pista": "Una pista breve sin revelar la palabra"}}

Ejemplos válidos:
- Temática "Ariana Grande" → {{"palabra": "ALBUM", "pista": "Producción musical de un artista"}}
- Temática "Fútbol" → {{"palabra": "BALON", "pista": "Donde termina el disparo del delantero"}}

Responde solo con el JSON.
"""

    respuesta = modelo.generate_content(prompt)
    raw = respuesta.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    data = json.loads(raw)
    palabra = data["palabra"].upper().strip()

    if len(palabra) != 5:
        raise ValueError(f"La IA devolvió una palabra con {len(palabra)} letras: {palabra}")

    return {
        "palabra": palabra,
        "pista": data.get("pista", "")
    }