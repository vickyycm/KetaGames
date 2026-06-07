from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for

from controladores.juegos.rosco import (
    iniciar_partida,
    responder_pregunta,
    pasar_pregunta,
    obtener_sesion
)

juegos_bp = Blueprint("juegos", __name__)

@juegos_bp.route("/juegos/rosco/jugar")
def rosco_jugar():

    id_sesion = request.args.get("sesion", "").strip()

    if not id_sesion:
        return redirect(url_for("index"))

    estado = obtener_sesion(id_sesion)

    if "error" in estado:
        return redirect(url_for("index"))

    return render_template(
        "juegos/rosco.html",
        sesion=estado
    )


@juegos_bp.route("/juegos/rosco/iniciar", methods=["POST"])
def rosco_iniciar():

    id_usuario = session.get("id_usuario", "invitado")

    data = request.get_json()
    tematica = data.get("tematica", "").strip()

    if not tematica:
        return jsonify({"error": "Ingresá una temática"}), 400

    resultado = iniciar_partida(
        id_usuario,
        tematica
    )

    return jsonify(resultado), 200


@juegos_bp.route("/juegos/rosco/responder", methods=["POST"])
def rosco_responder():

    data = request.get_json()

    id_sesion = data.get("id_sesion", "").strip()
    letra = data.get("letra", "").strip().upper()
    respuesta = data.get("respuesta", "").strip()

    if not id_sesion or not letra or not respuesta:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = responder_pregunta(
        id_sesion,
        letra,
        respuesta
    )

    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200


@juegos_bp.route("/juegos/rosco/pasar", methods=["POST"])
def rosco_pasar():

    data = request.get_json()

    id_sesion = data.get("id_sesion", "").strip()
    letra = data.get("letra", "").strip().upper()

    if not id_sesion or not letra:
        return jsonify({"error": "Faltan datos"}), 400

    resultado = pasar_pregunta(
        id_sesion,
        letra
    )

    if "error" in resultado:
        return jsonify(resultado), 400

    return jsonify(resultado), 200


@juegos_bp.route("/juegos/rosco/sesion/<id_sesion>")
def rosco_sesion(id_sesion):

    resultado = obtener_sesion(id_sesion)

    if "error" in resultado:
        return jsonify(resultado), 404

    return jsonify(resultado), 200