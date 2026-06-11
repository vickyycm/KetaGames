from servicios.auth_servicio import actualizar_estadisticas_usuario
from datetime import datetime
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
import random

def obtener_palabra_de_tematica(tematica: str) -> dict:
    tematica_id = tematica.lower().strip()
    ref_tematica = db.collection("tematicas_palabras").document(tematica_id)
    doc = ref_tematica.get()

    palabras_disponibles = []
    pistas = {}

    if doc.exists:
        data = doc.to_dict()
        palabras_disponibles = data.get("palabras", [])
        pistas = data.get("pistas", {})

    if not palabras_disponibles:
        resultado_ia_batch = {
            "palabras": ["GATOS", "PERRO", "CASAS", "ARBOL", "PLAZA"],
            "pistas": {
                "GATOS": "Animal doméstico muy popular",
                "PERRO": "El mejor amigo del hombre",
                "CASAS": "Lugar donde viven las familias",
                "ARBOL": "Planta grande con tronco leñoso",
                "PLAZA": "Espacio público con juegos y pasto"
            }
        }
        palabras_disponibles = resultado_ia_batch["palabras"]
        pistas = resultado_ia_batch["pistas"]

    palabra_elegida = random.choice(palabras_disponibles)
    pista_elegida = pistas.get(palabra_elegida, "Sin pista disponible")

    palabras_disponibles.remove(palabra_elegida)
    ref_tematica.set({
        "nombre_original": tematica,
        "palabras": palabras_disponibles,
        "pistas": pistas
    }, merge=True)

    return {"palabra": palabra_elegida, "pista": pista_elegida}


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