import ejercicios


def test_juntar():
    assert ejercicios.juntar([("a", 1), ("b", 2)]) == {"a": 1, "b": 2}


def test_ok():
    assert ejercicios.valores_ok([1, None, 3]) == [1, 3]


def test_fallaron():
    assert ejercicios.cuantos_fallaron([1, None, None]) == 2


def test_tasa():
    assert ejercicios.tasa([1, None, 3, 4]) == 75
    assert ejercicios.tasa([]) == 0
