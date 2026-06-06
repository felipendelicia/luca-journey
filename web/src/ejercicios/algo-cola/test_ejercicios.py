"""🧪 Tests — Cola (queue)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_cola_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_encolar():
    assert modulo.encolar([1, 2], 3) == [1, 2, 3]


def test_atender():
    cola = [1, 2, 3]
    assert modulo.atender(cola) == 1
    assert cola == [2, 3]
    assert modulo.atender([]) is None


def test_en_espera():
    assert modulo.en_espera([1, 2, 3]) == 3
    assert modulo.en_espera([]) == 0


def test_orden_de_atencion():
    cola = [1, 2, 3]
    assert modulo.orden_de_atencion(cola) == [1, 2, 3]
    assert cola == [1, 2, 3]
