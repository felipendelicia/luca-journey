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


def clasificar_nivel(n):
    if n < 30:
        return "bajo"
    if n < 70:
        return "medio"
    return "alto"


def probar_clasificar_nivel(f):
    assert f(10) == "bajo"
    assert f(50) == "medio"
    assert f(90) == "alto"


def iniciales(nombre):
    return "".join(p[0].upper() for p in nombre.split())


def probar_iniciales(f):
    assert f("ash ketchum") == "AK"


def contar_mayuscula(texto):
    return sum(1 for c in texto if c.isupper())


def probar_contar_mayuscula(f):
    assert f("PiKa") == 2


def es_multiplo(n, m):
    return n % m == 0


def probar_es_multiplo(f):
    assert f(10, 5) is True
    assert f(10, 3) is False


def distancia(a, b):
    return abs(a - b)


def probar_distancia(f):
    assert f(3, 8) == 5
    assert f(8, 3) == 5


def juntar(lista, sep):
    return sep.join(lista)


def probar_juntar(f):
    assert f(["a", "b"], "-") == "a-b"


def limite(n, maximo):
    return min(n, maximo)


def probar_limite(f):
    assert f(5, 10) == 5
    assert f(20, 10) == 10


def repetir_lista(lista, n):
    return lista * n


def probar_repetir_lista(f):
    assert f([1, 2], 2) == [1, 2, 1, 2]
