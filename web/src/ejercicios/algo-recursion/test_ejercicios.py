"""🧪 Tests — Recursión"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_recursion_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_factorial():
    assert modulo.factorial(5) == 120
    assert modulo.factorial(0) == 1


def test_suma_hasta():
    assert modulo.suma_hasta(4) == 10
    assert modulo.suma_hasta(0) == 0


def test_fibonacci():
    assert modulo.fibonacci(6) == 8
    assert modulo.fibonacci(0) == 0
    assert modulo.fibonacci(1) == 1


def test_potencia():
    assert modulo.potencia(2, 5) == 32
    assert modulo.potencia(7, 0) == 1
