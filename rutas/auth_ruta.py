from flask import Blueprint, session, redirect, url_for

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/auth/test-login")
def test_login():

    session["id_usuario"] = "usuario_test"

    return {
        "mensaje":"login ok",
        "usuario": session["id_usuario"]
    }


@auth_bp.route("/auth/logout")
def logout():

    session.clear()

    return {"mensaje":"logout ok"}