LETRAS = [
    "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S",
    "T", "U", "V", "W", "X", "Y", "Z"
]

def obtener_rosco_mock():
    return [
        {
            "letra": "A",
            "pregunta": "Club inglés de Londres",
            "respuesta": "ARSENAL",
            "estado": "pendiente"
        },
        {
            "letra": "B",
            "pregunta": "Selección campeona del mundo cinco veces",
            "respuesta": "BRASIL",
            "estado": "pendiente"
        },
        {
            "letra": "C",
            "pregunta": "Apellido de Cristiano",
            "respuesta": "CRISTIANO",
            "estado": "pendiente"
        },
        {
            "letra": "D",
            "pregunta": "Jugador histórico argentino de apellido Maradona",
            "respuesta": "DIEGO",
            "estado": "pendiente"
        },
        {
            "letra": "E",
            "pregunta": "Equipo inglés de Liverpool",
            "respuesta": "EVERTON",
            "estado": "pendiente"
        },
        {
            "letra": "F",
            "pregunta": "Club español de Barcelona",
            "respuesta": "FCBARCELONA",
            "estado": "pendiente"
        },
        {
            "letra": "G",
            "pregunta": "Club francés de París",
            "respuesta": "GPS",
            "estado": "pendiente"
        },
        {
            "letra": "H",
            "pregunta": "Delantero francés Thierry",
            "respuesta": "HENRY",
            "estado": "pendiente"
        },
        {
            "letra": "I",
            "pregunta": "Club italiano de Milán",
            "respuesta": "INTER",
            "estado": "pendiente"
        },
        {
            "letra": "J",
            "pregunta": "País donde nació Cruyff",
            "respuesta": "JAPON",
            "estado": "pendiente"
        },
        {
            "letra": "K",
            "pregunta": "Apellido del arquero alemán Oliver",
            "respuesta": "KAHN",
            "estado": "pendiente"
        },
        {
            "letra": "L",
            "pregunta": "Club inglés conocido como los Reds",
            "respuesta": "LIVERPOOL",
            "estado": "pendiente"
        },
        {
            "letra": "M",
            "pregunta": "Apellido del capitán argentino campeón del mundo 2022",
            "respuesta": "MESSI",
            "estado": "pendiente"
        },
        {
            "letra": "N",
            "pregunta": "Apellido del delantero brasileño Neymar",
            "respuesta": "NEYMAR",
            "estado": "pendiente"
        },
        {
            "letra": "O",
            "pregunta": "Apellido del delantero Michael del Bayern",
            "respuesta": "OWEN",
            "estado": "pendiente"
        },
        {
            "letra": "P",
            "pregunta": "Apellido del arquero argentino campeón del mundo Ubaldo",
            "respuesta": "PUMPIDO",
            "estado": "pendiente"
        },
        {
            "letra": "Q",
            "pregunta": "Apellido del ex jugador Ricardo de River",
            "respuesta": "QUARESMA",
            "estado": "pendiente"
        },
        {
            "letra": "R",
            "pregunta": "Apellido de Cristiano",
            "respuesta": "RONALDO",
            "estado": "pendiente"
        },
        {
            "letra": "S",
            "pregunta": "Club alemán de Gelsenkirchen",
            "respuesta": "SCHALKE",
            "estado": "pendiente"
        },
        {
            "letra": "T",
            "pregunta": "Apellido del delantero francés David",
            "respuesta": "TREZEGUET",
            "estado": "pendiente"
        },
        {
            "letra": "U",
            "pregunta": "Club de Montevideo",
            "respuesta": "URUGUAY",
            "estado": "pendiente"
        },
        {
            "letra": "V",
            "pregunta": "Apellido del ex arquero español Victor",
            "respuesta": "VALDES",
            "estado": "pendiente"
        },
        {
            "letra": "W",
            "pregunta": "Apellido del delantero inglés Wayne",
            "respuesta": "WAYNE",
            "estado": "pendiente"
        },
        {
            "letra": "X",
            "pregunta": "Apellido del mediocampista Xabi",
            "respuesta": "XABI",
            "estado": "pendiente"
        },
        {
            "letra": "Y",
            "pregunta": "Apellido del ex defensor argentino Walter",
            "respuesta": "YACOB",
            "estado": "pendiente"
        },
        {
            "letra": "Z",
            "pregunta": "Apellido del delantero chileno Iván",
            "respuesta": "ZAMORANO",
            "estado": "pendiente"
        }
    ]

def verificar_respuesta(respuesta_usuario, respuesta_correcta):
    return respuesta_usuario.strip().upper() == respuesta_correcta.strip().upper()

def calcular_puntaje(correctas):
    return correctas * 10