from servicios.auth_servicio import actualizar_estadisticas_usuario
from datetime import datetime
import json
import os
import random
from db.firebase import db
from servicios.ia_servicio import generar_palabras_wordle
from servicios.wordle_servicio import (
    evaluar_intento,
    intento_valido,
    es_ganador,
    calcular_puntaje,
    MAX_INTENTOS
)
from modelos.juegos.wordle import SesionWordle

DICCIONARIO_PALABRAS = set()

try:
    ruta_diccionario = os.path.join(os.path.dirname(__file__), '../../diccionario_es.json')
    ruta_diccionario = os.path.abspath(ruta_diccionario)
    
    if os.path.exists(ruta_diccionario):
        with open(ruta_diccionario, 'r', encoding='utf-8') as f:
            palabras_json = json.load(f)
            DICCIONARIO_PALABRAS = {p.upper().strip() for p in palabras_json}
except Exception as e:
    print(f"Error al cargar el diccionario de palabras: {str(e)}")

def obtener_palabra_de_tematica(tematica: str) -> dict:

    tematica = tematica.lower().strip()

    paises = {
        "CHINA": "País más poblado del mundo",
        "JAPON": "País asiático famoso por el sushi",
        "ITALI": "País europeo con forma de bota",
        "INDIA": "Segundo país más poblado del mundo",
        "CHILE": "País largo y angosto de Sudamérica"
    }

    animales = {
        "ABEJA": "Insecto productor de miel",
        "PERRO": "El mejor amigo del hombre",
        "TIGRE": "Felino salvaje de rayas",
        "CEBRA": "Animal africano con rayas",
        "PANDA": "Animal blanco y negro de China"
    }

    if tematica == "animales":
        palabras = animales
    else:
        palabras = paises

    palabra_elegida = random.choice(list(palabras.keys()))

    return {
        "palabra": palabra_elegida,
        "pista": palabras[palabra_elegida]
    }


def iniciar_partida(id_usuario: str, tematica: str) -> dict:
    resultado_palabra = obtener_palabra_de_tematica(tematica)
    id_sesion = f"{id_usuario}_{int(datetime.utcnow().timestamp())}"

    sesion_objeto = SesionWordle(
        id_usuario=id_usuario,
        tematica=tematica,
        palabra=resultado_palabra["palabra"],
        pista=resultado_palabra["pista"]
    )

    db.collection("partidas_wordle").document(id_sesion).set(sesion_objeto.to_dict())

    return {
        "id_sesion": id_sesion,
        "pista": sesion_objeto.pista,
        "tematica": tematica,
        "max_intentos": MAX_INTENTOS,
        "largo_palabra": 5
    }


def enviar_intento(id_sesion: str, intento: str) -> dict:
    ref_doc = db.collection("partidas_wordle").document(id_sesion)
    doc = ref_doc.get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionWordle.from_dict(doc.to_dict())

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    intento = intento.upper().strip()

    if not intento_valido(intento):
        return {"error": "El intento debe tener exactamente 5 letras"}
    
    if DICCIONARIO_PALABRAS and (intento not in DICCIONARIO_PALABRAS):
        return {"error": f"La palabra '{intento}' no es válida en el diccionario"}


    evaluacion = evaluar_intento(sesion.palabra, intento)
    gano = es_ganador(evaluacion)

    sesion.intentos.append({"intento": intento, "resultado": evaluacion})
    intentos_usados = len(sesion.intentos)

    if gano:
        sesion.estado = "ganada"
        sesion.finalizada_en = datetime.utcnow().isoformat()
    elif intentos_usados >= MAX_INTENTOS:
        sesion.estado = "perdida"
        sesion.finalizada_en = datetime.utcnow().isoformat()

    puntaje = (
        calcular_puntaje(intentos_usados, gano)
        if sesion.estado != "jugando"
        else 0
    )
    sesion.puntaje = puntaje

    if sesion.estado != "jugando" and sesion.id_usuario != "invitado":
        actualizar_estadisticas_usuario(
            sesion.id_usuario,
            "wordle",
            puntaje,
            gano=gano
        )

    ref_doc.update(sesion.to_dict())

    respuesta = {
        "evaluacion": evaluacion, 
        "intentos_usados": intentos_usados,
        "max_intentos": MAX_INTENTOS,
        "estado": sesion.estado,
        "puntaje": puntaje
    }

    if sesion.estado == "perdida":
        respuesta["palabra"] = sesion.palabra

    return respuesta


def obtener_sesion(id_sesion: str) -> dict:
    doc = db.collection("partidas_wordle").document(id_sesion).get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionWordle.from_dict(doc.to_dict())

    data = {
        "id_sesion": id_sesion,
        "id_usuario": sesion.id_usuario,
        "tematica": sesion.tematica,
        "pista": sesion.pista,
        "intentos": sesion.intentos,
        "estado": sesion.estado,
        "puntaje": sesion.puntaje,
        "max_intentos": MAX_INTENTOS,
        "largo_palabra": 5
    }

    if sesion.estado != "jugando":
        data["palabra"] = sesion.palabra

    return data