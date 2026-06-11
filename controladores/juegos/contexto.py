from datetime import datetime
from db.firebase import db
from modelos.juegos.contexto import SesionContexto
from servicios.contexto_servicio import calcular_similitud, validar_palabra
from controladores.juegos.wordle import obtener_palabra_de_tematica
from servicios.auth_servicio import actualizar_estadisticas_usuario
import random

MAX_INTENTOS = 100

def obtener_palabra_contexto(tematica: str) -> dict:
    tematica_id = tematica.lower().strip()
    ref = db.collection("tematicas_palabras_contexto").document(tematica_id)
    doc = ref.get()

    palabras_disponibles = []

    if doc.exists:
        palabras_disponibles = doc.to_dict().get("palabras", [])

    if not palabras_disponibles:
        palabras_disponibles = [
            "FAMILIA", "HOGAR", "TECHO", "PUERTA", "COCINA",
            "JARDIN", "PATIO", "CUARTO", "SALON", "MUEBLE",
            "CAMA", "MESA", "SILLA", "VENTANA", "PARED",
            "SUELO", "BALCON", "TECHO", "ARMARIO", "PASILLO"
        ]

    palabra_elegida = random.choice(palabras_disponibles)
    palabras_disponibles.remove(palabra_elegida)

    ref.set({
        "nombre_original": tematica,
        "palabras": palabras_disponibles
    }, merge=True)

    return {"palabra": palabra_elegida}


def iniciar_partida(id_usuario: str, tematica: str) -> dict:
    resultado = obtener_palabra_contexto(tematica)
    if "error" in resultado:
        return resultado

    id_sesion = f"ctx_{id_usuario}_{int(datetime.utcnow().timestamp())}"

    sesion = SesionContexto(
        id_usuario=id_usuario,
        tematica=tematica,
        palabra=resultado["palabra"]
    )

    db.collection("partidas_contexto").document(id_sesion).set(sesion.to_dict())

    return {
        "id_sesion": id_sesion,
        "tematica": tematica,
        "max_intentos": MAX_INTENTOS
    }


def enviar_intento(id_sesion: str, intento: str) -> dict:
    ref = db.collection("partidas_contexto").document(id_sesion)
    doc = ref.get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionContexto.from_dict(doc.to_dict())

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    intento = intento.lower().strip()

    if not validar_palabra(intento):
        return {"error": "Palabra no válida o menor a 4 letras"}

    ya_ingresada = any(i["palabra"] == intento for i in sesion.intentos)
    if ya_ingresada:
        return {"error": "Ya ingresaste esa palabra"}

    similitud = calcular_similitud(sesion.palabra, intento)
    gano = intento.lower() == sesion.palabra.lower()

    nuevo_intento = {
        "palabra": intento,
        "similitud": similitud,
        "timestamp": datetime.utcnow().isoformat()
    }

    sesion.intentos.append(nuevo_intento)
    sesion.cantidad_intentos += 1

    if gano:
        sesion.estado = "ganada"
        sesion.gano = True
        sesion.finalizada_en = datetime.utcnow().isoformat()
        sesion.puntaje = max(100 - (sesion.cantidad_intentos - 1), 10)
    elif sesion.cantidad_intentos >= MAX_INTENTOS:
        sesion.estado = "perdida"
        sesion.finalizada_en = datetime.utcnow().isoformat()

    if sesion.estado != "jugando" and sesion.id_usuario != "invitado":
        actualizar_estadisticas_usuario(
            sesion.id_usuario,
            "contexto",
            sesion.puntaje,
            gano=gano
        )

    ref.update(sesion.to_dict())

    intentos_ordenados = sorted(sesion.intentos, key=lambda x: x["similitud"])

    return {
        "similitud": similitud,
        "estado": sesion.estado,
        "gano": sesion.gano,
        "cantidad_intentos": sesion.cantidad_intentos,
        "max_intentos": MAX_INTENTOS,
        "intentos_ordenados": intentos_ordenados,
        "puntaje": sesion.puntaje,
        **({"palabra": sesion.palabra} if sesion.estado != "jugando" else {})
    }


def rendirse(id_sesion: str) -> dict:
    ref = db.collection("partidas_contexto").document(id_sesion)
    doc = ref.get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionContexto.from_dict(doc.to_dict())

    if sesion.estado != "jugando":
        return {"error": "La partida ya terminó"}

    sesion.estado = "rendida"
    sesion.finalizada_en = datetime.utcnow().isoformat()

    if sesion.id_usuario != "invitado":
        actualizar_estadisticas_usuario(
            sesion.id_usuario,
            "contexto",
            0,
            gano=False
        )

    ref.update(sesion.to_dict())

    return {
        "estado": "rendida",
        "palabra": sesion.palabra
    }


def obtener_sesion(id_sesion: str) -> dict:
    doc = db.collection("partidas_contexto").document(id_sesion).get()

    if not doc.exists:
        return {"error": "Sesión no encontrada"}

    sesion = SesionContexto.from_dict(doc.to_dict())

    intentos_ordenados = sorted(sesion.intentos, key=lambda x: x["similitud"])

    data = {
        "id_sesion": id_sesion,
        "tematica": sesion.tematica,
        "intentos_ordenados": intentos_ordenados,
        "cantidad_intentos": sesion.cantidad_intentos,
        "max_intentos": MAX_INTENTOS,
        "estado": sesion.estado,
        "puntaje": sesion.puntaje
    }

    if sesion.estado != "jugando":
        data["palabra"] = sesion.palabra

    return data