import ejercicios


def test_asignar():
    assert ejercicios.asignar(0, 3) == 0
    assert ejercicios.asignar(4, 3) == 1


def test_cargas():
    assert ejercicios.cargas(5, 2) == [3, 2]
    assert ejercicios.cargas(6, 3) == [2, 2, 2]


def test_mas_cargado():
    assert ejercicios.mas_cargado([2, 5, 3]) == 1
    assert ejercicios.mas_cargado([4, 4]) == 0


def test_balance():
    assert ejercicios.balance([2, 5, 3]) == 3
    assert ejercicios.balance([4, 4]) == 0
