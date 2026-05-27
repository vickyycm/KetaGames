MAX_INTENTOS = 6
LARGO_PALABRA = 5


def evaluar_intento(secreta: str, intento: str) -> list[dict]:
    
    secreta = secreta.upper()
    intento = intento.upper()

    resultado = [{"letra": l, "estado": "ausente"} for l in intento]
    secreta_restante = list(secreta)

    for i in range(LARGO_PALABRA):
        if intento[i] == secreta[i]:
            resultado[i]["estado"] = "correcta"
            secreta_restante[i] = None

    for i in range(LARGO_PALABRA):
        if resultado[i]["estado"] == "correcta":
            continue
        if intento[i] in secreta_restante:
            resultado[i]["estado"] = "presente"
            secreta_restante[secreta_restante.index(intento[i])] = None

    return resultado


def intento_valido(intento: str) -> bool:

    return len(intento) == LARGO_PALABRA and intento.isalpha()


def es_ganador(resultado: list[dict]) -> bool:

    return all(r["estado"] == "correcta" for r in resultado)


def calcular_puntaje(intentos_usados: int, gano: bool) -> int:
    
    if not gano:
        return 0
    return max(100 - (intentos_usados - 1) * 10, 50)