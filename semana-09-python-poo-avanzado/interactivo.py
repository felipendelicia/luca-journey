#!/usr/bin/env python3
"""
🔥💧🌿⚡ Sistema de Tipos Pokémon — Semana 09

Una jerarquía de clases por tipo. Elegís tu Pokémon y el rival, y se simula una
batalla donde las VENTAJAS de tipo importan: Fuego>Planta, Agua>Fuego, etc.

Cómo jugar:
    python interactivo.py
"""

import random
from abc import ABC, abstractmethod


class Pokemon(ABC):
    """Base abstracta de todos los Pokémon del sistema de tipos."""

    tipo = "Normal"          # cada subclase lo redefine
    emoji = "❓"

    def __init__(self, nombre):
        self.nombre = nombre
        self.hp = 100

    @abstractmethod
    def nombre_ataque(self):
        """Cada tipo tiene su ataque característico."""
        ...

    def recibir_dano(self, cantidad):
        self.hp = self.hp - cantidad
        if self.hp < 0:
            self.hp = 0

    def esta_debilitado(self):
        return self.hp <= 0


class Fuego(Pokemon):
    tipo = "Fuego"
    emoji = "🔥"

    def nombre_ataque(self):
        return "Lanzallamas"


class Agua(Pokemon):
    tipo = "Agua"
    emoji = "💧"

    def nombre_ataque(self):
        return "Hidrobomba"


class Planta(Pokemon):
    tipo = "Planta"
    emoji = "🌿"

    def nombre_ataque(self):
        return "Rayo Solar"


class Electrico(Pokemon):
    tipo = "Electrico"
    emoji = "⚡"

    def nombre_ataque(self):
        return "Rayo"


# Mapa de tipo -> clase, para crear Pokémon a partir de una opción del menú.
TIPOS = {
    "1": ("Fuego", Fuego),
    "2": ("Agua", Agua),
    "3": ("Planta", Planta),
    "4": ("Electrico", Electrico),
}

# Qué tipo le gana a cuál.
_VENTAJAS = {
    "Fuego": "Planta",
    "Agua": "Fuego",
    "Planta": "Agua",
    "Electrico": "Agua",
}


def efectividad(tipo_atacante, tipo_defensor):
    """Devuelve el multiplicador y un texto descriptivo de la efectividad."""
    if _VENTAJAS.get(tipo_atacante) == tipo_defensor:
        return 2.0, "¡Es súper efectivo! 💥"
    if _VENTAJAS.get(tipo_defensor) == tipo_atacante:
        return 0.5, "No es muy efectivo... 😐"
    return 1.0, "Efectividad normal."


def calcular_dano(tipo_atacante, tipo_defensor, base):
    """Daño final = base * multiplicador de efectividad (entero)."""
    mult, _ = efectividad(tipo_atacante, tipo_defensor)
    return int(base * mult)


def elegir_pokemon(rol):
    """Pide al usuario elegir un tipo y devuelve un objeto Pokemon."""
    print(f"\nElegí el tipo de {rol}:")
    for clave, (nombre_tipo, _) in TIPOS.items():
        print(f"   {clave}) {nombre_tipo}")
    eleccion = None
    while eleccion not in TIPOS:
        eleccion = input("   Opción > ").strip()
        if eleccion not in TIPOS:
            print("   ⚠️ Elegí 1, 2, 3 o 4.")
    nombre_tipo, clase = TIPOS[eleccion]
    nombre = input(f"   Nombre de tu {nombre_tipo}: ").strip() or nombre_tipo
    return clase(nombre)


def jugar():
    print("=" * 55)
    print("🔥💧🌿⚡  SISTEMA DE TIPOS POKÉMON — Semana 09")
    print("=" * 55)
    print("Ventajas: Fuego>Planta, Agua>Fuego, Planta>Agua, Electrico>Agua")

    try:
        jugador = elegir_pokemon("TU Pokémon")
        rival = elegir_pokemon("el RIVAL")
    except (EOFError, KeyboardInterrupt):
        print("\n¡Chau! 👋")
        return

    print(f"\n¡{jugador.nombre} {jugador.emoji} vs {rival.nombre} {rival.emoji}!")

    turno = 1
    while not jugador.esta_debilitado() and not rival.esta_debilitado():
        print(f"\n----- TURNO {turno} -----")
        print(f"{jugador.emoji} {jugador.nombre}: {jugador.hp} HP")
        print(f"{rival.emoji} {rival.nombre}: {rival.hp} HP")

        try:
            input("Presioná Enter para atacar...")
        except (EOFError, KeyboardInterrupt):
            print("\n¡Huiste! 🏃")
            return

        # Ataque del jugador.
        base = random.randint(20, 30)
        mult, texto = efectividad(jugador.tipo, rival.tipo)
        dano = int(base * mult)
        rival.recibir_dano(dano)
        print(f"{jugador.emoji} {jugador.nombre} usa {jugador.nombre_ataque()}! {texto}")
        print(f"   Le hizo {dano} de daño a {rival.nombre}.")
        if rival.esta_debilitado():
            break

        # Ataque del rival.
        base = random.randint(20, 30)
        mult, texto = efectividad(rival.tipo, jugador.tipo)
        dano = int(base * mult)
        jugador.recibir_dano(dano)
        print(f"{rival.emoji} {rival.nombre} usa {rival.nombre_ataque()}! {texto}")
        print(f"   Le hizo {dano} de daño a {jugador.nombre}.")

        turno += 1

    print("\n" + "=" * 55)
    if rival.esta_debilitado():
        print(f"🏆 ¡{jugador.nombre} ganó la batalla!")
    else:
        print(f"💀 {jugador.nombre} fue derrotado. ¡La próxima!")
    print("=" * 55)


if __name__ == "__main__":
    jugar()
