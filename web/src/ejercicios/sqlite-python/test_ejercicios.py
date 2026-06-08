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


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?)", [("Pikachu", 25), ("Charizard", 90), ("Bulbasaur", 12)])
    return c


def test_todos():
    assert modulo.todos(_db()) == ["Pikachu", "Charizard", "Bulbasaur"]


def test_niveles():
    assert modulo.niveles(_db()) == [25, 90, 12]


def test_actualizar():
    c = _db()
    modulo.actualizar(c, "Pikachu", 50)
    assert modulo.nivel_de(c, "Pikachu") == 50


def test_borrar():
    c = _db()
    modulo.borrar(c, "Pikachu")
    assert modulo.todos(c) == ["Charizard", "Bulbasaur"]


def test_existe():
    assert modulo.existe(_db(), "Pikachu") is True
    assert modulo.existe(_db(), "Mew") is False


def test_nivel_de():
    assert modulo.nivel_de(_db(), "Charizard") == 90
    assert modulo.nivel_de(_db(), "Mew") is None


def test_promedio():
    assert round(modulo.promedio(_db()), 2) == 42.33


def test_maximo():
    assert modulo.maximo(_db()) == 90


def test_guardar_varios():
    c = _db()
    modulo.guardar_varios(c, [("Mew", 5), ("Snorlax", 70)])
    assert modulo.existe(c, "Snorlax") is True


def test_mas_fuerte():
    assert modulo.mas_fuerte(_db()) == "Charizard"


def test_ordenados():
    assert modulo.ordenados(_db()) == ["Charizard", "Pikachu", "Bulbasaur"]


def test_contar_arriba():
    assert modulo.contar_arriba(_db(), 20) == 2


def test_vaciar():
    c = _db()
    modulo.vaciar(c)
    assert modulo.todos(c) == []


def test_a_diccionario():
    assert modulo.a_diccionario(_db()) == {"Pikachu": 25, "Charizard": 90, "Bulbasaur": 12}


def test_subir_nivel():
    c = _db()
    modulo.subir_nivel(c, "Pikachu", 5)
    assert modulo.nivel_de(c, "Pikachu") == 30


def test_total_niveles():
    assert modulo.total_niveles(_db()) == 127
