import ejercicios


def test_agregar():
    assert ejercicios.agregar_arista({}, "a", "b") == {"a": ["b"]}
    g = {"a": ["b"]}
    assert ejercicios.agregar_arista(g, "a", "c") == {"a": ["b", "c"]}


def test_vecinos():
    assert ejercicios.vecinos({"a": ["b"]}, "a") == ["b"]
    assert ejercicios.vecinos({"a": ["b"]}, "z") == []


def test_es_vecino():
    assert ejercicios.es_vecino({"a": ["b"]}, "a", "b") is True
    assert ejercicios.es_vecino({"a": ["b"]}, "a", "z") is False


def test_total():
    assert ejercicios.total_aristas({"a": ["b", "c"], "b": ["a"]}) == 3
