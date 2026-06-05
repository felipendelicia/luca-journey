import ejercicios
import sqlite3


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Meditite",  28, "Lucha"),
        ("Machoke",   27, "Lucha"),
        ("Lucario",   34, "Lucha"),
        ("Zubat",     18, "Veneno"),
        ("Geodude",   15, "Roca"),
    ])
    return c


def test_de_tipo():
    assert ejercicios.de_tipo(_db(), "Lucha") == ["Meditite", "Machoke", "Lucario"]
    assert ejercicios.de_tipo(_db(), "Roca") == ["Geodude"]
    assert ejercicios.de_tipo(_db(), "Agua") == []


def test_fuertes():
    assert ejercicios.fuertes(_db(), 27) == ["Lucario", "Meditite", "Machoke"]
    assert ejercicios.fuertes(_db(), 35) == []


def test_ordenados_por_nivel():
    assert ejercicios.ordenados_por_nivel(_db()) == ["Lucario", "Meditite", "Machoke", "Zubat", "Geodude"]


def test_top_tres():
    assert ejercicios.top_tres(_db()) == ["Lucario", "Meditite", "Machoke"]
