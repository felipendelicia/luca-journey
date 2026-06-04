"""
🧪 Tests del Gestor de Equipo — Semana 06
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana06_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")
GestorEquipo = interactivo.GestorEquipo


def test_agregar_pokemon():
    g = GestorEquipo()
    msg = g.agregar("Pikachu", "Electrico", 25)
    assert "se unió" in msg
    assert g.cantidad() == 1


def test_no_agregar_duplicados():
    g = GestorEquipo()
    g.agregar("Pikachu", "Electrico", 25)
    msg = g.agregar("Pikachu", "Electrico", 30)
    assert "ya está" in msg, "No debería permitir nombres repetidos"
    assert g.cantidad() == 1


def test_equipo_maximo_seis():
    g = GestorEquipo()
    for i in range(6):
        g.agregar(f"Poke{i}", "Normal", 10)
    msg = g.agregar("UnoMas", "Normal", 10)
    assert "lleno" in msg, "No debería permitir un séptimo Pokémon"
    assert g.cantidad() == 6


def test_quitar_pokemon():
    g = GestorEquipo()
    g.agregar("Pikachu", "Electrico", 25)
    msg = g.quitar("Pikachu")
    assert "dejó el equipo" in msg
    assert g.cantidad() == 0


def test_quitar_inexistente():
    g = GestorEquipo()
    msg = g.quitar("Mewtwo")
    assert "no está" in msg, "Quitar algo inexistente debería avisar"


def test_buscar_encuentra():
    g = GestorEquipo()
    g.agregar("Pikachu", "Electrico", 25)
    encontrado = g.buscar("pikachu")  # también busca en minúsculas
    assert encontrado is not None
    assert encontrado["nombre"] == "Pikachu"


def test_buscar_no_encuentra():
    g = GestorEquipo()
    assert g.buscar("Mewtwo") is None


def test_listar_vacio():
    g = GestorEquipo()
    assert g.listar() == ["(equipo vacío)"]


def test_listar_con_pokemon():
    g = GestorEquipo()
    g.agregar("Pikachu", "Electrico", 25)
    lineas = g.listar()
    assert any("Pikachu" in l for l in lineas), "El listado debería incluir a Pikachu"
