"""🧪 Tests — Proyecto: Pokédex en SQLite"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"proydb_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Pikachu", "Electrico", 25),
        ("Charizard", "Fuego", 90),
        ("Vulpix", "Fuego", 18),
    ])
    return c


def test_crear_pokedex():
    c = modulo.crear_pokedex()
    c.execute("INSERT INTO pokemon VALUES ('X', 'Fuego', 1)")
    assert c.execute("SELECT tipo FROM pokemon").fetchone()[0] == "Fuego"


def test_agregar():
    c = _db()
    modulo.agregar(c, "Mew", "Psiquico", 70)
    assert c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0] == 4


def test_listar():
    assert modulo.listar(_db()) == ["Charizard", "Pikachu", "Vulpix"]


def test_por_tipo():
    assert sorted(modulo.por_tipo(_db(), "Fuego")) == ["Charizard", "Vulpix"]


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(_db()) == "Charizard"


def test_cuantos_por_tipo():
    assert modulo.cuantos_por_tipo(_db()) == {"Electrico": 1, "Fuego": 2}
