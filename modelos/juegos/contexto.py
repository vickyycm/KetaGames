from datetime import datetime

class SesionContexto:
    def __init__(self, id_usuario: str, tematica: str, palabra: str):
        self.id_usuario = id_usuario
        self.tematica = tematica
        self.palabra = palabra
        self.intentos = []
        self.estado = "jugando"
        self.gano = False
        self.cantidad_intentos = 0
        self.puntaje = 0
        self.creada_en = datetime.utcnow().isoformat()
        self.finalizada_en = None

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "tematica": self.tematica,
            "palabra": self.palabra,
            "intentos": self.intentos,
            "estado": self.estado,
            "gano": self.gano,
            "cantidad_intentos": self.cantidad_intentos,
            "puntaje": self.puntaje,
            "creada_en": self.creada_en,
            "finalizada_en": self.finalizada_en
        }

    @staticmethod
    def from_dict(data: dict) -> "SesionContexto":
        s = SesionContexto(
            id_usuario=data["id_usuario"],
            tematica=data["tematica"],
            palabra=data["palabra"]
        )
        s.intentos = data.get("intentos", [])
        s.estado = data.get("estado", "jugando")
        s.gano = data.get("gano", False)
        s.cantidad_intentos = data.get("cantidad_intentos", 0)
        s.puntaje = data.get("puntaje", 0)
        s.creada_en = data.get("creada_en")
        s.finalizada_en = data.get("finalizada_en")
        return s