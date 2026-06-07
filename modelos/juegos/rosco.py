from datetime import datetime


class SesionRosco:
    def __init__(self, id_usuario: str, tematica: str, preguntas: dict):
        self.id_usuario = id_usuario
        self.tematica = tematica
        self.preguntas = preguntas
        self.estado = "jugando"
        self.puntaje = 0
        self.letra_actual = "A"
        self.aciertos = 0
        self.errores = 0
        self.creada_en = datetime.utcnow().isoformat()
        self.finalizada_en = None

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "tematica": self.tematica,
            "preguntas": self.preguntas,
            "estado": self.estado,
            "puntaje": self.puntaje,
            "letra_actual": self.letra_actual,
            "aciertos": self.aciertos,
            "errores": self.errores,
            "creada_en": self.creada_en,
            "finalizada_en": self.finalizada_en
        }

    @staticmethod
    def from_dict(data):
        sesion = SesionRosco(
            id_usuario=data["id_usuario"],
            tematica=data["tematica"],
            preguntas=data["preguntas"]
        )

        sesion.estado = data.get("estado", "jugando")
        sesion.puntaje = data.get("puntaje", 0)
        sesion.letra_actual = data.get("letra_actual", "A")
        sesion.aciertos = data.get("aciertos", 0)
        sesion.errores = data.get("errores", 0)
        sesion.creada_en = data.get("creada_en")
        sesion.finalizada_en = data.get("finalizada_en")

        return sesion