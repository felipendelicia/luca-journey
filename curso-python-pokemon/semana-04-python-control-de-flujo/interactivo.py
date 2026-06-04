#!/usr/bin/env python3
"""
⚔️ Simulador de Batalla por Turnos — Semana 04

Una batalla entre tu Pikachu y un Onix salvaje. Cada turno elegís un ataque
(con input()) y se muestra el desarrollo hasta que uno de los dos se debilita.

Cómo jugar:
    python interactivo.py

La lógica de daño y estado vive en funciones puras (testeables). La parte
aleatoria y el input() están en jugar().
"""

import random


# Tabla de ataques: nombre -> (daño_minimo, daño_maximo)
ATAQUES_PIKACHU = {
    "1": ("Impactrueno", 18, 28),
    "2": ("Ataque Rápido", 10, 16),
    "3": ("Rayo", 22, 35),
}

ATAQUES_ONIX = {
    "Lanzarrocas": (15, 25),
    "Placaje": (8, 14),
    "Atadura": (12, 20),
}


def aplicar_dano(hp, dano):
    """
    Devuelve el HP resultante después de recibir 'dano'.
    Nunca baja de 0 (un Pokémon no tiene HP negativo).
    """
    nuevo = hp - dano
    if nuevo < 0:
        nuevo = 0
    return nuevo


def esta_debilitado(hp):
    """Devuelve True si el Pokémon se debilitó (HP llegó a 0)."""
    return hp <= 0


def barra_hp(hp, hp_max, largo=20):
    """
    Devuelve una barra de vida en texto, ej: [██████░░░░] 60/100
    """
    if hp_max <= 0:
        hp_max = 1
    # Calculamos cuántos bloques llenos mostrar, proporcional al HP.
    llenos = int((hp / hp_max) * largo)
    if llenos < 0:
        llenos = 0
    vacios = largo - llenos
    return f"[{'█' * llenos}{'░' * vacios}] {hp}/{hp_max}"


def jugar():
    print("=" * 50)
    print("⚔️  BATALLA POKÉMON — Semana 04")
    print("=" * 50)
    print("¡Un Onix salvaje apareció!\n")

    hp_max = 100
    hp_pikachu = hp_max
    hp_onix = hp_max

    turno = 1
    while not esta_debilitado(hp_pikachu) and not esta_debilitado(hp_onix):
        print(f"\n----- TURNO {turno} -----")
        print(f"⚡ Pikachu  {barra_hp(hp_pikachu, hp_max)}")
        print(f"🪨 Onix     {barra_hp(hp_onix, hp_max)}")
        print("\nElegí tu ataque:")
        for clave, (nombre, dmin, dmax) in ATAQUES_PIKACHU.items():
            print(f"   {clave}) {nombre} ({dmin}-{dmax} de daño)")

        # Pedimos un ataque válido.
        eleccion = None
        while eleccion not in ATAQUES_PIKACHU:
            try:
                eleccion = input("   Tu ataque > ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n¡Huiste de la batalla! 🏃")
                return
            if eleccion not in ATAQUES_PIKACHU:
                print("   ⚠️ Elegí 1, 2 o 3.")

        # Turno de Pikachu.
        nombre, dmin, dmax = ATAQUES_PIKACHU[eleccion]
        dano = random.randint(dmin, dmax)
        hp_onix = aplicar_dano(hp_onix, dano)
        print(f"\n⚡ ¡Pikachu usó {nombre}! Le hizo {dano} de daño a Onix.")

        if esta_debilitado(hp_onix):
            break

        # Turno de Onix (la CPU elige un ataque al azar).
        nombre_onix = random.choice(list(ATAQUES_ONIX.keys()))
        dmin_o, dmax_o = ATAQUES_ONIX[nombre_onix]
        dano_o = random.randint(dmin_o, dmax_o)
        hp_pikachu = aplicar_dano(hp_pikachu, dano_o)
        print(f"🪨 ¡Onix usó {nombre_onix}! Le hizo {dano_o} de daño a Pikachu.")

        turno += 1

    # Resultado final.
    print("\n" + "=" * 50)
    if esta_debilitado(hp_onix):
        print("🏆 ¡Onix se debilitó! ¡GANASTE LA BATALLA! ⚡")
    else:
        print("💀 ¡Pikachu se debilitó! Perdiste... ¡la próxima es tuya!")
    print("=" * 50)


if __name__ == "__main__":
    jugar()
