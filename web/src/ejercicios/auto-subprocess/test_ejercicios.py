"""🧪 Tests — Ejecutar programas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_subprocess_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_armar_comando():
    assert modulo.armar_comando("git", {"--depth": 1}) == ["git", "--depth", "1"]
    assert modulo.armar_comando("ls", {}) == ["ls"]


def test_parsear_salida():
    assert modulo.parsear_salida("uno\n\n  dos  \n") == ["uno", "dos"]
    assert modulo.parsear_salida("") == []


def test_contar_lineas():
    assert modulo.contar_lineas("a\n\nb\n") == 2
    assert modulo.contar_lineas("") == 0


def test_estado():
    assert modulo.estado({"returncode": 0}) == "ok"
    assert modulo.estado({"returncode": 1}) == "error"
