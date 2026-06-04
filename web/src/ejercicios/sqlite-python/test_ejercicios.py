"""🧪 Tests — SQLite desde Python"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlitepy_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_crear_conexion():
    c = modulo.crear_conexion()
    c.execute("INSERT INTO pokemon VALUES ('Pikachu', 25)")
    assert c.execute("SELECT nivel FROM pokemon").fetchone()[0] == 25


def test_guardar():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    modulo.guardar(c, "Charizard", 90)
    assert c.execute("SELECT nombre FROM pokemon").fetchall() == [("Charizard",)]


def test_cantidad():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?)", [("A", 1), ("B", 2), ("C", 3)])
    assert modulo.cantidad(c) == 3


def test_buscar():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    c.execute("INSERT INTO pokemon VALUES ('Eevee', 15)")
    assert modulo.buscar(c, "Eevee") == ("Eevee", 15)
    assert modulo.buscar(c, "Mew") is None
