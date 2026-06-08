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


def test_nombres_y_debilidad():
    assert sorted(modulo.nombres_y_debilidad(_db())) == [("Blastoise", "Planta"), ("Charizard", "Agua"), ("Vulpix", "Agua")]


def test_cuantos_debiles_a():
    assert modulo.cuantos_debiles_a(_db(), "Agua") == 2


def test_tipos_con_debilidad():
    assert sorted(modulo.tipos_con_debilidad(_db())) == [("Agua", "Planta"), ("Fuego", "Agua")]


def test_debilidad_del_tipo():
    assert modulo.debilidad_del_tipo(_db(), "Fuego") == "Agua"
    assert modulo.debilidad_del_tipo(_db(), "Roca") is None


def test_sin_debilidad_conocida():
    assert modulo.sin_debilidad_conocida(_db()) == []


def test_con_debilidad_conocida():
    assert sorted(modulo.con_debilidad_conocida(_db())) == ["Blastoise", "Charizard", "Vulpix"]


def test_contar_join():
    assert modulo.contar_join(_db()) == 3


def test_mapa_debilidades():
    assert modulo.mapa_debilidades(_db()) == {"Fuego": "Agua", "Agua": "Planta"}


def test_tipos_de_pokemon():
    assert modulo.tipos_de_pokemon(_db()) == ["Agua", "Fuego"]


def test_debilidades_distintas():
    assert modulo.debilidades_distintas(_db()) == ["Agua", "Planta"]


def test_nombre_tipo_debilidad():
    assert ("Charizard", "Fuego", "Agua") in modulo.nombre_tipo_debilidad(_db())


def test_hay_debilidad_para():
    assert modulo.hay_debilidad_para(_db(), "Fuego") is True
    assert modulo.hay_debilidad_para(_db(), "Roca") is False


def test_primer_debil_a():
    assert modulo.primer_debil_a(_db(), "Planta") == "Blastoise"
    assert modulo.primer_debil_a(_db(), "Tierra") is None


def test_tipos_que_pierden_contra():
    assert modulo.tipos_que_pierden_contra(_db(), "Agua") == ["Fuego"]


def test_cuantos_de_tipo():
    assert modulo.cuantos_de_tipo(_db(), "Fuego") == 2


def test_nombres_debiles_ordenados():
    assert modulo.nombres_debiles_ordenados(_db()) == ["Blastoise", "Charizard", "Vulpix"]


def test_todos_los_nombres():
    assert sorted(modulo.todos_los_nombres(_db())) == ["Blastoise", "Charizard", "Vulpix"]
