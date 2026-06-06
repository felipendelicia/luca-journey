import ejercicios


def test_preparar():
    assert ejercicios.preparar(["a", "b"]) == [{"url": "a", "ok": False}, {"url": "b", "ok": False}]


def test_planificar():
    assert ejercicios.planificar([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_ejecutar_lote():
    assert ejercicios.ejecutar_lote([{"url": "a", "ok": False}]) == [{"url": "a", "ok": True}]


def test_correr():
    assert ejercicios.correr(["a", "b", "c"], 2) == "3 descargas en 2 lotes."
    assert ejercicios.correr(["a"], 5) == "1 descargas en 1 lotes."
