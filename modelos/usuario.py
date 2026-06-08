from datetime import datetime

class Usuario:
    def __init__(self, uid: str, nombre: str, email: str,
                 foto_url: str = None, proveedor: str = "google"):
        self.uid = uid
        self.nombre = nombre
        self.email = email
        self.foto_url = foto_url
        self.proveedor = proveedor
        self.creado_en = datetime.utcnow().isoformat()
        self.ultimo_acceso = datetime.utcnow().isoformat()

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "nombre": self.nombre,
            "email": self.email,
            "foto_url": self.foto_url,
            "proveedor": self.proveedor,
            "creado_en": self.creado_en,
            "ultimo_acceso": self.ultimo_acceso
        }

    @staticmethod
    def from_dict(data: dict) -> "Usuario":
        u = Usuario(
            uid=data["uid"],
            nombre=data["nombre"],
            email=data["email"],
            foto_url=data.get("foto_url"),
            proveedor=data.get("proveedor", "google")
        )
        u.creado_en = data.get("creado_en", u.creado_en)
        u.ultimo_acceso = data.get("ultimo_acceso", u.ultimo_acceso)
        return u