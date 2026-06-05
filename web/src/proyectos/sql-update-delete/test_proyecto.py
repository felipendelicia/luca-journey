import ejercicios
import sqlite3


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Gyarados",  34, "Agua"),
        ("Quagsire",  27, "Agua"),
        ("Floatzel",  29, "Agua"),
        ("Gastrodon", 30, "Agua"),
        ("Magikarp",   8, "Agua"),
    ])
    return c


def test_cambiar_nivel():
    c = _db()
    ejercicios.cambiar_nivel(c, "Magikarp", 20)
    nivel = c.execute("SELECT nivel FROM pokemon WHERE nombre = 'Magikarp'").fetchone()[0]
    assert nivel == 20


def test_subir_todos():
    c = _db()
    ejercicios.subir_todos(c, 5)
    niveles = {f[0]: f[1] for f in c.execute("SELECT nombre, nivel FROM pokemon")}
    assert niveles["Gyarados"] == 39
    assert niveles["Quagsire"] == 32
    assert niveles["Magikarp"] == 13


def test_borrar():
    c = _db()
    ejercicios.borrar(c, "Magikarp")
    nombres = [f[0] for f in c.execute("SELECT nombre FROM pokemon")]
    assert "Magikarp" not in nombres
    assert len(nombres) == 4


def test_borrar_debiles():
    c = _db()
    ejercicios.borrar_debiles(c, 28)
    nombres = [f[0] for f in c.execute("SELECT nombre FROM pokemon")]
    assert "Quagsire" not in nombres
    assert "Magikarp" not in nombres
    assert "Gyarados" in nombres
    assert "Floatzel" in nombres
    assert "Gastrodon" in nombres
