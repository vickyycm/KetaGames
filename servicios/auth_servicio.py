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
        datos = doc.to_dict()
        usuario = Usuario.from_dict(datos)
        usuario.ultimo_acceso = ahora
        ref.update({"ultimo_acceso": ahora})
        resultado = usuario.to_dict()
        resultado["activo"] = datos.get("activo", True)
        return resultado
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

def actualizar_estadisticas_usuario(
    uid: str,
    juego: str,
    score: int,
    gano: bool = False
):
    ref = db.collection("usuarios").document(uid)
    doc = ref.get()

    if not doc.exists:
        return

    datos = doc.to_dict()

    update_data = {
        "score_total": datos.get("score_total", 0) + score,
        "partidas_totales": datos.get("partidas_totales", 0) + 1
    }

    if juego == "wordle":
        update_data["wordle_partidas"] = datos.get("wordle_partidas", 0) + 1
        update_data["wordle_ganadas"] = datos.get("wordle_ganadas", 0) + (1 if gano else 0)
        update_data["wordle_mejor_score"] = max(datos.get("wordle_mejor_score", 0), score)
        update_data["wordle_ultimo_score"] = score
        update_data["wordle_score_total"] = datos.get("wordle_score_total", 0) + score

    elif juego == "contexto":
        update_data["contexto_partidas"] = datos.get("contexto_partidas", 0) + 1
        update_data["contexto_ganadas"] = datos.get("contexto_ganadas", 0) + (1 if gano else 0)
        update_data["contexto_mejor_score"] = max(datos.get("contexto_mejor_score", 0), score)
        update_data["contexto_ultimo_score"] = score
        update_data["contexto_score_total"] = datos.get("contexto_score_total", 0) + score

    elif juego == "rosco":
        update_data["rosco_partidas"] = datos.get("rosco_partidas", 0) + 1
        update_data["rosco_ganadas"] = datos.get("rosco_ganadas", 0) + (1 if gano else 0)
        update_data["rosco_mejor_score"] = max(datos.get("rosco_mejor_score", 0), score)
        update_data["rosco_ultimo_score"] = score
        update_data["rosco_score_total"] = datos.get("rosco_score_total", 0) + score

    ref.update(update_data)