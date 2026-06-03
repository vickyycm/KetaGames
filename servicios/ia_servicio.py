import google.generativeai as genai
import json
import os
import re

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

modelo = genai.GenerativeModel("gemini-2.0-flash")

# wordle prompt
def generar_palabras_wordle(tematica: str) -> dict:
    prompt = f"""
Eres un generador de palabras para un juego tipo Wordle en español.

El usuario eligió la temática: "{tematica}"

Tu tarea:
1. Generar exactamente 20 palabras en español de EXACTAMENTE 5 letras, relacionadas con esa temática.
2. Cada palabra debe ser un sustantivo común, sin tildes, sin la letra Ñ.
3. Para cada palabra incluir una pista breve que ayude a adivinarla sin revelarla.
4. Devolver SOLO un JSON con este formato exacto, sin explicaciones ni markdown:
{{"palabras": ["XXXXX", "XXXXX", ...], "pistas": {{"XXXXX": "pista", "XXXXX": "pista", ...}}}}

Ejemplo válido:
- Temática "Fútbol" → {{"palabras": ["BALON", "ARCO", "FALTA", "PENAL", "TIROS"], "pistas": {{"BALON": "Objeto esférico del juego", "ARCO": "Donde entra el gol", "FALTA": "Infracción al reglamento", "PENAL": "Tiro desde los doce pasos", "TIROS": "Disparos al arco"}}}}

Responde solo con el JSON.
"""

    respuesta = modelo.generate_content(prompt)
    raw = respuesta.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    data = json.loads(raw)
    palabras = [p.upper().strip() for p in data["palabras"]]
    pistas = {k.upper().strip(): v for k, v in data["pistas"].items()}

    palabras = [p for p in palabras if len(p) == 5 and p.isalpha()]

    if len(palabras) < 5:
        raise ValueError(f"La IA devolvió muy pocas palabras válidas: {len(palabras)}")

    return {"palabras": palabras, "pistas": pistas}



# contexto prompt
def generar_palabras_contexto(tematica: str) -> dict:
    prompt = f"""
Eres un generador de palabras para un juego de asociación semántica en español.

El usuario eligió la temática: "{tematica}"

Tu tarea:
1. Generar exactamente 20 palabras en español relacionadas con esa temática.
2. Cada palabra debe ser un sustantivo común, sin tildes, sin la letra Ñ, de mínimo 4 letras.
3. Las palabras deben tener distintos niveles de relación con la temática — algunas muy obvias, otras más indirectas.
4. Devolver SOLO un JSON con este formato exacto, sin explicaciones ni markdown:
{{"palabras": ["PALABRA1", "PALABRA2", ...]}}

Ejemplos válidos:
- Temática "Fútbol" → {{"palabras": ["GOLES", "BALON", "ARCO", "CANCHA", "ARBITRO", "FALTA", "PENAL", "TIRO", "PASE", "DEFENSA", "ATAQUE", "CENTRO", "BANCO", "HINCHA", "COPA", "LIGA", "CLUB", "ESTADIO", "TORNEO", "CAPITAN"]}}

Responde solo con el JSON.
"""

    respuesta = modelo.generate_content(prompt)
    raw = respuesta.text.strip()
    raw = re.sub(r"```json|```", "", raw).strip()

    data = json.loads(raw)
    palabras = [p.upper().strip() for p in data["palabras"]]
    palabras = [p for p in palabras if len(p) >= 4 and p.isalpha()]

    if len(palabras) < 5:
        raise ValueError(f"La IA devolvió muy pocas palabras válidas: {len(palabras)}")

    return {"palabras": palabras}