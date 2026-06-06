"""🧪 Tests — Variables de entorno y config"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_entorno_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_parsear_env():
    assert modulo.parsear_env("API=abc\n# nota\nDEBUG=1") == {"API": "abc", "DEBUG": "1"}
    assert modulo.parsear_env("") == {}


def test_obtener():
    assert modulo.obtener({"A": "1"}, "A", "0") == "1"
    assert modulo.obtener({}, "A", "0") == "0"


def test_es_verdadero():
    assert modulo.es_verdadero("TRUE") is True
    assert modulo.es_verdadero("si") is True
    assert modulo.es_verdadero("no") is False


def test_leer_entorno():
    os.environ["POKE_TEST_VAR"] = "rojo"
    assert modulo.leer_entorno("POKE_TEST_VAR", "azul") == "rojo"
    assert modulo.leer_entorno("NO_EXISTE_XYZ", "azul") == "azul"
