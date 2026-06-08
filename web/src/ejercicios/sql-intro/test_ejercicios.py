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


def test_ordenados_por_nivel():
    assert modulo.ordenados_por_nivel(_db()) == ["Charizard", "Pikachu", "Bulbasaur"]


def test_mas_de():
    assert modulo.mas_de(_db(), 20) == ["Pikachu", "Charizard"]


def test_de_tipo():
    assert modulo.de_tipo(_db(), "Fuego") == ["Charizard"]


def test_promedio_nivel():
    assert round(modulo.promedio_nivel(_db()), 1) == 42.3


def test_maximo_nivel():
    assert modulo.maximo_nivel(_db()) == 90


def test_minimo_nivel():
    assert modulo.minimo_nivel(_db()) == 12


def test_nivel_total():
    assert modulo.nivel_total(_db()) == 127


def test_contar_de_tipo():
    assert modulo.contar_de_tipo(_db(), "Fuego") == 1


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(_db()) == "Charizard"


def test_tipos_distintos():
    assert modulo.tipos_distintos(_db()) == ["Electrico", "Fuego", "Planta"]


def test_existe():
    assert modulo.existe(_db(), "Pikachu") is True
    assert modulo.existe(_db(), "Mew") is False


def test_nivel_de():
    assert modulo.nivel_de(_db(), "Pikachu") == 25
    assert modulo.nivel_de(_db(), "Mew") is None


def test_primeros():
    assert modulo.primeros(_db(), 2) == ["Pikachu", "Charizard"]


def test_nombres_que_empiezan():
    assert modulo.nombres_que_empiezan(_db(), "B") == ["Bulbasaur"]


def test_ordenados_alfabeticamente():
    assert modulo.ordenados_alfabeticamente(_db()) == ["Bulbasaur", "Charizard", "Pikachu"]
