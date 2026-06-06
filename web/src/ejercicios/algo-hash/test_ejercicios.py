"""🧪 Tests — Diccionarios y sets"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_hash_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_frecuencias():
    assert modulo.frecuencias(["a", "b", "a", "c", "a"]) == {"a": 3, "b": 1, "c": 1}
    assert modulo.frecuencias([]) == {}


def test_sin_duplicados():
    assert modulo.sin_duplicados([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_mas_comun():
    assert modulo.mas_comun(["a", "b", "a", "c"]) == "a"


def test_interseccion():
    assert modulo.interseccion([1, 2, 3, 4], [2, 4, 6]) == [2, 4]
    assert modulo.interseccion([1], [2]) == []
