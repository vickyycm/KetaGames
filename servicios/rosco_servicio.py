LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generar_preguntas_por_tematica(tematica):

    tematica = tematica.lower().strip()

    if tematica == "animales":

        return {
            "A": {"respuesta": "ABEJA", "definicion": "Empieza con A: insecto productor de miel", "estado": "pendiente"},
            "B": {"respuesta": "BALLENA", "definicion": "Empieza con B: mamífero marino gigante", "estado": "pendiente"},
            "C": {"respuesta": "CAMELLO", "definicion": "Empieza con C: animal con jorobas", "estado": "pendiente"},
            "D": {"respuesta": "DELFIN", "definicion": "Empieza con D: mamífero marino muy inteligente", "estado": "pendiente"},
            "E": {"respuesta": "ELEFANTE", "definicion": "Empieza con E: el mamífero terrestre más grande", "estado": "pendiente"},
            "F": {"respuesta": "FOCA", "definicion": "Empieza con F: mamífero marino de cuerpo redondeado", "estado": "pendiente"},
            "G": {"respuesta": "GANSO", "definicion": "Empieza con G: ave doméstica de cuello largo", "estado": "pendiente"},
            "H": {"respuesta": "HIPOPOTAMO", "definicion": "Empieza con H: gran mamífero africano", "estado": "pendiente"},
            "I": {"respuesta": "IGUANA", "definicion": "Empieza con I: reptil de sangre fría", "estado": "pendiente"},
            "J": {"respuesta": "JABALI", "definicion": "Empieza con J: cerdo salvaje", "estado": "pendiente"},
            "K": {"respuesta": "KOALA", "definicion": "Empieza con K: marsupial australiano", "estado": "pendiente"},
            "L": {"respuesta": "LEON", "definicion": "Empieza con L: rey de la selva", "estado": "pendiente"},
            "M": {"respuesta": "MONO", "definicion": "Empieza con M: primate muy común", "estado": "pendiente"},
            "N": {"respuesta": "NUTRIA", "definicion": "Empieza con N: mamífero acuático", "estado": "pendiente"},
            "O": {"respuesta": "OSO", "definicion": "Empieza con O: mamífero grande y fuerte", "estado": "pendiente"},
            "P": {"respuesta": "PINGUINO", "definicion": "Empieza con P: ave que no vuela", "estado": "pendiente"},
            "Q": {"respuesta": "QUETZAL", "definicion": "Empieza con Q: ave centroamericana", "estado": "pendiente"},
            "R": {"respuesta": "RINOCERONTE", "definicion": "Empieza con R: animal con cuerno", "estado": "pendiente"},
            "S": {"respuesta": "SERPIENTE", "definicion": "Empieza con S: reptil sin patas", "estado": "pendiente"},
            "T": {"respuesta": "TIGRE", "definicion": "Empieza con T: felino rayado", "estado": "pendiente"},
            "U": {"respuesta": "URRACA", "definicion": "Empieza con U: ave de plumaje blanco y negro", "estado": "pendiente"},
            "V": {"respuesta": "VACA", "definicion": "Empieza con V: animal productor de leche", "estado": "pendiente"},
            "W": {"respuesta": "WALLABY", "definicion": "Empieza con W: marsupial australiano", "estado": "pendiente"},
            "X": {"respuesta": "XIFOSURO", "definicion": "Empieza con X: artrópodo marino", "estado": "pendiente"},
            "Y": {"respuesta": "YACARE", "definicion": "Empieza con Y: reptil sudamericano", "estado": "pendiente"},
            "Z": {"respuesta": "ZORRO", "definicion": "Empieza con Z: cánido salvaje", "estado": "pendiente"}
        }

    return {
        "A": {"respuesta": "ALBANIA", "definicion": "Empieza con A: país europeo cuya capital es Tirana", "estado": "pendiente"},
        "B": {"respuesta": "BRASIL", "definicion": "Empieza con B: país más grande de Sudamérica", "estado": "pendiente"},
        "C": {"respuesta": "CHINA", "definicion": "Empieza con C: país más poblado del mundo", "estado": "pendiente"},
        "D": {"respuesta": "DINAMARCA", "definicion": "Empieza con D: país nórdico", "estado": "pendiente"},
        "E": {"respuesta": "ESPAÑA", "definicion": "Empieza con E: país europeo cuya capital es Madrid", "estado": "pendiente"},
        "F": {"respuesta": "FRANCIA", "definicion": "Empieza con F: país de la Torre Eiffel", "estado": "pendiente"},
        "G": {"respuesta": "GRECIA", "definicion": "Empieza con G: cuna de la democracia", "estado": "pendiente"},
        "H": {"respuesta": "HAITI", "definicion": "Empieza con H: país del Caribe", "estado": "pendiente"},
        "I": {"respuesta": "INDIA", "definicion": "Empieza con I: segundo país más poblado del mundo", "estado": "pendiente"},
        "J": {"respuesta": "JAPON", "definicion": "Empieza con J: país del sol naciente", "estado": "pendiente"},
        "K": {"respuesta": "KENIA", "definicion": "Empieza con K: país africano", "estado": "pendiente"},
        "L": {"respuesta": "LIBIA", "definicion": "Empieza con L: país del norte de África", "estado": "pendiente"},
        "M": {"respuesta": "MEXICO", "definicion": "Empieza con M: país norteamericano", "estado": "pendiente"},
        "N": {"respuesta": "NORUEGA", "definicion": "Empieza con N: país famoso por sus fiordos", "estado": "pendiente"},
        "O": {"respuesta": "OMAN", "definicion": "Empieza con O: país de Medio Oriente", "estado": "pendiente"},
        "P": {"respuesta": "PERU", "definicion": "Empieza con P: país de Machu Picchu", "estado": "pendiente"},
        "Q": {"respuesta": "QATAR", "definicion": "Empieza con Q: sede del Mundial 2022", "estado": "pendiente"},
        "R": {"respuesta": "RUSIA", "definicion": "Empieza con R: país más extenso del mundo", "estado": "pendiente"},
        "S": {"respuesta": "SUECIA", "definicion": "Empieza con S: país escandinavo", "estado": "pendiente"},
        "T": {"respuesta": "TURQUIA", "definicion": "Empieza con T: país entre Europa y Asia", "estado": "pendiente"},
        "U": {"respuesta": "URUGUAY", "definicion": "Empieza con U: vecino de Argentina", "estado": "pendiente"},
        "V": {"respuesta": "VENEZUELA", "definicion": "Empieza con V: país sudamericano", "estado": "pendiente"},
        "W": {"respuesta": "WALES", "definicion": "Empieza con W: nación constitutiva del Reino Unido", "estado": "pendiente"},
        "X": {"respuesta": "XINJIANG", "definicion": "Empieza con X: región autónoma de China", "estado": "pendiente"},
        "Y": {"respuesta": "YEMEN", "definicion": "Empieza con Y: país de la península arábiga", "estado": "pendiente"},
        "Z": {"respuesta": "ZAMBIA", "definicion": "Empieza con Z: país africano", "estado": "pendiente"}
    }


def obtener_siguiente_letra(preguntas):

    for letra in LETRAS:
        if preguntas[letra]["estado"] == "pendiente":
            return letra

    for letra in LETRAS:
        if preguntas[letra]["estado"] == "pasada":
            return letra

    return None
def hay_preguntas_pendientes(preguntas):

    for letra in LETRAS:
        if preguntas[letra]["estado"] in [
            "pendiente",
            "pasada"
        ]:
            return True

    return False

def calcular_puntaje(aciertos):
    return aciertos * 10