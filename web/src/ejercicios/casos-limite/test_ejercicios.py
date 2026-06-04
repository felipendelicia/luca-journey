"""🧪 Tests — Casos límite y errores"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"casoslim_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_probar_largo():
    modulo.probar_largo(lambda t: len(t))
    # función que olvida el caso vacío (devuelve 1 para "")
    with pytest.raises(AssertionError):
        modulo.probar_largo(lambda t: len(t) if t else 1)


def test_probar_suma_lista():
    modulo.probar_suma_lista(lambda nums: sum(nums))
    with pytest.raises(AssertionError):
        modulo.probar_suma_lista(lambda nums: 99)


def test_probar_dividir():
    modulo.probar_dividir(lambda a, b: a / b)
    # una división que NO lanza con 0 (devuelve 0) -> el test debe detectarlo
    with pytest.raises(AssertionError):
        modulo.probar_dividir(lambda a, b: 0)
