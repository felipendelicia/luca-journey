"""🧪 Tests — Tu primer test"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"primertest_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_probar_doble():
    # con una función correcta NO debe lanzar
    modulo.probar_doble(lambda x: x * 2)
    # con una función ROTA debe detectar el bug (AssertionError)
    with pytest.raises(AssertionError):
        modulo.probar_doble(lambda x: x + 2)


def test_probar_es_par():
    modulo.probar_es_par(lambda x: x % 2 == 0)
    with pytest.raises(AssertionError):
        modulo.probar_es_par(lambda x: True)


def test_probar_mayor():
    modulo.probar_mayor(lambda a, b: a if a >= b else b)
    with pytest.raises(AssertionError):
        modulo.probar_mayor(lambda a, b: a)
