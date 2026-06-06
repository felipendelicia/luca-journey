"""🧪 Tests — Corrutinas (async def)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_corrutinas_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


async def descargar():
    return 1


async def subir():
    return 2


def sumar():
    return 3


def test_es_corrutina():
    assert modulo.es_corrutina(descargar) is True
    assert modulo.es_corrutina(sumar) is False


def test_contar_corrutinas():
    assert modulo.contar_corrutinas([descargar, sumar, subir]) == 2
    assert modulo.contar_corrutinas([sumar]) == 0


def test_nombres_corrutinas():
    assert modulo.nombres_corrutinas([descargar, sumar, subir]) == ["descargar", "subir"]


def test_firma():
    assert modulo.firma("descargar", True) == "async def descargar():"
    assert modulo.firma("sumar", False) == "def sumar():"
