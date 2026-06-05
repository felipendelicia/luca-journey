import ejercicios
import sqlite3


def _base_cargada():
    c = ejercicios.crear_base()
    ejercicios.cargar_datos(c)
    return c


def test_crear_base():
    c = ejercicios.crear_base()
    assert c.execute("SELECT COUNT(*) FROM tipos").fetchone()[0] == 0
    assert c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0] == 0


def test_cargar_datos():
    c = ejercicios.crear_base()
    ejercicios.cargar_datos(c)
    assert c.execute("SELECT COUNT(*) FROM tipos").fetchone()[0] == 5
    assert c.execute("SELECT COUNT(*) FROM pokemon").fetchone()[0] == 8


def test_estadisticas():
    c = _base_cargada()
    prom = ejercicios.promedio_por_tipo(c)
    assert abs(prom["Agua"] - 36.5) < 0.01
    assert abs(prom["Fuego"] - 38.0) < 0.01
    assert abs(prom["Dragon"] - 66.0) < 0.01

    fuerte = ejercicios.el_mas_fuerte_por_tipo(c)
    assert fuerte["Agua"] == "Empoleon"
    assert fuerte["Fuego"] == "Infernape"
    assert fuerte["Dragon"] == "Garchomp"


def test_debilidades_join():
    c = _base_cargada()
    resultado = ejercicios.con_debilidad(c)
    assert len(resultado) == 8
    assert resultado[0] == ("Piplup", "Planta")

    debiles = ejercicios.mas_debiles_a(c, "Agua")
    assert debiles == ["Infernape", "Chimchar"]


def test_buscar_y_actualizar():
    c = _base_cargada()
    assert ejercicios.buscar(c, "Garchomp") == ("Garchomp", "Dragon", 66)
    assert ejercicios.buscar(c, "Mew") is None

    ejercicios.evolucionar(c, "Chimchar", "Monferno", 26)
    assert ejercicios.buscar(c, "Monferno") == ("Monferno", "Fuego", 26)
    assert ejercicios.buscar(c, "Chimchar") is None
