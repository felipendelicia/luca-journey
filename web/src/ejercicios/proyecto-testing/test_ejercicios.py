"""🧪 Tests — Proyecto: módulo testeado"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"proytest_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_raiz_cuadrada():
    assert modulo.raiz_cuadrada(9) == 3
    assert modulo.raiz_cuadrada(0) == 0
    with pytest.raises(ValueError):
        modulo.raiz_cuadrada(-4)


def _raiz_ok(n):
    if n < 0:
        raise ValueError()
    return n ** 0.5


def test_probar_raiz():
    modulo.probar_raiz(_raiz_ok)
    # una raíz que NO valida negativos -> el test debe detectarlo
    with pytest.raises(AssertionError):
        modulo.probar_raiz(lambda n: abs(n) ** 0.5)


def test_dividir_seguro():
    assert modulo.dividir_seguro(6, 2) == 3
    assert modulo.dividir_seguro(1, 0) is None


def test_probar_dividir_seguro():
    modulo.probar_dividir_seguro(lambda a, b: (a / b) if b else None)
    with pytest.raises(AssertionError):
        modulo.probar_dividir_seguro(lambda a, b: 0)
