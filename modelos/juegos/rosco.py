from datetime import datetime

class SesionRosco:
    def __init__(self, id_usuario: str, tematica: str, preguntas: list):
        self.id_usuario = id_usuario
        self.tematica = tematica
        self.preguntas = preguntas
        self.estado = "jugando"
        self.correctas = 0
        self.incorrectas = 0
        self.puntaje = 0
        self.creada_en = datetime.utcnow().isoformat()
        self.finalizada_en = None

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "tematica": self.tematica,
            "preguntas": self.preguntas,
            "estado": self.estado,
            "correctas": self.correctas,
            "incorrectas": self.incorrectas,
            "puntaje": self.puntaje,
            "creada_en": self.creada_en,
            "finalizada_en": self.finalizada_en
        }

    @staticmethod
    def from_dict(data: dict) -> "SesionRosco":
        sesion = SesionRosco(
            id_usuario=data["id_usuario"],
            tematica=data["tematica"],
            preguntas=data["preguntas"]
        )

        sesion.estado = data.get("estado", "jugando")
        sesion.correctas = data.get("correctas", 0)
        sesion.incorrectas = data.get("incorrectas", 0)
        sesion.puntaje = data.get("puntaje", 0)
        sesion.creada_en = data.get("creada_en")
        sesion.finalizada_en = data.get("finalizada_en")

        return sesion