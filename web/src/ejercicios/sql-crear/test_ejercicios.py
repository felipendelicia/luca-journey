"""🧪 Tests — SQL: crear e insertar"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlcrear_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _con_tabla():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE entrenadores (nombre TEXT, medallas INTEGER)")
    return c


def test_crear_tabla():
    c = sqlite3.connect(":memory:")
    modulo.crear_tabla(c)
    c.execute("INSERT INTO entrenadores VALUES ('Ash', 8)")
    assert c.execute("SELECT medallas FROM entrenadores").fetchone()[0] == 8


def test_insertar():
    c = _con_tabla()
    modulo.insertar(c, "Ash", 8)
    assert c.execute("SELECT * FROM entrenadores").fetchall() == [("Ash", 8)]


def test_insertar_varios():
    c = _con_tabla()
    modulo.insertar_varios(c, [("Ash", 8), ("Gary", 5), ("Misty", 3)])
    assert c.execute("SELECT COUNT(*) FROM entrenadores").fetchone()[0] == 3
    assert c.execute("SELECT nombre FROM entrenadores WHERE medallas = 5").fetchone()[0] == "Gary"


def test_crear_pokedex():
    c = sqlite3.connect(":memory:")
    modulo.crear_pokedex(c)
    assert c.execute("SELECT nombre, nivel FROM pokemon").fetchall() == [("Pikachu", 25)]
