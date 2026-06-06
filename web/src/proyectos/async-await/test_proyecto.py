import ejercicios


def test_con_await():
    assert ejercicios.con_await(["bajar()", "sumar()"], [True, False]) == ["await bajar()", "sumar()"]


def test_cuantas():
    assert ejercicios.cuantas_esperan([True, False, True]) == 2
    assert ejercicios.cuantas_esperan([]) == 0


def test_todas():
    assert ejercicios.todas_esperan([True, True]) is True
    assert ejercicios.todas_esperan([]) is False
    assert ejercicios.todas_esperan([True, False]) is False


def test_primera():
    assert ejercicios.primera_espera([False, True, True]) == 1
    assert ejercicios.primera_espera([False]) == -1
