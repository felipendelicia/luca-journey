"""🧪 Tests — Archivos y rutas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_archivos_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_nombre_archivo():
    assert modulo.nombre_archivo("datos/pokedex/kanto.csv") == "kanto.csv"
    assert modulo.nombre_archivo("solo.txt") == "solo.txt"


def test_extension():
    assert modulo.extension("kanto.csv") == ".csv"
    assert modulo.extension("LEEME") == ""


def test_cambiar_extension():
    assert modulo.cambiar_extension("kanto.csv", ".json") == "kanto.json"
    assert modulo.cambiar_extension("datos/kanto.csv", ".txt") == "datos/kanto.txt"


def test_guardar_y_leer():
    assert modulo.guardar_y_leer("nota_test.txt", "hola") == "hola"
    assert modulo.guardar_y_leer("nota_test.txt", "Pikachu") == "Pikachu"


def test_directorio():
    assert modulo.directorio("/home/ash/pokedex.txt") == "/home/ash"


def test_sin_extension():
    assert modulo.sin_extension("/home/ash/pokedex.txt") == "/home/ash/pokedex"


def test_unir():
    assert modulo.unir("/home/ash", "pokedex.txt") == "/home/ash/pokedex.txt"


def test_es_absoluta():
    assert modulo.es_absoluta("/home/x") is True
    assert modulo.es_absoluta("home/x") is False


def test_partes():
    assert modulo.partes("home/ash/x.txt") == ["home", "ash", "x.txt"]


def test_nombre_sin_ext():
    assert modulo.nombre_sin_ext("/home/ash/pokedex.txt") == "pokedex"


def test_tiene_extension():
    assert modulo.tiene_extension("a.json", ".json") is True
    assert modulo.tiene_extension("a.txt", ".json") is False


def test_cambiar_carpeta():
    assert modulo.cambiar_carpeta("/viejo/x.txt", "/nuevo") == "/nuevo/x.txt"


def test_normalizar_barras():
    assert modulo.normalizar_barras("home\\ash\\x.txt") == "home/ash/x.txt"


def test_agregar_sufijo():
    assert modulo.agregar_sufijo("foto.png", "_chica") == "foto_chica.png"


def test_es_oculto():
    assert modulo.es_oculto("/home/ash/.config") is True
    assert modulo.es_oculto("/home/ash/x.txt") is False


def test_mismo_directorio():
    assert modulo.mismo_directorio("/a/x.txt", "/a/y.txt") is True
    assert modulo.mismo_directorio("/a/x.txt", "/b/y.txt") is False


def test_extension_minuscula():
    assert modulo.extension_minuscula("FOTO.PNG") == ".png"


def test_contar_niveles():
    assert modulo.contar_niveles("/home/ash/x.txt") == 3


def test_quitar_barra_final():
    assert modulo.quitar_barra_final("/home/ash/") == "/home/ash"


def test_es_tipo():
    assert modulo.es_tipo("a.png", [".png", ".jpg"]) is True
    assert modulo.es_tipo("a.gif", [".png", ".jpg"]) is False
