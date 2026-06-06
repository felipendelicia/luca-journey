import ejercicios


def test_bloques():
    assert ejercicios.bloques([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]
    assert ejercicios.bloques([1, 2, 3, 4, 5, 6], 3) == [[1, 2], [3, 4], [5, 6]]


def test_tam_max():
    assert ejercicios.tam_max(10, 3) == 4
    assert ejercicios.tam_max(9, 3) == 3


def test_unir():
    assert ejercicios.unir([[1, 2], [3]]) == [1, 2, 3]


def test_cabe():
    assert ejercicios.cabe_todo(10, 3, 4) is True
    assert ejercicios.cabe_todo(10, 2, 4) is False
