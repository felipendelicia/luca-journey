import ejercicios
import sqlite3


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Geodude",  11, "Roca"),
        ("Onix",     14, "Roca"),
        ("Machop",    8, "Lucha"),
        ("Zubat",     9, "Veneno"),
        ("Nosepass", 12, "Roca"),
    ])
    return c


def test_todos_los_nombres():
    assert ejercicios.todos_los_nombres(_db()) == ["Geodude", "Onix", "Machop", "Zubat", "Nosepass"]


def test_cuantos_hay():
    assert ejercicios.cuantos_hay(_db()) == 5


def test_nombres_y_niveles():
    assert ejercicios.nombres_y_niveles(_db()) == [
        ("Geodude", 11), ("Onix", 14), ("Machop", 8), ("Zubat", 9), ("Nosepass", 12)
    ]


def test_el_primero():
    assert ejercicios.el_primero(_db()) == "Geodude"
