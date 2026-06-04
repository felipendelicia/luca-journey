"""🧪 Tests — Errores: try / except"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"tryexc_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_dividir_seguro():
    assert modulo.dividir_seguro(10, 2) == 5
    assert modulo.dividir_seguro(5, 0) is None


def test_a_entero():
    assert modulo.a_entero("42") == 42
    assert modulo.a_entero("pikachu") == 0


def test_elemento():
    assert modulo.elemento([10, 20, 30], 1) == 20
    assert modulo.elemento([10], 5) is None


def test_valor():
    assert modulo.valor({"nivel": 25}, "nivel") == 25
    assert modulo.valor({"nivel": 25}, "tipo") == "no encontrado"
