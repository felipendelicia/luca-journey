#!/usr/bin/env python3
"""
🎒 Gestor de Equipo Pokémon — Semana 06

Administrá tu equipo (máximo 6). Podés agregar, quitar, buscar y listar Pokémon
desde un menú. Cada Pokémon es un diccionario con nombre, tipo y nivel.

Cómo jugar:
    python interactivo.py
"""

MAX_EQUIPO = 6


class GestorEquipo:
    """Maneja la lista de Pokémon del equipo. La lógica acá es testeable."""

    def __init__(self):
        # El equipo arranca vacío. Es una lista de diccionarios.
        self.equipo = []

    def agregar(self, nombre, tipo, nivel):
        """Agrega un Pokémon. Devuelve un mensaje de resultado."""
        # Regla 1: no más de 6.
        if len(self.equipo) >= MAX_EQUIPO:
            return f"❌ El equipo está lleno (máximo {MAX_EQUIPO})."
        # Regla 2: no repetir nombres.
        if self.buscar(nombre) is not None:
            return f"❌ {nombre} ya está en el equipo."
        # Lo agregamos como diccionario.
        self.equipo.append({"nombre": nombre, "tipo": tipo, "nivel": nivel})
        return f"✅ {nombre} se unió al equipo."

    def quitar(self, nombre):
        """Quita un Pokémon por nombre. Devuelve un mensaje."""
        pokemon = self.buscar(nombre)
        if pokemon is None:
            return f"❌ {nombre} no está en el equipo."
        self.equipo.remove(pokemon)
        return f"👋 {nombre} dejó el equipo."

    def buscar(self, nombre):
        """Devuelve el diccionario del Pokémon, o None si no está."""
        # Recorremos buscando por nombre (sin importar mayúsculas/minúsculas).
        for pokemon in self.equipo:
            if pokemon["nombre"].lower() == nombre.lower():
                return pokemon
        return None

    def listar(self):
        """Devuelve una lista de strings, una por Pokémon."""
        if not self.equipo:
            return ["(equipo vacío)"]
        lineas = []
        for indice, p in enumerate(self.equipo, start=1):
            lineas.append(f"{indice}. {p['nombre']} ({p['tipo']}) - Nivel {p['nivel']}")
        return lineas

    def cantidad(self):
        """Cuántos Pokémon hay en el equipo."""
        return len(self.equipo)


def jugar():
    print("=" * 50)
    print("🎒  GESTOR DE EQUIPO POKÉMON — Semana 06")
    print("=" * 50)

    gestor = GestorEquipo()

    while True:
        print(f"\nEquipo actual ({gestor.cantidad()}/{MAX_EQUIPO}):")
        for linea in gestor.listar():
            print("   " + linea)

        print("\n¿Qué querés hacer?")
        print("   1) Agregar Pokémon")
        print("   2) Quitar Pokémon")
        print("   3) Buscar Pokémon")
        print("   4) Salir")

        try:
            opcion = input("Opción > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n¡Chau! 👋")
            return

        if opcion == "1":
            nombre = input("   Nombre: ").strip()
            tipo = input("   Tipo: ").strip()
            nivel_txt = input("   Nivel: ").strip()
            # Validamos que el nivel sea un número.
            nivel = int(nivel_txt) if nivel_txt.isdigit() else 1
            print("   " + gestor.agregar(nombre, tipo, nivel))

        elif opcion == "2":
            nombre = input("   Nombre a quitar: ").strip()
            print("   " + gestor.quitar(nombre))

        elif opcion == "3":
            nombre = input("   Nombre a buscar: ").strip()
            pokemon = gestor.buscar(nombre)
            if pokemon:
                print(f"   🔎 {pokemon['nombre']} ({pokemon['tipo']}) - Nivel {pokemon['nivel']}")
            else:
                print(f"   ❌ {nombre} no está en el equipo.")

        elif opcion == "4":
            print("¡Hasta la próxima, Entrenador! 👋")
            return

        else:
            print("   ⚠️ Opción no válida.")


if __name__ == "__main__":
    jugar()
