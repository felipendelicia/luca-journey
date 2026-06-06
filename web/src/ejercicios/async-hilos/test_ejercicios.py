"""🧪 Tests — Dividir trabajo (hilos)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_hilos_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_dividir():
    assert modulo.dividir([1, 2, 3, 4, 5, 6], 3) == [[1, 2], [3, 4], [5, 6]]
    assert modulo.dividir([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]


def test_tamano_chunk():
    assert modulo.tamano_chunk(10, 3) == 4
    assert modulo.tamano_chunk(9, 3) == 3


def test_cuantos_hilos():
    assert modulo.cuantos_hilos(10, 4) == 3
    assert modulo.cuantos_hilos(8, 4) == 2


def test_aplanar():
    assert modulo.aplanar([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]
