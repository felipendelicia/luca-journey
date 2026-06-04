"""Tests del módulo agenda.equipo."""

from agenda.pokemon import Pokemon
from agenda.equipo import Equipo


def _poke(nombre):
    return Pokemon(nombre, "Normal", 10)


def test_agregar():
    e = Equipo()
    ok, msg = e.agregar(_poke("Pikachu"))
    assert ok is True
    assert e.cantidad() == 1


def test_no_duplicados():
    e = Equipo()
    e.agregar(_poke("Pikachu"))
    ok, msg = e.agregar(_poke("Pikachu"))
    assert ok is False
    assert "ya está" in msg


def test_maximo_seis():
    e = Equipo()
    for i in range(6):
        e.agregar(_poke(f"Poke{i}"))
    ok, msg = e.agregar(_poke("Extra"))
    assert ok is False
    assert "lleno" in msg
    assert e.cantidad() == 6


def test_quitar():
    e = Equipo()
    e.agregar(_poke("Pikachu"))
    ok, msg = e.quitar("Pikachu")
    assert ok is True
    assert e.cantidad() == 0


def test_quitar_inexistente():
    e = Equipo()
    ok, msg = e.quitar("Mewtwo")
    assert ok is False
    assert "no está" in msg


def test_buscar_case_insensitive():
    e = Equipo()
    e.agregar(_poke("Pikachu"))
    assert e.buscar("pikachu") is not None


def test_nombres_y_to_list():
    e = Equipo()
    e.agregar(_poke("Pikachu"))
    e.agregar(_poke("Onix"))
    assert e.nombres() == ["Pikachu", "Onix"]
    assert e.to_list() == ["Pikachu", "Onix"]
