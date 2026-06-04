"""🧪 Tests — SQL: leer datos"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlintro_{nombre}", ruta)
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
    ])
    return c


def test_todos():
    assert modulo.todos(_db()) == ["Pikachu", "Charizard", "Bulbasaur"]


def test_cuantos():
    assert modulo.cuantos(_db()) == 3


def test_niveles():
    assert modulo.niveles(_db()) == [25, 90, 12]


def test_nombres_y_niveles():
    assert modulo.nombres_y_niveles(_db()) == [("Pikachu", 25), ("Charizard", 90), ("Bulbasaur", 12)]


def test_primero():
    assert modulo.primero(_db()) == "Pikachu"
