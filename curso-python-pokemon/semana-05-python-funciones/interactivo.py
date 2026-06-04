#!/usr/bin/env python3
"""
🧮 Calculadora de Estadísticas Pokémon — Semana 05

Un menú con varias calculadoras. Vos ingresás valores y la app te muestra el
resultado. Todo está armado con FUNCIONES (el tema de la semana).

Cómo jugar:
    python interactivo.py
"""


# ======================================================================
#  Las funciones de cálculo (puras, testeables).
# ======================================================================
def calcular_dano(ataque, defensa, es_super=False):
    """Daño = ataque - defensa, x2 si es súper efectivo. Mínimo 1 si hay golpe."""
    base = ataque - defensa
    if base < 1:
        base = 1
    if es_super:
        base = base * 2
    return base


def velocidad_efectiva(velocidad_base, nivel, paralizado=False):
    """Velocidad efectiva = base + nivel*2; si está paralizado, se reduce a la mitad."""
    efectiva = velocidad_base + nivel * 2
    if paralizado:
        efectiva = efectiva // 2
    return efectiva


def nivel_desde_experiencia(exp):
    """Cada 100 de experiencia = 1 nivel. Mínimo nivel 1."""
    nivel = exp // 100
    if nivel < 1:
        nivel = 1
    return nivel


def hp_maximo(hp_base, nivel):
    """Fórmula simplificada de HP máximo según el nivel."""
    return hp_base + (nivel * 2) + 10


def pedir_entero(mensaje):
    """Pide un número entero al usuario, reintentando si se equivoca."""
    while True:
        try:
            return int(input(mensaje))
        except ValueError:
            print("   ⚠️ Escribí un número entero válido.")
        except (EOFError, KeyboardInterrupt):
            raise


# ======================================================================
#  El menú interactivo.
# ======================================================================
def jugar():
    print("=" * 50)
    print("🧮  CALCULADORA DE ESTADÍSTICAS POKÉMON — Semana 05")
    print("=" * 50)

    while True:
        print("\n¿Qué querés calcular?")
        print("   1) Daño de un ataque")
        print("   2) Velocidad efectiva")
        print("   3) Nivel a partir de experiencia")
        print("   4) HP máximo")
        print("   5) Salir")

        try:
            opcion = input("Elegí una opción > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return

        if opcion == "1":
            ataque = pedir_entero("   Ataque del atacante: ")
            defensa = pedir_entero("   Defensa del rival: ")
            sup = input("   ¿Es súper efectivo? (s/n): ").strip().lower()
            es_super = sup.startswith("s")
            dano = calcular_dano(ataque, defensa, es_super)
            print(f"   💥 Daño calculado: {dano}")

        elif opcion == "2":
            base = pedir_entero("   Velocidad base: ")
            nivel = pedir_entero("   Nivel: ")
            par = input("   ¿Está paralizado? (s/n): ").strip().lower()
            paralizado = par.startswith("s")
            vel = velocidad_efectiva(base, nivel, paralizado)
            print(f"   🏃 Velocidad efectiva: {vel}")

        elif opcion == "3":
            exp = pedir_entero("   Experiencia acumulada: ")
            nivel = nivel_desde_experiencia(exp)
            print(f"   ⭐ Nivel: {nivel}")

        elif opcion == "4":
            hp_base = pedir_entero("   HP base: ")
            nivel = pedir_entero("   Nivel: ")
            hp = hp_maximo(hp_base, nivel)
            print(f"   ❤️ HP máximo: {hp}")

        elif opcion == "5":
            print("¡Hasta la próxima, Entrenador! 👋")
            return

        else:
            print("   ⚠️ Opción no válida. Elegí del 1 al 5.")


if __name__ == "__main__":
    jugar()
