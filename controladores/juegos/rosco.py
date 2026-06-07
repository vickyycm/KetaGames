from datetime import datetime

from modelos.juegos.rosco import SesionRosco
from servicios.rosco_servicio import (
    obtener_rosco_mock,
    verificar_respuesta,
    calcular_puntaje
)

sesiones = {}

def iniciar_partida(id_usuario: str, tematica: str) -> dict:
    preguntas = obtener_rosco_mock()

    id_sesion = f"rosco_{id_usuario}_{int(datetime.utcnow().timestamp())}"

    sesion = SesionRosco(
        id_usuario=id_usuario,
        tematica=tematica,
        preguntas=preguntas
    )

    sesiones[id_sesion] = sesion

    return {
        "id_sesion": id_sesion,
        "tematica": tematica,
        "estado": sesion.estado,
        "correctas": 0,
        "incorrectas": 0
    }


def responder_pregunta(id_sesion: str, letra: str, respuesta: str) -> dict:
    sesion = sesiones.get(id_sesion)

    if not sesion:
        return {"error": "Sesión no encontrada"}

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    pregunta = next(
        (
            p for p in sesion.preguntas
            if p["letra"] == letra and p["estado"] in ["pendiente", "pasada"]
        ),
        None
    )

    if not pregunta:
        return {"error": "Pregunta no encontrada"}

    correcta = verificar_respuesta(
        respuesta,
        pregunta["respuesta"]
    )

    if correcta:
        pregunta["estado"] = "correcta"
        sesion.correctas += 1
    else:
        pregunta["estado"] = "incorrecta"
        sesion.incorrectas += 1

    finalizar_si_corresponde(sesion)

    return estado_partida(id_sesion, sesion)


def pasar_pregunta(id_sesion: str, letra: str) -> dict:
    sesion = sesiones.get(id_sesion)

    if not sesion:
        return {"error": "Sesión no encontrada"}

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    pregunta = next(
        (
            p for p in sesion.preguntas
            if p["letra"] == letra and p["estado"] == "pendiente"
        ),
        None
    )

    if not pregunta:
        return {"error": "Pregunta no encontrada"}

    pregunta["estado"] = "pasada"

    return estado_partida(id_sesion, sesion)


def obtener_sesion(id_sesion: str) -> dict:
    sesion = sesiones.get(id_sesion)

    if not sesion:
        return {"error": "Sesión no encontrada"}

    return estado_partida(id_sesion, sesion)


def finalizar_si_corresponde(sesion):
    quedan = any(
        pregunta["estado"] in ["pendiente", "pasada"]
        for pregunta in sesion.preguntas
    )

    if quedan:
        return

    sesion.estado = "finalizada"
    sesion.puntaje = calcular_puntaje(sesion.correctas)
    sesion.finalizada_en = datetime.utcnow().isoformat()


def estado_partida(id_sesion, sesion):
    return {
        "id_sesion": id_sesion,
        "tematica": sesion.tematica,
        "estado": sesion.estado,
        "correctas": sesion.correctas,
        "incorrectas": sesion.incorrectas,
        "puntaje": sesion.puntaje,
        "preguntas": sesion.preguntas
    }