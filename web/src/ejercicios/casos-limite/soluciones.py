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


def probar_division_segura(div):
    assert div(10, 2) == 5
    assert div(5, 0) is None


def probar_primero_seguro(primero):
    assert primero([10, 20]) == 10
    assert primero([]) is None


def probar_ultimo_seguro(ultimo):
    assert ultimo([10, 20]) == 20
    assert ultimo([]) is None


def probar_promedio_seguro(promedio):
    assert promedio([2, 4]) == 3
    assert promedio([]) == 0


def probar_maximo_seguro(maximo):
    assert maximo([3, 1]) == 3
    assert maximo([]) is None


def probar_es_vacio(es_vacio):
    assert es_vacio([]) is True
    assert es_vacio([1]) is False


def probar_clamp(clamp):
    assert clamp(5, 0, 10) == 5
    assert clamp(-3, 0, 10) == 0
    assert clamp(20, 0, 10) == 10


def probar_signo(signo):
    assert signo(0) == 0
    assert signo(5) == 1
    assert signo(-3) == -1


def probar_porcentaje(porcentaje):
    assert porcentaje(1, 4) == 25
    assert porcentaje(5, 0) == 0


def probar_indice_seguro(en):
    assert en([10, 20], 1) == 20
    assert en([10], 5) is None


def probar_contar_vocales(contar):
    assert contar("aei") == 3
    assert contar("xyz") == 0


def probar_recortar(recortar):
    assert recortar("pikachu", 4) == "pika"
    assert recortar("pi", 10) == "pi"


def probar_quitar_negativos(quitar):
    assert quitar([-1, 0, 2]) == [0, 2]
    assert quitar([-1, -2]) == []


def probar_primera_palabra(primera):
    assert primera("hola mundo") == "hola"
    assert primera("") == ""


def probar_minimo_seguro(minimo):
    assert minimo([3, 1]) == 1
    assert minimo([]) is None


def probar_dividir_lista(dividir):
    assert dividir([10, 20], 2) == [5, 10]
    assert dividir([10], 0) is None


def probar_es_positivo(es_positivo):
    assert es_positivo(5) is True
    assert es_positivo(0) is False
    assert es_positivo(-2) is False
