import ejercicios
import sqlite3


def _db():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER, tipo TEXT)")
    c.executemany("INSERT INTO pokemon VALUES (?, ?, ?)", [
        ("Gengar",     38, "Fantasma"),
        ("Mismagius",  36, "Fantasma"),
        ("Duskull",    21, "Fantasma"),
        ("Clefable",   35, "Normal"),
        ("Jigglypuff", 17, "Normal"),
    ])
    return c


def test_nivel_promedio():
    assert ejercicios.nivel_promedio(_db()) == pytest_approx(29.4)


def test_nivel_maximo():
    assert ejercicios.nivel_maximo(_db()) == 38


def test_cuantos_por_tipo():
    assert ejercicios.cuantos_por_tipo(_db()) == {"Fantasma": 3, "Normal": 2}


def test_promedio_por_tipo():
    resultado = ejercicios.promedio_por_tipo(_db())
    assert abs(resultado["Fantasma"] - (38 + 36 + 21) / 3) < 0.01
    assert abs(resultado["Normal"] - (35 + 17) / 2) < 0.01


def pytest_approx(valor):
    class Aprox:
        def __eq__(self, other):
            return abs(other - valor) < 0.01
    return Aprox()
