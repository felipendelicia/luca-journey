"""🧪 Tests — assert: afirmaciones"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"assert_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_verificar_positivo():
    assert modulo.verificar_positivo(5) == 5
    with pytest.raises(AssertionError):
        modulo.verificar_positivo(-2)


def test_verificar_nivel():
    assert modulo.verificar_nivel(50) == 50
    with pytest.raises(AssertionError):
        modulo.verificar_nivel(0)


def test_promedio():
    assert modulo.promedio([10, 20, 30]) == 20
    with pytest.raises(AssertionError):
        modulo.promedio([])
