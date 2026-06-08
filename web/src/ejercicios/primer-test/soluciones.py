"""✅ Soluciones — Tu primer test"""


def probar_doble(doble):
    assert doble(3) == 6
    assert doble(0) == 0
    assert doble(-2) == -4


def probar_es_par(es_par):
    assert es_par(2) is True
    assert es_par(3) is False
    assert es_par(0) is True


def probar_mayor(mayor):
    assert mayor(5, 3) == 5
    assert mayor(2, 8) == 8
    assert mayor(4, 4) == 4


def probar_triple(triple):
    assert triple(2) == 6
    assert triple(0) == 0
    assert triple(5) == 15


def probar_resta(resta):
    assert resta(5, 2) == 3
    assert resta(0, 0) == 0


def probar_es_impar(es_impar):
    assert es_impar(3) is True
    assert es_impar(4) is False


def probar_maximo(maximo):
    assert maximo(3, 8) == 8
    assert maximo(9, 1) == 9


def probar_minimo(minimo):
    assert minimo(3, 8) == 3
    assert minimo(9, 1) == 1


def probar_absoluto(absoluto):
    assert absoluto(5) == 5
    assert absoluto(-5) == 5


def probar_largo(largo):
    assert largo([1, 2, 3]) == 3
    assert largo([]) == 0


def probar_primero(primero):
    assert primero([10, 20, 30]) == 10


def probar_ultimo(ultimo):
    assert ultimo([10, 20, 30]) == 30


def probar_suma_lista(suma_lista):
    assert suma_lista([1, 2, 3]) == 6
    assert suma_lista([]) == 0


def probar_contiene(contiene):
    assert contiene([1, 2, 3], 2) is True
    assert contiene([1, 2, 3], 9) is False


def probar_invertir(invertir):
    assert invertir([1, 2, 3]) == [3, 2, 1]


def probar_mayusculas(mayusculas):
    assert mayusculas("pika") == "PIKA"


def probar_repetir(repetir):
    assert repetir("ab", 3) == "ababab"


def probar_promedio(promedio):
    assert promedio([2, 4, 6]) == 4.0


def probar_cuadrado(cuadrado):
    assert cuadrado(4) == 16
    assert cuadrado(0) == 0


def probar_es_vocal(es_vocal):
    assert es_vocal("a") is True
    assert es_vocal("z") is False
