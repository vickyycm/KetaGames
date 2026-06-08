from flask import Blueprint, request, session, redirect, url_for, jsonify
from servicios.auth_servicio import verificar_token, crear_o_actualizar_usuario
from functools import wraps

auth_bp = Blueprint("auth_bp", __name__)

def requiere_login(f):
    @wraps(f)
    def decorador(*args, **kwargs):
        if "uid" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorador

@auth_bp.route("/auth/google/callback", methods=["POST"])
def google_callback():
    data = request.get_json()
    id_token = data.get("id_token")

    if not id_token:
        return jsonify({"error": "Token no recibido"}), 400

    decoded = verificar_token(id_token)
    if not decoded:
        return jsonify({"error": "Token inválido"}), 401

    usuario = crear_o_actualizar_usuario(decoded)

    session["uid"] = usuario["uid"]
    session["nombre"] = usuario["nombre"]
    session["email"] = usuario["email"]

    return jsonify({"ok": True, "redirect": "/"}), 200

@auth_bp.route("/auth/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@auth_bp.route("/auth/me")
@requiere_login
def me():
    return jsonify({
        "uid": session["uid"],
        "nombre": session["nombre"],
        "email": session["email"]
    })