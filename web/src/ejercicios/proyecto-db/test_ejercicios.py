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


def test_contar():
    assert modulo.contar(_db()) == 3


def test_nombres():
    assert modulo.nombres(_db()) == ["Pikachu", "Charizard", "Vulpix"]


def test_nivel_promedio():
    assert round(modulo.nivel_promedio(_db()), 2) == 44.33


def test_tipos():
    assert modulo.tipos(_db()) == ["Electrico", "Fuego"]


def test_borrar():
    c = _db()
    modulo.borrar(c, "Pikachu")
    assert modulo.contar(c) == 2


def test_subir_nivel():
    c = _db()
    modulo.subir_nivel(c, "Pikachu", 5)
    assert modulo.buscar(c, "Pikachu")[2] == 30


def test_buscar():
    assert modulo.buscar(_db(), "Charizard") == ("Charizard", "Fuego", 90)
    assert modulo.buscar(_db(), "Mew") is None


def test_existe():
    assert modulo.existe(_db(), "Pikachu") is True
    assert modulo.existe(_db(), "Mew") is False


def test_mas_debil():
    assert modulo.mas_debil(_db()) == "Vulpix"


def test_de_nivel_minimo():
    assert sorted(modulo.de_nivel_minimo(_db(), 20)) == ["Charizard", "Pikachu"]


def test_nivel_total():
    assert modulo.nivel_total(_db()) == 133


def test_promedio_por_tipo():
    assert modulo.promedio_por_tipo(_db()) == {"Electrico": 25.0, "Fuego": 54.0}


def test_renombrar():
    c = _db()
    modulo.renombrar(c, "Pikachu", "Pika")
    assert modulo.existe(c, "Pika") is True


def test_ordenados_por_nivel():
    assert modulo.ordenados_por_nivel(_db()) == ["Charizard", "Pikachu", "Vulpix"]
