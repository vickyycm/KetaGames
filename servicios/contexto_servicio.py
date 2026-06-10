import json
import os
import google.generativeai as genai
from config import Config

genai.configure(api_key=Config.GEMINI_API_KEY)
_modelo_gemini = genai.GenerativeModel("gemini-2.0-flash")

_ruta_diccionario = os.path.join(os.path.dirname(__file__), "..", "diccionario_es.json")
with open(_ruta_diccionario, encoding="utf-8") as f:
    _diccionario: set = set(w.lower() for w in json.load(f))


def validar_palabra(palabra: str) -> bool:
    palabra = palabra.lower().strip()
    if len(palabra) < 4:
        return False
    if not palabra.isalpha():
        return False
    return palabra in _diccionario


def calcular_similitud(palabra_secreta: str, intento: str) -> int:
    prompt = f"""Sos un motor de asociación semántica para un juego de palabras en español.
    Dado un par de palabras, devolvés un número del 1 al 100 indicando qué tan relacionadas están.

    Escala:
    1-5   = misma palabra o sinónimo exacto ("auto" y "coche")
    6-15  = muy relacionadas, mismo campo directo ("bomba" y "explosion", "espada" y "guerrero", "espiral" y "laberinto", "rueda" y "bicicleta")
    16-35 = relacionadas indirectamente ("fuego" y "explosion", "miedo" y "fantasma", "selva" y "animal")
    36-60 = relación lejana o por contexto ("bosque" y "explosion", "casa" y "laberinto")
    61-85 = poca relación ("agua" y "explosion")
    86-100 = sin relación ("amor" y "explosion", "planta" y "laberinto")

    Usá siempre el significado más común y cotidiano de cada palabra, evitá asociaciones por doble sentido o acepciones poco comunes.

    Par a evaluar: "{intento}" y "{palabra_secreta}"

    Respondé SOLO con el número entero, sin texto extra."""

    respuesta = _modelo_gemini.generate_content(prompt)
    score = int(respuesta.text.strip())
    return max(1, min(100, score))