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

    if doc.exists:
        ref.update({"ultimo_acceso": ahora})
        data = doc.to_dict()
        data["ultimo_acceso"] = ahora
        return data
    else:
        nuevo = {
            "uid": uid,
            "nombre": decoded_token.get("name", ""),
            "email": decoded_token.get("email", ""),
            "foto_url": decoded_token.get("picture", None),
            "proveedor": "google",
            "creado_en": ahora,
            "ultimo_acceso": ahora
        }
        ref.set(nuevo)
        return nuevo