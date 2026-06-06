import ejercicios


def test_min_indice():
    assert ejercicios.min_indice([30, 10, 20]) == 1
    assert ejercicios.min_indice([5]) == 0


def test_intercambiar():
    assert ejercicios.intercambiar([1, 2, 3], 0, 2) == [3, 2, 1]


def test_burbuja():
    assert ejercicios.burbuja([3, 1, 2]) == [1, 2, 3]
    assert ejercicios.burbuja([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_ordenada():
    assert ejercicios.ordenada([1, 2, 3]) is True
    assert ejercicios.ordenada([2, 1]) is False
