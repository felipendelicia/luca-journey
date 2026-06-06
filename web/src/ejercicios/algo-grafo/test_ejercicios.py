"""🧪 Tests — Grafos"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_grafo_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

G = {"a": ["b", "c"], "b": ["a"], "c": ["a"]}


def test_vecinos():
    assert modulo.vecinos(G, "a") == ["b", "c"]
    assert modulo.vecinos(G, "z") == []


def test_grado():
    assert modulo.grado(G, "a") == 2
    assert modulo.grado(G, "b") == 1


def test_hay_arista():
    assert modulo.hay_arista(G, "a", "b") is True
    assert modulo.hay_arista(G, "b", "c") is False


def test_nodos():
    assert modulo.nodos({"c": [], "a": [], "b": []}) == ["a", "b", "c"]
