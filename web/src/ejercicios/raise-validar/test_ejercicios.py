"""🧪 Tests — Lanzar errores: raise"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"raise_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_validar_edad():
    assert modulo.validar_edad(25) == 25
    with pytest.raises(ValueError):
        modulo.validar_edad(-1)


def test_validar_nivel():
    assert modulo.validar_nivel(50) == 50
    with pytest.raises(ValueError):
        modulo.validar_nivel(0)
    with pytest.raises(ValueError):
        modulo.validar_nivel(101)


def test_dividir():
    assert modulo.dividir(10, 2) == 5
    with pytest.raises(ValueError):
        modulo.dividir(5, 0)


def test_solo_texto():
    assert modulo.solo_texto("Pikachu") == "Pikachu"
    with pytest.raises(TypeError):
        modulo.solo_texto(123)
