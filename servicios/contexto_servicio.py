from sentence_transformers import SentenceTransformer, util
import json
import os


_modelo = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

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
    emb_secreta = _modelo.encode(palabra_secreta, convert_to_tensor=True)
    emb_intento = _modelo.encode(intento, convert_to_tensor=True)
    coseno = util.cos_sim(emb_secreta, emb_intento).item()

    score = round(1 + (1 - coseno) ** 0.7 * 99)
    return max(1, min(100, score))