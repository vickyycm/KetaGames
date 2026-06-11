from datetime import datetime

class Usuario:

    def __init__(
        self,
        uid: str,
        nombre: str,
        email: str,
        foto_url: str = None,
        proveedor: str = "google"
    ):

        self.uid = uid
        self.nombre = nombre
        self.email = email
        self.foto_url = foto_url
        self.proveedor = proveedor

        self.creado_en = datetime.utcnow().isoformat()
        self.ultimo_acceso = datetime.utcnow().isoformat()

        self.score_total = 0
        self.partidas_totales = 0

        self.wordle_partidas = 0
        self.wordle_ganadas = 0
        self.wordle_mejor_score = 0
        self.wordle_ultimo_score = 0
        self.wordle_score_total = 0

        self.contexto_partidas = 0
        self.contexto_ganadas = 0
        self.contexto_mejor_score = 0
        self.contexto_ultimo_score = 0
        self.contexto_score_total = 0

        self.rosco_partidas = 0
        self.rosco_ganadas = 0
        self.rosco_mejor_score = 0
        self.rosco_ultimo_score = 0
        self.rosco_score_total = 0

    def to_dict(self) -> dict:

        return {
            "uid": self.uid,
            "nombre": self.nombre,
            "email": self.email,
            "foto_url": self.foto_url,
            "proveedor": self.proveedor,
            "creado_en": self.creado_en,
            "ultimo_acceso": self.ultimo_acceso,

            "score_total": self.score_total,
            "partidas_totales": self.partidas_totales,

            "wordle_partidas": self.wordle_partidas,
            "wordle_ganadas": self.wordle_ganadas,
            "wordle_mejor_score": self.wordle_mejor_score,
            "wordle_ultimo_score": self.wordle_ultimo_score,
            "wordle_score_total": self.wordle_score_total,

            "contexto_partidas": self.contexto_partidas,
            "contexto_ganadas": self.contexto_ganadas,
            "contexto_mejor_score": self.contexto_mejor_score,
            "contexto_ultimo_score": self.contexto_ultimo_score,
            "contexto_score_total": self.contexto_score_total,

            "rosco_partidas": self.rosco_partidas,
            "rosco_ganadas": self.rosco_ganadas,
            "rosco_mejor_score": self.rosco_mejor_score,
            "rosco_ultimo_score": self.rosco_ultimo_score,
            "rosco_score_total": self.rosco_score_total,
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

        u.score_total = data.get("score_total", 0)
        u.partidas_totales = data.get("partidas_totales", 0)

        u.wordle_partidas = data.get("wordle_partidas", 0)
        u.wordle_ganadas = data.get("wordle_ganadas", 0)
        u.wordle_mejor_score = data.get("wordle_mejor_score", 0)
        u.wordle_ultimo_score = data.get("wordle_ultimo_score", 0)
        u.wordle_score_total = data.get("wordle_score_total", 0)

        u.contexto_partidas = data.get("contexto_partidas", 0)
        u.contexto_ganadas = data.get("contexto_ganadas", 0)
        u.contexto_mejor_score = data.get("contexto_mejor_score", 0)
        u.contexto_ultimo_score = data.get("contexto_ultimo_score", 0)
        u.contexto_score_total = data.get("contexto_score_total", 0)

        u.rosco_partidas = data.get("rosco_partidas", 0)
        u.rosco_ganadas = data.get("rosco_ganadas", 0)
        u.rosco_mejor_score = data.get("rosco_mejor_score", 0)
        u.rosco_ultimo_score = data.get("rosco_ultimo_score", 0)
        u.rosco_score_total = data.get("rosco_score_total", 0)

        return u