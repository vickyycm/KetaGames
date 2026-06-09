from datetime import datetime

from db.firebase import db
from modelos.juegos.rosco import SesionRosco
from servicios.rosco_servicio import (
    generar_preguntas_demo,
    obtener_siguiente_letra,
    calcular_puntaje
)


def iniciar_partida(id_usuario: str, tematica: str) -> dict:

    preguntas = generar_preguntas_demo()

    id_sesion = f"rosco_{id_usuario}_{int(datetime.utcnow().timestamp())}"

    sesion = SesionRosco(
        id_usuario=id_usuario,
        tematica=tematica,
        preguntas=preguntas
    )

    db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).set(
        sesion.to_dict()
    )

    return {
        "id_sesion": id_sesion,
        "tematica": tematica,
        "letra": "A",
        "definicion": preguntas["A"]["definicion"]
    }


def obtener_sesion(id_sesion: str) -> dict:

    doc = db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionRosco.from_dict(
        doc.to_dict()
    )

    data = {
        "id_sesion": id_sesion,
        "tematica": sesion.tematica,
        "estado": sesion.estado,
        "puntaje": sesion.puntaje,
        "aciertos": sesion.aciertos,
        "errores": sesion.errores,
        "letra_actual": sesion.letra_actual,
        "preguntas": sesion.preguntas
    }

    if sesion.letra_actual:
        data["definicion"] = (
            sesion.preguntas[
                sesion.letra_actual
            ]["definicion"]
        )

    return data


def responder_pregunta(
    id_sesion: str,
    letra: str,
    respuesta: str
) -> dict:

    doc = db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionRosco.from_dict(
        doc.to_dict()
    )

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    pregunta = sesion.preguntas[letra]

    respuesta = respuesta.upper().strip()

    correcta = (
        respuesta ==
        pregunta["respuesta"]
    )

    respuesta_correcta = None

    if correcta:
        pregunta["estado"] = "correcta"
        sesion.aciertos += 1
    else:
        pregunta["estado"] = "incorrecta"
        sesion.errores += 1
        respuesta_correcta = pregunta["respuesta"]

    siguiente_letra = obtener_siguiente_letra(
        sesion.preguntas
    )

    sesion.letra_actual = siguiente_letra

    if siguiente_letra is None:
        sesion.estado = "finalizada"
        sesion.puntaje = calcular_puntaje(
            sesion.aciertos
        )
        sesion.finalizada_en = (
            datetime.utcnow().isoformat()
        )

    db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).set(
        sesion.to_dict()
    )

    resultado = {
        "correcta": correcta,
        "respuesta_correcta": respuesta_correcta,
        "estado": sesion.estado,
        "aciertos": sesion.aciertos,
        "errores": sesion.errores,
        "puntaje": sesion.puntaje,
        "preguntas": sesion.preguntas
    }

    if siguiente_letra:
        resultado["letra_actual"] = siguiente_letra
        resultado["definicion"] = (
            sesion.preguntas[
                siguiente_letra
            ]["definicion"]
        )

    return resultado


def pasar_pregunta(
    id_sesion: str,
    letra: str
) -> dict:

    doc = db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionRosco.from_dict(
        doc.to_dict()
    )

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    sesion.preguntas[letra]["estado"] = "pasada"

    siguiente_letra = obtener_siguiente_letra(
        sesion.preguntas
    )

    sesion.letra_actual = siguiente_letra

    if siguiente_letra is None:
        sesion.estado = "finalizada"
        sesion.puntaje = calcular_puntaje(
            sesion.aciertos
        )
        sesion.finalizada_en = (
            datetime.utcnow().isoformat()
        )

    db.collection(
        "partidas_rosco"
    ).document(
        id_sesion
    ).set(
        sesion.to_dict()
    )

    resultado = {
        "estado": sesion.estado,
        "aciertos": sesion.aciertos,
        "errores": sesion.errores,
        "puntaje": sesion.puntaje,
        "preguntas": sesion.preguntas
    }

    if siguiente_letra:
        resultado["letra_actual"] = siguiente_letra
        resultado["definicion"] = (
            sesion.preguntas[
                siguiente_letra
            ]["definicion"]
        )

    return resultado