"""🧪 Tests — SQL: actualizar y borrar"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlupd_{nombre}", ruta)
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


def _nivel(c, nombre):
    return c.execute("SELECT nivel FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()[0]


def _nombres(c):
    return [f[0] for f in c.execute("SELECT nombre FROM pokemon ORDER BY nombre")]


def test_cambiar_nivel():
    c = _db()
    modulo.cambiar_nivel(c, "Pikachu", 50)
    assert _nivel(c, "Pikachu") == 50


def test_subir_todos():
    c = _db()
    modulo.subir_todos(c, 5)
    assert _nivel(c, "Pikachu") == 30 and _nivel(c, "Charizard") == 95


def test_borrar():
    c = _db()
    modulo.borrar(c, "Bulbasaur")
    assert _nombres(c) == ["Charizard", "Pikachu"]


def test_borrar_debiles():
    c = _db()
    modulo.borrar_debiles(c, 20)
    assert _nombres(c) == ["Charizard", "Pikachu"]
