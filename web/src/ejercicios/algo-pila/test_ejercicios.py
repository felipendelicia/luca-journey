"""🧪 Tests — Pila (stack)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_pila_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_apilar():
    assert modulo.apilar([1, 2], 3) == [1, 2, 3]


def test_desapilar():
    pila = [1, 2, 3]
    assert modulo.desapilar(pila) == 3
    assert pila == [1, 2]
    assert modulo.desapilar([]) is None


def test_tope():
    assert modulo.tope([1, 2, 3]) == 3
    assert modulo.tope([]) is None


def test_balanceado():
    assert modulo.balanceado("(a(b)c)") is True
    assert modulo.balanceado("(a(b)") is False
    assert modulo.balanceado(")(") is False
