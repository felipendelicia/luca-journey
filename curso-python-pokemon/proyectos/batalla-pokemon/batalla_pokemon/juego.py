"""
batalla_pokemon.juego — La interfaz de consola del simulador de batalla.

Dos modos:
  - vs CPU: peleás contra la computadora.
  - vs Jugador: dos personas en la misma terminal, por turnos.
"""

import random

from . import datos
from .batalla import Batalla, elegir_movimiento_cpu


def barra_hp(pokemon, largo=20):
    """Barra de HP en texto."""
    llenos = int((pokemon.hp / pokemon.hp_max) * largo) if pokemon.hp_max else 0
    llenos = max(0, min(largo, llenos))
    estado = f" [{pokemon.estado}]" if pokemon.estado else ""
    return f"{pokemon.nombre:<12} [{'█' * llenos}{'░' * (largo - llenos)}] {pokemon.hp}/{pokemon.hp_max}{estado}"


def mostrar_tablero(p1, p2):
    print("\n" + "-" * 50)
    print("  " + barra_hp(p1))
    print("  " + barra_hp(p2))
    print("-" * 50)


def elegir_pokemon(quien):
    """Menú para que un jugador elija su Pokémon. Devuelve un Pokémon nuevo."""
    nombres = list(datos.ROSTER.keys())
    print(f"\n{quien}, elegí tu Pokémon:")
    for i, nombre in enumerate(nombres, start=1):
        print(f"   {i}) {nombre}")
    while True:
        eleccion = input("   Opción > ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(nombres):
            return datos.crear(nombres[int(eleccion) - 1])
        print("   ⚠️ Elegí un número válido.")


def elegir_movimiento(pokemon):
    """Menú de movimientos para el jugador. Devuelve el índice elegido."""
    print(f"\n  Movimientos de {pokemon.nombre}:")
    for i, m in enumerate(pokemon.movimientos):
        estado = "" if m.usable() else " (sin PP)"
        print(f"   {i + 1}) {m.nombre} [{m.tipo}] poder {m.poder} — PP {m.pp}/{m.pp_max}{estado}")
    while True:
        eleccion = input("   Tu movimiento > ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(pokemon.movimientos):
            indice = int(eleccion) - 1
            if pokemon.movimientos[indice].usable():
                return indice
            print("   ⚠️ Ese movimiento no tiene PP.")
        else:
            print("   ⚠️ Elegí un número válido.")


def _imprimir(mensajes):
    for m in mensajes:
        print("  " + m)


def jugar_partida(p1, p2, controlador_p1, controlador_p2):
    """
    Corre la batalla completa. 'controlador_pX' es una función que recibe el
    Pokémon atacante y devuelve el índice del movimiento (jugador o CPU).
    """
    batalla = Batalla(p1, p2)
    turno = 1
    while not batalla.terminada():
        mostrar_tablero(p1, p2)
        print(f"\n===== TURNO {turno} =====")

        # Turno del jugador 1.
        idx = controlador_p1(p1)
        if idx is not None:
            _imprimir(batalla.ejecutar_movimiento(p1, p2, idx))
        if batalla.terminada():
            break

        # Turno del jugador 2.
        idx = controlador_p2(p2)
        if idx is not None:
            _imprimir(batalla.ejecutar_movimiento(p2, p1, idx))

        # Daño de estados al final del turno.
        _imprimir(batalla.fin_de_turno(p1))
        _imprimir(batalla.fin_de_turno(p2))
        turno += 1

    ganador = batalla.ganador()
    print("\n" + "=" * 50)
    if ganador:
        print(f"🏆 ¡{ganador.nombre} ganó la batalla!")
    else:
        print("🤝 ¡Empate!")
    print("=" * 50)


def jugar_vs_cpu():
    print("\n🤖 MODO: vs CPU")
    jugador = elegir_pokemon("Jugador")
    # La CPU elige al azar.
    cpu = datos.crear(random.choice(list(datos.ROSTER.keys())))
    print(f"\nLa CPU eligió a {cpu.nombre}!")

    jugar_partida(
        jugador, cpu,
        controlador_p1=lambda p: elegir_movimiento(p),
        controlador_p2=lambda p: elegir_movimiento_cpu(p),
    )


def jugar_vs_jugador():
    print("\n👥 MODO: vs Jugador (misma terminal)")
    p1 = elegir_pokemon("Jugador 1")
    p2 = elegir_pokemon("Jugador 2")

    def turno_humano(etiqueta):
        def controlador(p):
            print(f"\n>>> Turno de {etiqueta} ({p.nombre})")
            return elegir_movimiento(p)
        return controlador

    jugar_partida(
        p1, p2,
        controlador_p1=turno_humano("Jugador 1"),
        controlador_p2=turno_humano("Jugador 2"),
    )


def run():
    print("=" * 50)
    print("⚔️  SIMULADOR DE BATALLA POKÉMON")
    print("=" * 50)
    while True:
        print("\nModos de juego:")
        print("   1) vs CPU")
        print("   2) vs Jugador (misma terminal)")
        print("   3) Salir")
        try:
            opcion = input("Elegí > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return
        if opcion == "1":
            jugar_vs_cpu()
        elif opcion == "2":
            jugar_vs_jugador()
        elif opcion == "3":
            print("¡Hasta la próxima, Entrenador! 👋")
            return
        else:
            print("⚠️ Opción no válida.")


if __name__ == "__main__":
    run()
