"""🧪 Tests — SQL: filtrar y ordenar"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlselect_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Pikachu", 25, "Electrico"),
        ("Charizard", 90, "Fuego"),
        ("Bulbasaur", 12, "Planta"),
        ("Charmander", 40, "Fuego"),
        ("Snorlax", 70, "Normal"),
    ])
    return c


def test_de_tipo():
    assert sorted(modulo.de_tipo(_db(), "Fuego")) == ["Charizard", "Charmander"]


def test_fuertes():
    assert modulo.fuertes(_db(), 50) == ["Charizard", "Snorlax"]


def test_ordenados_por_nivel():
    assert modulo.ordenados_por_nivel(_db()) == ["Charizard", "Snorlax", "Charmander", "Pikachu", "Bulbasaur"]


def test_empiezan_con():
    assert sorted(modulo.empiezan_con(_db(), "C")) == ["Charizard", "Charmander"]


def test_top():
    assert modulo.top(_db(), 2) == ["Charizard", "Snorlax"]
