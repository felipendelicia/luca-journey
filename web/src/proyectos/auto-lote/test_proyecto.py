import ejercicios


def test_es_imagen():
    assert ejercicios.es_imagen("pikachu.PNG") is True
    assert ejercicios.es_imagen("foto.jpg") is True
    assert ejercicios.es_imagen("notas.txt") is False


def test_total():
    assert ejercicios.total_tamano([("a", 10), ("b", 5)]) == 15
    assert ejercicios.total_tamano([]) == 0


def test_grandes():
    assert ejercicios.filtrar_grandes([("a", 10), ("b", 100), ("c", 50)], 50) == ["b", "c"]


def test_resumen():
    assert ejercicios.resumen_carpeta([("a", 10), ("b", 5)]) == "2 archivos, 15 bytes en total."
    assert ejercicios.resumen_carpeta([]) == "0 archivos, 0 bytes en total."
