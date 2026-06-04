"""
batalla_pokemon.datos — Roster de Pokémon listos para pelear.

Cada función crea un Pokémon NUEVO (con sus movimientos frescos), así dos
batallas no comparten el mismo objeto.
"""

from .modelos import Movimiento, Pokemon
from . import estados


def crear_pikachu():
    return Pokemon("Pikachu", "electrico", 100, [
        Movimiento("Impactrueno", "electrico", 40, 15, efecto=estados.PARALIZADO, prob_efecto=0.3),
        Movimiento("Ataque Rápido", "normal", 30, 30),
        Movimiento("Rayo", "electrico", 55, 10),
        Movimiento("Trueno", "electrico", 70, 5, efecto=estados.PARALIZADO, prob_efecto=0.3),
    ])


def crear_charizard():
    return Pokemon("Charizard", "fuego", 100, [
        Movimiento("Lanzallamas", "fuego", 55, 15, efecto=estados.ENVENENADO, prob_efecto=0.1),
        Movimiento("Garra", "normal", 35, 25),
        Movimiento("Llamarada", "fuego", 70, 5),
        Movimiento("Vuelo", "volador", 45, 15),
    ])


def crear_blastoise():
    return Pokemon("Blastoise", "agua", 100, [
        Movimiento("Pistola Agua", "agua", 40, 25),
        Movimiento("Hidrobomba", "agua", 70, 5),
        Movimiento("Placaje", "normal", 30, 35),
        Movimiento("Rayo Burbuja", "agua", 45, 20),
    ])


def crear_venusaur():
    return Pokemon("Venusaur", "planta", 100, [
        Movimiento("Látigo Cepa", "planta", 40, 25),
        Movimiento("Rayo Solar", "planta", 70, 5),
        Movimiento("Polvo Veneno", "planta", 10, 20, efecto=estados.ENVENENADO, prob_efecto=0.6),
        Movimiento("Somnífero", "planta", 5, 10, efecto=estados.DORMIDO, prob_efecto=0.7),
    ])


def crear_snorlax():
    return Pokemon("Snorlax", "normal", 130, [
        Movimiento("Placaje", "normal", 35, 30),
        Movimiento("Golpe Cuerpo", "normal", 55, 15, efecto=estados.PARALIZADO, prob_efecto=0.2),
        Movimiento("Bostezo", "normal", 5, 10, efecto=estados.DORMIDO, prob_efecto=0.5),
        Movimiento("Hiperrayo", "normal", 75, 5),
    ])


# Diccionario nombre -> función creadora, para los menús.
ROSTER = {
    "Pikachu": crear_pikachu,
    "Charizard": crear_charizard,
    "Blastoise": crear_blastoise,
    "Venusaur": crear_venusaur,
    "Snorlax": crear_snorlax,
}


def crear(nombre):
    """Crea un Pokémon del roster por nombre, o None si no existe."""
    creadora = ROSTER.get(nombre)
    return creadora() if creadora else None
