import ejercicios
import sqlite3


def _pokedex():
    c = ejercicios.crear_pokedex()
    ejercicios.agregar(c, "Raichu",  "Electrico", 45)
    ejercicios.agregar(c, "Luxray",  "Electrico", 42)
    ejercicios.agregar(c, "Garchomp", "Dragon",   58)
    return c


def test_crear_pokedex():
    c = ejercicios.crear_pokedex()
    resultado = c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0]
    assert resultado == 0


def test_agregar_y_listar():
    c = ejercicios.crear_pokedex()
    ejercicios.agregar(c, "Raichu", "Electrico", 45)
    ejercicios.agregar(c, "Luxray", "Electrico", 42)
    assert ejercicios.listar(c) == ["Luxray", "Raichu"]


def test_por_tipo_y_fuerte():
    c = _pokedex()
    electricos = ejercicios.por_tipo(c, "Electrico")
    assert set(electricos) == {"Raichu", "Luxray"}
    assert ejercicios.por_tipo(c, "Agua") == []
    assert ejercicios.el_mas_fuerte(c) == "Garchomp"


def test_actualizar_y_borrar():
    c = _pokedex()
    ejercicios.actualizar_nivel(c, "Luxray", 60)
    nivel = c.execute("SELECT nivel FROM pokemon WHERE nombre = 'Luxray'").fetchone()[0]
    assert nivel == 60
    ejercicios.borrar(c, "Raichu")
    nombres = [f[0] for f in c.execute("SELECT nombre FROM pokemon")]
    assert "Raichu" not in nombres
    assert len(nombres) == 2
