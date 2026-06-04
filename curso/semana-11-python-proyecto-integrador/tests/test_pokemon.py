"""Tests del módulo agenda.pokemon."""

from agenda.pokemon import Pokemon


def test_creacion():
    p = Pokemon("Pikachu", "Electrico", 25, "2024-01-01")
    assert p.nombre == "Pikachu"
    assert p.tipo == "Electrico"
    assert p.nivel == 25
    assert p.fecha_captura == "2024-01-01"


def test_nivel_se_guarda_como_int():
    p = Pokemon("Onix", "Roca", "30")
    assert p.nivel == 30
    assert isinstance(p.nivel, int)


def test_fecha_por_defecto():
    p = Pokemon("Pikachu", "Electrico", 25)
    # Sin fecha, se completa con la de hoy (formato AAAA-MM-DD, 10 caracteres).
    assert len(p.fecha_captura) == 10


def test_to_dict_y_from_dict():
    original = Pokemon("Charizard", "Fuego", 50, "2024-02-02")
    d = original.to_dict()
    assert d == {
        "nombre": "Charizard",
        "tipo": "Fuego",
        "nivel": 50,
        "fecha_captura": "2024-02-02",
    }
    reconstruido = Pokemon.from_dict(d)
    assert reconstruido == original


def test_igualdad_por_nombre():
    a = Pokemon("Pikachu", "Electrico", 25)
    b = Pokemon("Pikachu", "Electrico", 99)
    assert a == b, "Dos Pokémon con el mismo nombre se consideran iguales"
