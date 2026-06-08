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


def _lleno():
    c = _con_tabla()
    c.executemany("INSERT INTO entrenadores VALUES (?, ?)", [("Ash", 8), ("Gary", 5), ("Misty", 3)])
    return c


def test_contar():
    assert modulo.contar(_lleno()) == 3


def test_todos_los_nombres():
    assert modulo.todos_los_nombres(_lleno()) == ["Ash", "Gary", "Misty"]


def test_medallas_de():
    assert modulo.medallas_de(_lleno(), "Gary") == 5
    assert modulo.medallas_de(_lleno(), "Brock") is None


def test_total_medallas():
    assert modulo.total_medallas(_lleno()) == 16


def test_promedio_medallas():
    assert round(modulo.promedio_medallas(_lleno()), 2) == 5.33


def test_el_mejor():
    assert modulo.el_mejor(_lleno()) == "Ash"


def test_con_mas_de():
    assert sorted(modulo.con_mas_de(_lleno(), 4)) == ["Ash", "Gary"]


def test_ordenados_por_medallas():
    assert modulo.ordenados_por_medallas(_lleno()) == ["Ash", "Gary", "Misty"]


def test_existe():
    assert modulo.existe(_lleno(), "Ash") is True
    assert modulo.existe(_lleno(), "Brock") is False


def test_insertar_si_no_existe():
    c = _lleno()
    modulo.insertar_si_no_existe(c, "Brock", 7)
    assert modulo.contar(c) == 4
    modulo.insertar_si_no_existe(c, "Ash", 99)
    assert modulo.contar(c) == 4


def test_maximo_medallas():
    assert modulo.maximo_medallas(_lleno()) == 8


def test_cantidad_con():
    assert modulo.cantidad_con(_lleno(), 5) == 1


def test_nombres_y_medallas():
    assert modulo.nombres_y_medallas(_lleno()) == [("Ash", 8), ("Gary", 5), ("Misty", 3)]


def test_vaciar():
    c = _lleno()
    modulo.vaciar(c)
    assert modulo.contar(c) == 0


def test_actualizar_medallas():
    c = _lleno()
    modulo.actualizar_medallas(c, "Misty", 10)
    assert modulo.medallas_de(c, "Misty") == 10


def test_campeones():
    assert sorted(modulo.campeones(_lleno(), 5)) == ["Ash", "Gary"]
