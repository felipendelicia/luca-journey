"""
🧪 Tests del Creador de Pokémon Personalizado — Semana 08
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana08_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")
PokemonPersonalizado = interactivo.PokemonPersonalizado


def test_total_stats():
    p = PokemonPersonalizado("Test", "Normal", 50, 60, 70)
    assert p.total_stats() == 180


def test_categoria_legendario():
    p = PokemonPersonalizado("Mewtwo", "Psiquico", 90, 80, 90)
    assert p.categoria() == "Legendario", "Total 260 debería ser Legendario"


def test_categoria_fuerte():
    p = PokemonPersonalizado("Test", "Normal", 60, 50, 60)
    assert p.categoria() == "Fuerte", "Total 170 debería ser Fuerte"


def test_categoria_comun():
    p = PokemonPersonalizado("Rattata", "Normal", 30, 20, 40)
    assert p.categoria() == "Comun", "Total 90 debería ser Comun"


def test_ficha_incluye_datos():
    p = PokemonPersonalizado("Pikachu", "Electrico", 55, 40, 90)
    ficha = p.ficha()
    assert "Pikachu" in ficha
    assert "Electrico" in ficha
    assert isinstance(ficha, str)
