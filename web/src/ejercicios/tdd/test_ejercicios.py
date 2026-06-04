"""🧪 Tests — TDD: el test primero"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"tdd_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_es_palindromo():
    assert modulo.es_palindromo("oso") is True
    assert modulo.es_palindromo("gato") is False
    assert modulo.es_palindromo("ana") is True


def test_factorial():
    assert modulo.factorial(0) == 1
    assert modulo.factorial(1) == 1
    assert modulo.factorial(5) == 120


def test_contar_vocales():
    assert modulo.contar_vocales("pikachu") == 3
    assert modulo.contar_vocales("xyz") == 0
    assert modulo.contar_vocales("AEIOU") == 5
