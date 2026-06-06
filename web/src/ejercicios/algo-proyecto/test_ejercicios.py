"""🧪 Tests — Algoritmos sobre la Pokédex"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_proyecto_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_contar_tipos():
    assert modulo.contar_tipos([{"nombre": "a", "tipo": "agua"}, {"nombre": "b", "tipo": "agua"}]) == {"agua": 2}


def test_ordenar_por_nivel():
    r = modulo.ordenar_por_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}])
    assert r == [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]


def test_buscar():
    assert modulo.buscar([{"nombre": "Pikachu"}], "Pikachu") == {"nombre": "Pikachu"}
    assert modulo.buscar([{"nombre": "Pikachu"}], "Onix") is None


def test_top_n():
    pokes = [{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}, {"nombre": "c", "nivel": 12}]
    assert modulo.top_n(pokes, 2) == ["b", "c"]
