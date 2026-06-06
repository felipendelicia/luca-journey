import ejercicios


def test_lotes():
    assert ejercicios.lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_nro():
    assert ejercicios.nro_lotes(5, 2) == 3
    assert ejercicios.nro_lotes(4, 2) == 2


def test_disponible():
    assert ejercicios.disponible(2, 5) == 3
    assert ejercicios.disponible(5, 5) == 0


def test_recortar():
    assert ejercicios.recortar([1, 2, 3, 4], 2) == [1, 2]
    assert ejercicios.recortar([1], 5) == [1]
