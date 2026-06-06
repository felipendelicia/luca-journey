"""🧪 Tests — Búsqueda lineal y binaria"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_busqueda_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_busqueda_lineal():
    assert modulo.busqueda_lineal([10, 20, 30], 20) == 1
    assert modulo.busqueda_lineal([10], 99) == -1


def test_contiene():
    assert modulo.contiene([1, 2, 3], 2) is True
    assert modulo.contiene([1, 2, 3], 9) is False


def test_busqueda_binaria():
    assert modulo.busqueda_binaria([1, 3, 5, 7, 9], 7) == 3
    assert modulo.busqueda_binaria([1, 3, 5], 4) == -1
    assert modulo.busqueda_binaria([], 1) == -1


def test_primero_mayor():
    assert modulo.primero_mayor([1, 3, 5, 7], 4) == 5
    assert modulo.primero_mayor([1, 2], 9) is None
