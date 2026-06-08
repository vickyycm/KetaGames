from datetime import datetime
from firebase_admin import auth
from db.firebase import db
from modelos.usuario import Usuario

def verificar_token(id_token: str) -> dict | None:
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded
    except Exception:
        return None

def crear_o_actualizar_usuario(decoded_token: dict) -> dict:
    uid = decoded_token["uid"]
    ref = db.collection("usuarios").document(uid)
    doc = ref.get()

    ahora = datetime.utcnow().isoformat()

    firebase_info = decoded_token.get("firebase", {})
    proveedor = firebase_info.get("sign_in_provider", "password")
    if proveedor == "google.com":
        proveedor = "google"

    if doc.exists:
        usuario = Usuario.from_dict(doc.to_dict())
        usuario.ultimo_acceso = ahora
        ref.update({"ultimo_acceso": ahora})
        return usuario.to_dict()
    else:
        email = decoded_token.get("email", "")
        nombre_defecto = email.split("@")[0] if email else "Usuario"
        nombre = decoded_token.get("name") or nombre_defecto

        usuario = Usuario(
            uid=uid,
            nombre=nombre,
            email=email,
            foto_url=decoded_token.get("picture", None),
            proveedor=proveedor
        )
        usuario.creado_en = ahora
        usuario.ultimo_acceso = ahora

        ref.set(usuario.to_dict())
        return usuario.to_dict()