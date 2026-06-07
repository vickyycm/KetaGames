LETRAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generar_preguntas_demo():
    return {
        "A": {
            "respuesta": "ARGENTINA",
            "definicion": "País campeón del mundo en 2022",
            "estado": "pendiente"
        },
        "B": {
            "respuesta": "BOCA",
            "definicion": "Club de fútbol de la Ribera",
            "estado": "pendiente"
        },
        "C": {
            "respuesta": "CORDOBA",
            "definicion": "Provincia argentina muy conocida",
            "estado": "pendiente"
        },
        "D": {
            "respuesta": "DOLAR",
            "definicion": "Moneda de Estados Unidos",
            "estado": "pendiente"
        },
        "E": {
            "respuesta": "ESPAÑA",
            "definicion": "País europeo",
            "estado": "pendiente"
        },
        "F": {
            "respuesta": "FUTBOL",
            "definicion": "Deporte más popular de Argentina",
            "estado": "pendiente"
        },
        "G": {
            "respuesta": "GATO",
            "definicion": "Animal doméstico felino",
            "estado": "pendiente"
        },
        "H": {
            "respuesta": "HIELO",
            "definicion": "Agua en estado sólido",
            "estado": "pendiente"
        },
        "I": {
            "respuesta": "IGLESIA",
            "definicion": "Lugar de culto religioso",
            "estado": "pendiente"
        },
        "J": {
            "respuesta": "JARDIN",
            "definicion": "Espacio con plantas y flores",
            "estado": "pendiente"
        },
        "K": {
            "respuesta": "KARATE",
            "definicion": "Arte marcial japonés",
            "estado": "pendiente"
        },
        "L": {
            "respuesta": "LIBRO",
            "definicion": "Conjunto de páginas encuadernadas",
            "estado": "pendiente"
        },
        "M": {
            "respuesta": "MONTAÑA",
            "definicion": "Elevación natural del terreno",
            "estado": "pendiente"
        },
        "N": {
            "respuesta": "NARANJA",
            "definicion": "Fruta cítrica",
            "estado": "pendiente"
        },
        "O": {
            "respuesta": "OCEANO",
            "definicion": "Gran masa de agua salada",
            "estado": "pendiente"
        },
        "P": {
            "respuesta": "PERRO",
            "definicion": "Animal considerado el mejor amigo del hombre",
            "estado": "pendiente"
        },
        "Q": {
            "respuesta": "QUESO",
            "definicion": "Alimento derivado de la leche",
            "estado": "pendiente"
        },
        "R": {
            "respuesta": "RIO",
            "definicion": "Corriente natural de agua",
            "estado": "pendiente"
        },
        "S": {
            "respuesta": "SOL",
            "definicion": "Estrella del sistema solar",
            "estado": "pendiente"
        },
        "T": {
            "respuesta": "TIGRE",
            "definicion": "Felino salvaje rayado",
            "estado": "pendiente"
        },
        "U": {
            "respuesta": "UNIVERSIDAD",
            "definicion": "Institución de educación superior",
            "estado": "pendiente"
        },
        "V": {
            "respuesta": "VENTANA",
            "definicion": "Abertura en una pared para iluminar",
            "estado": "pendiente"
        },
        "W": {
            "respuesta": "WHISKY",
            "definicion": "Bebida alcohólica destilada",
            "estado": "pendiente"
        },
        "X": {
            "respuesta": "XILOFON",
            "definicion": "Instrumento musical de percusión",
            "estado": "pendiente"
        },
        "Y": {
            "respuesta": "YATE",
            "definicion": "Embarcación de recreo",
            "estado": "pendiente"
        },
        "Z": {
            "respuesta": "ZORRO",
            "definicion": "Animal salvaje parecido a un perro",
            "estado": "pendiente"
        }
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