"""Tests del módulo agenda.batallas."""

from agenda.batallas import Batalla, Historial, GANO, PERDIO


def test_batalla_gano():
    b = Batalla("Brock", GANO, "Pikachu")
    assert b.gano() is True


def test_batalla_perdio():
    b = Batalla("Brock", PERDIO, "Pikachu")
    assert b.gano() is False


def test_to_dict_y_from_dict():
    b = Batalla("Misty", GANO, "Charizard", "2024-03-03")
    d = b.to_dict()
    assert d["rival"] == "Misty"
    assert d["resultado"] == GANO
    reconstruido = Batalla.from_dict(d)
    assert reconstruido.rival == "Misty"
    assert reconstruido.gano() is True


def test_historial_conteos():
    h = Historial()
    h.registrar(Batalla("A", GANO, "Pikachu"))
    h.registrar(Batalla("B", GANO, "Pikachu"))
    h.registrar(Batalla("C", PERDIO, "Onix"))
    assert h.total() == 3
    assert h.victorias() == 2
    assert h.derrotas() == 1


def test_historial_vacio():
    h = Historial()
    assert h.total() == 0
    assert h.victorias() == 0
    assert h.derrotas() == 0
