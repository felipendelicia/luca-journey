"""✅ Soluciones — assert: afirmaciones"""


def verificar_positivo(n):
    assert n > 0, "n debe ser positivo"
    return n


def verificar_nivel(nivel):
    assert 1 <= nivel <= 100, "el nivel debe estar entre 1 y 100"
    return nivel


def promedio(numeros):
    assert len(numeros) > 0, "lista vacía"
    return sum(numeros) / len(numeros)
