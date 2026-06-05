import ejercicios
import sqlite3


def _db_vacia():
    return sqlite3.connect(":memory:")


def _db_con_tabla():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, tipo TEXT, nivel INTEGER)")
    return c


def test_crear_tabla():
    c = _db_vacia()
    ejercicios.crear_tabla(c)
    # Si la tabla existe, COUNT(*) no lanza excepción
    resultado = c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    assert resultado == 0


def test_insertar_uno():
    c = _db_con_tabla()
    ejercicios.insertar_uno(c, "Turtwig", "Planta", 10)
    filas = c.execute("SELECT nombre, tipo, nivel FROM pokemon").fetchall()
    assert filas == [("Turtwig", "Planta", 10)]


def test_insertar_varios():
    c = _db_con_tabla()
    ejercicios.insertar_varios(c, [("Cherubi", "Planta", 7), ("Roserade", "Planta", 22)])
    filas = c.execute("SELECT nombre FROM pokemon").fetchall()
    assert len(filas) == 2
    nombres = [f[0] for f in filas]
    assert "Cherubi" in nombres
    assert "Roserade" in nombres


def test_contar_registros():
    c = _db_con_tabla()
    ejercicios.insertar_varios(c, [
        ("Turtwig", "Planta", 10),
        ("Cherubi", "Planta", 7),
        ("Roserade", "Planta", 22),
    ])
    assert ejercicios.contar_registros(c) == 3
