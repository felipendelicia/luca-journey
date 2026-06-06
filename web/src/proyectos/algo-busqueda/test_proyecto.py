import ejercicios


def test_indice():
    assert ejercicios.indice_de([10, 20, 30], 30) == 2
    assert ejercicios.indice_de([10], 99) == -1


def test_esta():
    assert ejercicios.esta([1, 2], 2) is True
    assert ejercicios.esta([1, 2], 9) is False


def test_binaria():
    assert ejercicios.binaria([1, 3, 5, 7], 5) == 2
    assert ejercicios.binaria([1, 3, 5], 4) == -1


def test_menores():
    assert ejercicios.cuantos_menores([1, 3, 5, 7], 5) == 2
    assert ejercicios.cuantos_menores([1, 2], 0) == 0
