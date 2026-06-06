import ejercicios


def test_encolar():
    assert ejercicios.encolar([1, 2], 3) == [1, 2, 3]


def test_atender():
    cola = [1, 2, 3]
    assert ejercicios.atender(cola) == 1
    assert cola == [2, 3]
    assert ejercicios.atender([]) is None


def test_largo():
    assert ejercicios.largo([1, 2, 3]) == 3


def test_turnos():
    cola = [1, 2, 3]
    assert ejercicios.turnos(cola) == [1, 2, 3]
    assert cola == [1, 2, 3]
