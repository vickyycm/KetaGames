from flask import Blueprint, render_template
from db.firebase import db
from flask import redirect, url_for
from datetime import datetime
from flask import session
from functools import wraps


def requiere_admin(func):

    @wraps(func)
    def wrapper(*args, **kwargs):

        uid = session.get("uid")

        if not uid:
            return redirect(url_for("index"))

        doc = db.collection("usuarios").document(uid).get()

        if not doc.exists:
            return redirect(url_for("index"))

        usuario = doc.to_dict()

        if usuario.get("rol") != "admin":
            return redirect(url_for("index"))

        return func(*args, **kwargs)

    return wrapper


admin_bp = Blueprint(
    "admin",
    __name__
)


@admin_bp.route("/admin")
@requiere_admin
def dashboard():

    return render_template(
        "admin/panel.html"
    )


@admin_bp.route("/admin/usuarios")
@requiere_admin
def usuarios():

    docs = db.collection("usuarios").stream()

    lista_usuarios = []

    for doc in docs:

        usuario = doc.to_dict()

        if "activo" not in usuario:
            usuario["activo"] = True

        lista_usuarios.append(usuario)

    return render_template(
        "admin/usuarios.html",
        usuarios=lista_usuarios
    )


@admin_bp.route("/admin/usuarios/toggle/<uid>")
@requiere_admin
def toggle_usuario(uid):

    ref = db.collection("usuarios").document(uid)

    doc = ref.get()

    if not doc.exists:
        return redirect(url_for("admin.usuarios"))

    usuario = doc.to_dict()

    activo_actual = usuario.get(
        "activo",
        True
    )

    nuevo_estado = not activo_actual

    ref.update({
        "activo": nuevo_estado
    })

    db.collection("logs_admin").add({
        "accion": (
            "reactivar_usuario"
            if nuevo_estado
            else "suspender_usuario"
        ),
        "uid_usuario": uid,
        "fecha": datetime.utcnow().isoformat()
    })

    return redirect(
        url_for("admin.usuarios")
    )


@admin_bp.route("/admin/panel")
@requiere_admin
def panel():

    usuarios = list(
        db.collection("usuarios").stream()
    )

    total_usuarios = len(usuarios)

    total_wordle = 0
    total_contexto = 0
    total_rosco = 0

    for usuario in usuarios:

        data = usuario.to_dict()

        total_wordle += data.get(
            "wordle_partidas",
            0
        )

        total_contexto += data.get(
            "contexto_partidas",
            0
        )

        total_rosco += data.get(
            "rosco_partidas",
            0
        )

    usuarios_stats = []

    for usuario in usuarios:

        data = usuario.to_dict()

        usuarios_stats.append({
            "nombre": data.get("nombre", ""),
            "email": data.get("email", ""),
            "ultimo_acceso": data.get(
                "ultimo_acceso",
                "-"
            ),
            "partidas_totales": data.get(
                "partidas_totales",
                0
            ),
            "score_total": data.get(
                "score_total",
                0
            )
        })

    return render_template(
        "admin/panel.html",
        total_usuarios=total_usuarios,
        total_wordle=total_wordle,
        total_contexto=total_contexto,
        total_rosco=total_rosco,
        usuarios_stats=usuarios_stats
    )