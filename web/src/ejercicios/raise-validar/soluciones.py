"""✅ Soluciones — Lanzar errores: raise"""


def validar_edad(edad):
    if edad < 0:
        raise ValueError("edad inválida")
    return edad


def validar_nivel(nivel):
    if nivel < 1 or nivel > 100:
        raise ValueError("el nivel debe estar entre 1 y 100")
    return nivel


def dividir(a, b):
    if b == 0:
        raise ValueError("no se puede dividir por cero")
    return a / b


def solo_texto(x):
    if not isinstance(x, str):
        raise TypeError("debe ser un string")
    return x
