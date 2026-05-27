from datetime import datetime

# hay cosas que cambiar una vez este la conexion a firebase
# todavia no se que datos van
class SesionWordle:
    def __init__(self, id_usuario: str, tematica: str, palabra: str, pista: str):
        self.id_usuario = id_usuario
        self.tematica = tematica
        self.palabra = palabra
        self.pista = pista
        self.intentos = []
        self.estado = "jugando"   
        self.puntaje = 0
        self.creada_en = datetime.utcnow().isoformat()
        self.finalizada_en = None

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "tematica": self.tematica,
            "palabra": self.palabra,
            "pista": self.pista,
            "intentos": self.intentos,
            "estado": self.estado,
            "puntaje": self.puntaje,
            "creada_en": self.creada_en,
            "finalizada_en": self.finalizada_en
        }

    @staticmethod
    def from_dict(data: dict) -> "SesionWordle":
        sesion = SesionWordle(
            id_usuario=data["id_usuario"],
            tematica=data["tematica"],
            palabra=data["palabra"],
            pista=data["pista"]
        )
        sesion.intentos = data.get("intentos", [])
        sesion.estado = data.get("estado", "jugando")
        sesion.puntaje = data.get("puntaje", 0)
        sesion.creada_en = data.get("creada_en")
        sesion.finalizada_en = data.get("finalizada_en")
        return sesion