"""🧪 Tests — Límite de concurrencia"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_limite_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_por_lotes():
    assert modulo.por_lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert modulo.por_lotes([], 2) == []


def test_cantidad_lotes():
    assert modulo.cantidad_lotes(5, 2) == 3
    assert modulo.cantidad_lotes(4, 2) == 2


def test_cabe():
    assert modulo.cabe(2, 3) is True
    assert modulo.cabe(3, 3) is False


def test_limitar():
    assert modulo.limitar([1, 2, 3, 4], 2) == [1, 2]
    assert modulo.limitar([1], 5) == [1]
