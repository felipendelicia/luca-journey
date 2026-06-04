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
