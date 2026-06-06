"""🧪 Tests — Repartir tareas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_tareas_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_repartir():
    assert modulo.repartir([1, 2, 3, 4, 5], 2) == [[1, 3, 5], [2, 4]]
    assert modulo.repartir([1, 2, 3], 3) == [[1], [2], [3]]


def test_carga_de():
    assert modulo.carga_de([[1, 3, 5], [2, 4]]) == [3, 2]


def test_worker_libre():
    assert modulo.worker_libre([3, 1, 2]) == 1
    assert modulo.worker_libre([2, 2, 2]) == 0


def test_equilibrado():
    assert modulo.equilibrado([[1, 3], [2, 4]]) is True
    assert modulo.equilibrado([[1, 2, 3], [4]]) is False
