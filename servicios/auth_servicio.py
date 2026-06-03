from datetime import datetime
from firebase_admin import auth
from db.firebase import db

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
    proveedor = firebase_info.get("sign_in_provider", "password") # 'password' es email/contraseña
    if proveedor == "google.com":
        proveedor = "google"

    if doc.exists:
        ref.update({"ultimo_acceso": ahora})
        data = doc.to_dict()
        data["ultimo_acceso"] = ahora
        return data
    else:
        email = decoded_token.get("email", "")
        nombre_defecto = email.split("@")[0] if email else "Usuario"
        nombre = decoded_token.get("name") or nombre_defecto

        nuevo = {
            "uid": uid,
            "nombre": nombre,
            "email": email,
            "foto_url": decoded_token.get("picture", None),
            "proveedor": proveedor,
            "creado_en": ahora,
            "ultimo_acceso": ahora
        }
        ref.set(nuevo)
        return nuevo