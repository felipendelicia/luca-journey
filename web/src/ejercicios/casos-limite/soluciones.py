"""✅ Soluciones — Casos límite y errores"""


def probar_largo(largo):
    assert largo("hola") == 4
    assert largo("") == 0
    assert largo("a") == 1


def probar_suma_lista(suma_lista):
    assert suma_lista([1, 2, 3]) == 6
    assert suma_lista([]) == 0
    assert suma_lista([7]) == 7


def probar_dividir(dividir):
    assert dividir(10, 2) == 5
    try:
        dividir(5, 0)
    except ZeroDivisionError:
        return
    raise AssertionError("dividir(5, 0) debería lanzar ZeroDivisionError")
