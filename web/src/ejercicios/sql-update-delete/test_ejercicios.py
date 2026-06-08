"""🧪 Tests — SQL: actualizar y borrar"""
import importlib.util
import os
import sqlite3

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"sqlupd_{nombre}", ruta)
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


def _nivel(c, nombre):
    return c.execute("SELECT nivel FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()[0]


def _nombres(c):
    return [f[0] for f in c.execute("SELECT nombre FROM pokemon ORDER BY nombre")]


def test_cambiar_nivel():
    c = _db()
    modulo.cambiar_nivel(c, "Pikachu", 50)
    assert _nivel(c, "Pikachu") == 50


def test_subir_todos():
    c = _db()
    modulo.subir_todos(c, 5)
    assert _nivel(c, "Pikachu") == 30 and _nivel(c, "Charizard") == 95


def test_borrar():
    c = _db()
    modulo.borrar(c, "Bulbasaur")
    assert _nombres(c) == ["Charizard", "Pikachu"]


def test_borrar_debiles():
    c = _db()
    modulo.borrar_debiles(c, 20)
    assert _nombres(c) == ["Charizard", "Pikachu"]


def _tipo(c, nombre):
    return c.execute("SELECT tipo FROM pokemon WHERE nombre = ?", (nombre,)).fetchone()[0]


def test_bajar_todos():
    c = _db()
    modulo.bajar_todos(c, 5)
    assert _nivel(c, "Pikachu") == 20


def test_cambiar_tipo():
    c = _db()
    modulo.cambiar_tipo(c, "Pikachu", "Rayo")
    assert _tipo(c, "Pikachu") == "Rayo"


def test_duplicar_niveles():
    c = _db()
    modulo.duplicar_niveles(c)
    assert _nivel(c, "Pikachu") == 50


def test_poner_nivel_minimo():
    c = _db()
    modulo.poner_nivel_minimo(c, 20)
    assert _nivel(c, "Bulbasaur") == 20
    assert _nivel(c, "Pikachu") == 25


def test_borrar_de_tipo():
    c = _db()
    modulo.borrar_de_tipo(c, "Fuego")
    assert _nombres(c) == ["Bulbasaur", "Pikachu"]


def test_borrar_todos():
    c = _db()
    modulo.borrar_todos(c)
    assert _nombres(c) == []


def test_subir_de_tipo():
    c = _db()
    modulo.subir_de_tipo(c, "Fuego", 10)
    assert _nivel(c, "Charizard") == 100


def test_renombrar():
    c = _db()
    modulo.renombrar(c, "Pikachu", "Pika")
    assert "Pika" in _nombres(c)


def test_nivelar():
    c = _db()
    modulo.nivelar(c, 50)
    assert _nivel(c, "Charizard") == 50


def test_borrar_fuertes():
    c = _db()
    modulo.borrar_fuertes(c, 50)
    assert _nombres(c) == ["Bulbasaur", "Pikachu"]


def test_limitar_nivel():
    c = _db()
    modulo.limitar_nivel(c, 50)
    assert _nivel(c, "Charizard") == 50


def test_incrementar():
    c = _db()
    modulo.incrementar(c, "Pikachu", 5)
    assert _nivel(c, "Pikachu") == 30


def test_cambiar_nivel_de_tipo():
    c = _db()
    modulo.cambiar_nivel_de_tipo(c, "Electrico", 99)
    assert _nivel(c, "Pikachu") == 99


def test_sumar_a_los_debiles():
    c = _db()
    modulo.sumar_a_los_debiles(c, 30, 100)
    assert _nivel(c, "Pikachu") == 125
    assert _nivel(c, "Charizard") == 90


def test_reset_tipo():
    c = _db()
    modulo.reset_tipo(c, "Fuego", "Llama")
    assert _tipo(c, "Charizard") == "Llama"


def test_borrar_y_contar():
    c = _db()
    assert modulo.borrar_y_contar(c, "Electrico") == 1
