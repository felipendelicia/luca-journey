import ejercicios


def test_contar():
    assert ejercicios.contar(["a", "b", "a"]) == {"a": 2, "b": 1}


def test_unicos():
    assert ejercicios.unicos([3, 1, 3, 2]) == [3, 1, 2]


def test_repetidos():
    assert ejercicios.repetidos([1, 2, 2, 3, 3, 3]) == [2, 3]
    assert ejercicios.repetidos([1, 2, 3]) == []


def test_comunes():
    assert ejercicios.comunes([1, 2, 3], [2, 3, 4]) == [2, 3]
    assert ejercicios.comunes([1], [2]) == []
