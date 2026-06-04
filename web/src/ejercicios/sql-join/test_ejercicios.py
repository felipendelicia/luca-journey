"""🧪 Tests — SQL: relaciones y JOIN"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqljoin_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT)")
    c.execute("CREATE TABLE tipos (tipo TEXT, debilidad TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?)", [
        ("Charizard", "Fuego"), ("Blastoise", "Agua"), ("Vulpix", "Fuego"),
    ])
    c.executemany("INSERT INTO tipos VALUES (?, ?)", [
        ("Fuego", "Agua"), ("Agua", "Planta"),
    ])
    return c


def test_con_debilidad():
    r = modulo.con_debilidad(_db())
    assert ("Charizard", "Agua") in r
    assert ("Blastoise", "Planta") in r
    assert len(r) == 3


def test_debilidad_de():
    assert modulo.debilidad_de(_db(), "Charizard") == "Agua"
    assert modulo.debilidad_de(_db(), "Blastoise") == "Planta"


def test_debiles_a():
    assert sorted(modulo.debiles_a(_db(), "Agua")) == ["Charizard", "Vulpix"]
