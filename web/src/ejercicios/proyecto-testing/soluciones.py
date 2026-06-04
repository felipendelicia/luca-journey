"""✅ Soluciones — Proyecto: módulo testeado"""


def raiz_cuadrada(n):
    if n < 0:
        raise ValueError("no hay raíz cuadrada de un número negativo")
    return n ** 0.5


def probar_raiz(raiz):
    assert raiz(9) == 3
    assert raiz(0) == 0
    try:
        raiz(-1)
    except ValueError:
        return
    raise AssertionError("raiz(-1) debería lanzar ValueError")


def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None


def probar_dividir_seguro(dividir_seguro):
    assert dividir_seguro(6, 2) == 3
    assert dividir_seguro(1, 0) is None
