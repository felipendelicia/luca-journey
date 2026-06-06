import ejercicios


def test_carpeta():
    assert ejercicios.carpeta_de("descargas/fotos/pikachu.png") == "descargas/fotos"
    assert ejercicios.carpeta_de("raiz.txt") == "."


def test_prefijo():
    assert ejercicios.con_prefijo("pikachu.png", "2024_") == "2024_pikachu.png"


def test_destino():
    assert ejercicios.ruta_destino("orden/imagenes", "pikachu.png") == "orden/imagenes/pikachu.png"


def test_organizar():
    assert ejercicios.organizar(["a/x.png", "b/y.txt", "c/z.png"]) == {".png": ["x.png", "z.png"], ".txt": ["y.txt"]}
    assert ejercicios.organizar([]) == {}
