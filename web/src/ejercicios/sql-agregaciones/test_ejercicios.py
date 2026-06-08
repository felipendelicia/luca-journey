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


def test_nivel_minimo():
    assert modulo.nivel_minimo(_db()) == 10


def test_cuantos_de_tipo():
    assert modulo.cuantos_de_tipo(_db(), "Electrico") == 2


def test_suma_por_tipo():
    assert modulo.suma_por_tipo(_db()) == {"Electrico": 60, "Fuego": 90, "Planta": 10}


def test_maximo_por_tipo():
    assert modulo.maximo_por_tipo(_db()) == {"Electrico": 40, "Fuego": 90, "Planta": 10}


def test_tipo_mas_numeroso():
    assert modulo.tipo_mas_numeroso(_db()) == "Electrico"


def test_nivel_total_de_tipo():
    assert modulo.nivel_total_de_tipo(_db(), "Electrico") == 60


def test_cantidad_tipos():
    assert modulo.cantidad_tipos(_db()) == 3


def test_rango_nivel():
    assert modulo.rango_nivel(_db()) == 80


def test_cuantos_arriba_de():
    assert modulo.cuantos_arriba_de(_db(), 30) == 2


def test_promedio_de_tipo():
    assert modulo.promedio_de_tipo(_db(), "Electrico") == 30.0


def test_minimo_por_tipo():
    assert modulo.minimo_por_tipo(_db()) == {"Electrico": 20, "Fuego": 90, "Planta": 10}


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(_db()) == "Charizard"


def test_hay_de_tipo():
    assert modulo.hay_de_tipo(_db(), "Fuego") is True
    assert modulo.hay_de_tipo(_db(), "Agua") is False


def test_conteo_por_tipo_ordenado():
    assert modulo.conteo_por_tipo_ordenado(_db()) == [("Electrico", 2), ("Fuego", 1), ("Planta", 1)]
