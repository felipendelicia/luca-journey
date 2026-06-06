import ejercicios


def test_push():
    assert ejercicios.push([1, 2], 3) == [1, 2, 3]


def test_pop():
    pila = [1, 2, 3]
    assert ejercicios.pop_(pila) == 3
    assert pila == [1, 2]
    assert ejercicios.pop_([]) is None


def test_ver():
    assert ejercicios.ver([1, 2, 3]) == 3
    assert ejercicios.ver([]) is None


def test_invertir():
    assert ejercicios.invertir([1, 2, 3]) == [3, 2, 1]
    assert ejercicios.invertir([]) == []
