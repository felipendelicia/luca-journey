"""🧪 Tests — SQL: filtrar y ordenar"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlselect_{nombre}", ruta)
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
        ("Charmander", 40, "Fuego"),
        ("Snorlax", 70, "Normal"),
    ])
    return c


def test_de_tipo():
    assert sorted(modulo.de_tipo(_db(), "Fuego")) == ["Charizard", "Charmander"]


def test_fuertes():
    assert modulo.fuertes(_db(), 50) == ["Charizard", "Snorlax"]


def test_ordenados_por_nivel():
    assert modulo.ordenados_por_nivel(_db()) == ["Charizard", "Snorlax", "Charmander", "Pikachu", "Bulbasaur"]


def test_empiezan_con():
    assert sorted(modulo.empiezan_con(_db(), "C")) == ["Charizard", "Charmander"]


def test_top():
    assert modulo.top(_db(), 2) == ["Charizard", "Snorlax"]


def test_debiles():
    assert sorted(modulo.debiles(_db(), 40)) == ["Bulbasaur", "Charmander", "Pikachu"]


def test_entre_niveles():
    assert sorted(modulo.entre_niveles(_db(), 20, 70)) == ["Charmander", "Pikachu", "Snorlax"]


def test_no_de_tipo():
    assert sorted(modulo.no_de_tipo(_db(), "Fuego")) == ["Bulbasaur", "Pikachu", "Snorlax"]


def test_contienen():
    assert sorted(modulo.contienen(_db(), "Char")) == ["Charizard", "Charmander"]


def test_ordenados_alfabeticamente():
    assert modulo.ordenados_alfabeticamente(_db()) == ["Bulbasaur", "Charizard", "Charmander", "Pikachu", "Snorlax"]


def test_ultimo_alfabetico():
    assert modulo.ultimo_alfabetico(_db()) == "Snorlax"


def test_nombres_y_tipos():
    assert modulo.nombres_y_tipos(_db())[0] == ("Pikachu", "Electrico")


def test_dos_tipos():
    assert sorted(modulo.dos_tipos(_db(), "Fuego", "Planta")) == ["Bulbasaur", "Charizard", "Charmander"]


def test_cantidad_por_encima():
    assert modulo.cantidad_por_encima(_db(), 30) == 3


def test_nombres_largos():
    assert sorted(modulo.nombres_largos(_db(), 7)) == ["Bulbasaur", "Charizard", "Charmander"]


def test_el_de_nivel():
    assert modulo.el_de_nivel(_db(), 90) == "Charizard"
    assert modulo.el_de_nivel(_db(), 999) is None


def test_distintos_tipos():
    assert modulo.distintos_tipos(_db()) == ["Electrico", "Fuego", "Normal", "Planta"]


def test_los_n_mas_debiles():
    assert modulo.los_n_mas_debiles(_db(), 2) == ["Bulbasaur", "Pikachu"]


def test_mas_fuerte_de_tipo():
    assert modulo.mas_fuerte_de_tipo(_db(), "Fuego") == "Charizard"


def test_ordenar_por_tipo():
    assert modulo.ordenar_por_tipo(_db()) == ["Pikachu", "Charizard", "Charmander", "Snorlax", "Bulbasaur"]
