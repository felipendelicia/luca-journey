"""🧪 Tests — Cola productor/consumidor"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_cola_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_encolar():
    assert modulo.encolar([1, 2], 3) == [1, 2, 3]
    assert modulo.encolar([], "a") == ["a"]


def test_desencolar():
    cola = [1, 2, 3]
    assert modulo.desencolar(cola) == 1
    assert cola == [2, 3]
    assert modulo.desencolar([]) is None


def test_siguiente():
    assert modulo.siguiente([1, 2, 3]) == 1
    assert modulo.siguiente([]) is None


def test_vaciar():
    cola = [1, 2, 3]
    assert modulo.vaciar(cola) == [1, 2, 3]
    assert cola == []
