from datetime import datetime

from servicios.ia_servicio import generar_palabra_por_tematica
from servicios.wordle_servicio import (
    evaluar_intento,
    intento_valido,
    es_ganador,
    calcular_puntaje,
    MAX_INTENTOS
)

# Almacenamiento temporal (reemplazar con db)
sesiones = {}

def iniciar_partida(id_usuario: str, tematica: str) -> dict:
    # Test sin tokens
    resultado_ia = {
        "palabra": "GATOS",
        "pista": "Animal doméstico muy popular"
    }
    # Con IA descomentar
    # try:
    #     resultado_ia = generar_palabra_por_tematica(tematica)
    # except Exception as e:
    #     return {"error": f"No se pudo generar la palabra: {str(e)}"}
    
    id_sesion = f"{id_usuario}_{int(datetime.utcnow().timestamp())}"
 
    sesiones[id_sesion] = {
        "id_usuario": id_usuario,
        "tematica": tematica,
        "palabra": resultado_ia["palabra"],
        "pista": resultado_ia["pista"],
        "intentos": [],
        "estado": "jugando",
        "puntaje": 0,
        "creada_en": datetime.utcnow().isoformat()
    }
 
    return {
        "id_sesion": id_sesion,
        "pista": resultado_ia["pista"],
        "tematica": tematica,
        "max_intentos": MAX_INTENTOS,
        "largo_palabra": 5
    }

def enviar_intento(id_sesion: str, intento: str) -> dict:

    sesion = sesiones.get(id_sesion)

    if not sesion:
        return {"error": "Sesión no encontrada"}

    if sesion["estado"] != "jugando":
        return {"error": "La partida ya terminó"}

    intento = intento.upper().strip()

    if not intento_valido(intento):
        return {"error": "El intento debe tener exactamente 5 letras"}

    evaluacion = evaluar_intento(sesion["palabra"], intento)
    gano = es_ganador(evaluacion)

    sesion["intentos"].append({"intento": intento, "resultado": evaluacion})
    intentos_usados = len(sesion["intentos"])

    if gano:
        sesion["estado"] = "ganada"
    elif intentos_usados >= MAX_INTENTOS:
        sesion["estado"] = "perdida"

    puntaje = calcular_puntaje(intentos_usados, gano) if sesion["estado"] != "jugando" else 0
    sesion["puntaje"] = puntaje

    respuesta = {
        "evaluacion": evaluacion,
        "intentos_usados": intentos_usados,
        "max_intentos": MAX_INTENTOS,
        "estado": sesion["estado"],
        "puntaje": puntaje
    }

    if sesion["estado"] == "perdida":
        respuesta["palabra"] = sesion["palabra"]

    return respuesta


def obtener_sesion(id_sesion: str) -> dict:

    sesion = sesiones.get(id_sesion)

    if not sesion:
        return {"error": "Sesión no encontrada"}

    data = {
        "id_sesion": id_sesion,
        "tematica": sesion["tematica"],
        "pista": sesion["pista"],
        "intentos": sesion["intentos"],
        "estado": sesion["estado"],
        "puntaje": sesion["puntaje"],
        "max_intentos": MAX_INTENTOS,
        "largo_palabra": 5
    }

    if sesion["estado"] != "jugando":
        data["palabra"] = sesion["palabra"]

    return data