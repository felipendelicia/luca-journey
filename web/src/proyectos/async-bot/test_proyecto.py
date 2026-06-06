import ejercicios


def test_crear():
    assert ejercicios.crear(["a"]) == [{"url": "a", "ok": False}]


def test_lotes():
    assert ejercicios.en_lotes([1, 2, 3], 2) == [[1, 2], [3]]


def test_completar():
    assert ejercicios.completar([{"url": "a", "ok": False}]) == [{"url": "a", "ok": True}]


def test_informe():
    assert ejercicios.informe([{"ok": True}, {"ok": False}]) == "1/2 descargadas."
    assert ejercicios.informe([{"ok": True}, {"ok": True}]) == "2/2 descargadas."
