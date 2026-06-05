import ejercicios
import sqlite3


def _con_tabla():
    c = sqlite3.connect(":memory:")
    c.execute("CREATE TABLE pokemon (nombre TEXT, nivel INTEGER)")
    return c


def test_crear_conexion():
    c = ejercicios.crear_conexion()
    # La tabla debe existir y estar vacía
    resultado = c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    assert resultado == 0


def test_guardar():
    c = _con_tabla()
    ejercicios.guardar(c, "Snover", 40)
    fila = c.execute("SELECT nombre, nivel FROM pokemon WHERE nombre = 'Snover'").fetchone()
    assert fila == ("Snover", 40)


def test_cantidad():
    c = _con_tabla()
    ejercicios.guardar(c, "Snover", 40)
    ejercicios.guardar(c, "Abomasnow", 58)
    assert ejercicios.cantidad(c) == 2


def test_buscar():
    c = _con_tabla()
    ejercicios.guardar(c, "Snover", 40)
    assert ejercicios.buscar(c, "Snover") == ("Snover", 40)
    assert ejercicios.buscar(c, "Mew") is None
