import ejercicios


def test_primero_seguro():
    assert ejercicios.primero_seguro([10, 20, 30]) == 10
    assert ejercicios.primero_seguro(["pikachu"]) == "pikachu"
    assert ejercicios.primero_seguro([]) is None


def test_maximo_seguro():
    assert ejercicios.maximo_seguro([3, 1, 4, 1, 5]) == 5
    assert ejercicios.maximo_seguro([7]) == 7
    assert ejercicios.maximo_seguro([]) is None


def test_longitud_segura():
    assert ejercicios.longitud_segura([1, 2, 3]) == 3
    assert ejercicios.longitud_segura("pikachu") == 7
    assert ejercicios.longitud_segura([]) == 0
    assert ejercicios.longitud_segura(None) == 0
    assert ejercicios.longitud_segura(42) == 0


def test_nivel_promedio():
    assert ejercicios.nivel_promedio([{"nivel": 10}, {"nivel": 20}]) == 15.0
    assert ejercicios.nivel_promedio([{"nivel": 5}, {"nombre": "raro"}]) == 5.0
    assert ejercicios.nivel_promedio([]) == 0
    assert ejercicios.nivel_promedio(None) == 0
    assert ejercicios.nivel_promedio([{"nombre": "sin_nivel"}]) == 0
