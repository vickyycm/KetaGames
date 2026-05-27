from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for
from controladores.juegos.wordle import (
    iniciar_partida,
    enviar_intento,
    obtener_sesion
)

juegos_bp = Blueprint("juegos", __name__)

JUEGOS = {
    "palabra_del_dia": "Palabra del Día",
    "rosco":           "Rosco",
    "contexto":        "Contexto"
}

@juegos_bp.route("/tematica/<juego>")
def seleccionar_tematica(juego):
    
    if juego not in JUEGOS:
        return redirect(url_for("index"))

    return render_template(
        "juegos/tematica.html",
        juego=juego,
        nombre_juego=JUEGOS[juego]
    )


@juegos_bp.route("/juegos/wordle/jugar")
def wordle_jugar():
    
    id_sesion = request.args.get("sesion", "").strip()

    if not id_sesion:
        return redirect(url_for("juegos.seleccionar_tematica", juego="palabra_del_dia"))

    estado = obtener_sesion(id_sesion)

    if "error" in estado:
        return redirect(url_for("juegos.seleccionar_tematica", juego="palabra_del_dia"))

    return render_template("juegos/wordle.html", sesion=estado)


@juegos_bp.route("/juegos/wordle/iniciar", methods=["POST"])
def wordle_iniciar():
    
    id_usuario = session.get("id_usuario", "invitado")

    data = request.get_json()
    tematica = data.get("tematica", "").strip()

    if not tematica:
        return jsonify({"error": "Ingresá una temática"}), 400

    resultado = iniciar_partida(id_usuario, tematica)

    if "error" in resultado:
        return jsonify(resultado), 500

    return jsonify(resultado), 200


@juegos_bp.route("/juegos/wordle/intento", methods=["POST"])
def wordle_intento():
    
    data = request.get_json()
    id_sesion = data.get("id_sesion", "").strip()
    palabra_intento = data.get("intento", "").strip()

    if not id_sesion or not palabra_intento:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = enviar_intento(id_sesion, palabra_intento)

    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200


@juegos_bp.route("/juegos/wordle/sesion/<id_sesion>", methods=["GET"])
def wordle_sesion(id_sesion):
    
    resultado = obtener_sesion(id_sesion)

    if "error" in resultado:
        return jsonify(resultado), 404

    return jsonify(resultado), 200