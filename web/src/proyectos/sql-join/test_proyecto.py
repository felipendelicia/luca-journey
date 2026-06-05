import ejercicios
import sqlite3


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT)")
    c.execute("CREATE TABLE tipos (tipo TEXT, debilidad TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?)", [
        ("Bronzor",   "Acero"),
        ("Steelix",   "Acero"),
        ("Magneton",  "Acero"),
        ("Bastiodon", "Acero"),
    ])
    c.executemany("INSERT INTO tipos VALUES (?, ?)", [
        ("Acero",  "Fuego"),
        ("Agua",   "Planta"),
        ("Planta", "Fuego"),
        ("Fuego",  "Agua"),
    ])
    return c


def test_con_debilidad():
    assert ejercicios.con_debilidad(_db()) == [
        ("Bronzor", "Fuego"),
        ("Steelix", "Fuego"),
        ("Magneton", "Fuego"),
        ("Bastiodon", "Fuego"),
    ]


def test_debilidad_de():
    assert ejercicios.debilidad_de(_db(), "Steelix") == "Fuego"
    assert ejercicios.debilidad_de(_db(), "Magneton") == "Fuego"


def test_nombres_y_tipos():
    assert ejercicios.nombres_y_tipos(_db()) == [
        ("Bronzor", "Acero"),
        ("Steelix", "Acero"),
        ("Magneton", "Acero"),
        ("Bastiodon", "Acero"),
    ]


def test_debiles_a():
    assert set(ejercicios.debiles_a(_db(), "Fuego")) == {"Bronzor", "Steelix", "Magneton", "Bastiodon"}
    assert len(ejercicios.debiles_a(_db(), "Fuego")) == 4
    assert ejercicios.debiles_a(_db(), "Agua") == []
