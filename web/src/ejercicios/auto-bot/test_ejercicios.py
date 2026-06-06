"""🧪 Tests — Automatizador (bot)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_bot_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_normalizar():
    assert modulo.normalizar("  Pikachu ") == "pikachu"


def test_filtrar_nivel():
    pokes = [{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}]
    assert modulo.filtrar_nivel(pokes, 10) == [{"nombre": "b", "nivel": 20}]
    assert modulo.filtrar_nivel(pokes, 100) == []


def test_agrupar_por_tipo():
    pokes = [{"nombre": "Squirtle", "tipo": "agua"}, {"nombre": "Charmander", "tipo": "fuego"}, {"nombre": "Psyduck", "tipo": "agua"}]
    assert modulo.agrupar_por_tipo(pokes) == {"agua": ["Squirtle", "Psyduck"], "fuego": ["Charmander"]}


def test_contar():
    assert modulo.contar([{"nombre": "a"}, {"nombre": "b"}]) == 2
    assert modulo.contar([]) == 0
