"""🧪 Tests — Juntar resultados (gather)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_gather_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_combinar():
    assert modulo.combinar([("pikachu", 100), ("onix", 80)]) == {"pikachu": 100, "onix": 80}
    assert modulo.combinar([]) == {}


def test_en_orden():
    assert modulo.en_orden(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def test_todos_ok():
    assert modulo.todos_ok([1, 2, 3]) is True
    assert modulo.todos_ok([1, None, 3]) is False


def test_primer_error():
    assert modulo.primer_error([1, None, 3]) == 1
    assert modulo.primer_error([1, 2]) == -1
