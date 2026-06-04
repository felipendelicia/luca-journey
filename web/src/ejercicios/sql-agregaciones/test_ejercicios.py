"""🧪 Tests — SQL: agregaciones y GROUP BY"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlagg_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Pikachu", 20, "Electrico"),
        ("Raichu", 40, "Electrico"),
        ("Charizard", 90, "Fuego"),
        ("Bulbasaur", 10, "Planta"),
    ])
    return c


def test_total():
    assert modulo.total(_db()) == 4


def test_nivel_promedio():
    assert modulo.nivel_promedio(_db()) == (20 + 40 + 90 + 10) / 4


def test_nivel_maximo():
    assert modulo.nivel_maximo(_db()) == 90


def test_suma_niveles():
    assert modulo.suma_niveles(_db()) == 160


def test_cuantos_por_tipo():
    assert modulo.cuantos_por_tipo(_db()) == {"Electrico": 2, "Fuego": 1, "Planta": 1}


def test_promedio_por_tipo():
    r = modulo.promedio_por_tipo(_db())
    assert r["Electrico"] == 30 and r["Fuego"] == 90
