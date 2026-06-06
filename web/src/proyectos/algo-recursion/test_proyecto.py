import ejercicios


def test_suma():
    assert ejercicios.suma_lista([1, 2, 3]) == 6
    assert ejercicios.suma_lista([]) == 0


def test_cuenta():
    assert ejercicios.cuenta_atras(3) == [3, 2, 1]
    assert ejercicios.cuenta_atras(0) == []


def test_longitud():
    assert ejercicios.longitud([1, 2, 3]) == 3
    assert ejercicios.longitud([]) == 0


def test_invertir():
    assert ejercicios.invertir_texto("pika") == "akip"
    assert ejercicios.invertir_texto("") == ""
