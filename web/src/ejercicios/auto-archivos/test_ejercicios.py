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
