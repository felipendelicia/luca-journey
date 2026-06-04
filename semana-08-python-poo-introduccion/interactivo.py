#!/usr/bin/env python3
"""
🛠️ Creador de Pokémon Personalizado — Semana 08

Definí los datos de tu propio Pokémon (nombre, tipo, stats) y el programa crea
un OBJETO de la clase PokemonPersonalizado y muestra su ficha formateada.

Cómo jugar:
    python interactivo.py
"""


class PokemonPersonalizado:
    """Un Pokémon creado por el usuario, con stats completos."""

    def __init__(self, nombre, tipo, ataque, defensa, velocidad):
        self.nombre = nombre
        self.tipo = tipo
        self.ataque = ataque
        self.defensa = defensa
        self.velocidad = velocidad

    def total_stats(self):
        """Suma de los tres stats principales."""
        return self.ataque + self.defensa + self.velocidad

    def categoria(self):
        """Clasifica al Pokémon según su total de stats."""
        total = self.total_stats()
        if total >= 240:
            return "Legendario"
        elif total >= 150:
            return "Fuerte"
        else:
            return "Comun"

    def ficha(self):
        """Devuelve la ficha del Pokémon como ASCII art (string)."""

        def barra(valor, maximo=100, largo=10):
            # Una barrita visual proporcional al valor del stat.
            llenos = int((valor / maximo) * largo)
            if llenos > largo:
                llenos = largo
            if llenos < 0:
                llenos = 0
            return "█" * llenos + "░" * (largo - llenos)

        return f"""
┌────────────────────────────────┐
│  POKÉMON: {self.nombre[:20]:<20} │
│  TIPO:    {self.tipo[:20]:<20} │
├────────────────────────────────┤
│  Ataque    {barra(self.ataque)} {self.ataque:>3} │
│  Defensa   {barra(self.defensa)} {self.defensa:>3} │
│  Velocidad {barra(self.velocidad)} {self.velocidad:>3} │
├────────────────────────────────┤
│  Total: {self.total_stats():>3}   Categoría: {self.categoria()[:9]:<9} │
└────────────────────────────────┘
"""


def pedir_entero(mensaje, default=50):
    """Pide un entero; si el usuario escribe cualquier cosa, usa el default."""
    texto = input(mensaje).strip()
    return int(texto) if texto.isdigit() else default


def jugar():
    print("=" * 50)
    print("🛠️  CREADOR DE POKÉMON PERSONALIZADO — Semana 08")
    print("=" * 50)
    print("Diseñá tu propio Pokémon. Los stats van de 0 a 100.\n")

    try:
        nombre = input("Nombre de tu Pokémon: ").strip() or "Misterio"
        tipo = input("Tipo: ").strip() or "Normal"
        ataque = pedir_entero("Ataque (0-100): ")
        defensa = pedir_entero("Defensa (0-100): ")
        velocidad = pedir_entero("Velocidad (0-100): ")
    except (EOFError, KeyboardInterrupt):
        print("\n¡Chau! 👋")
        return

    # Creamos el OBJETO con la clase.
    pokemon = PokemonPersonalizado(nombre, tipo, ataque, defensa, velocidad)

    print("\n¡Tu Pokémon está listo!")
    print(pokemon.ficha())

    if pokemon.categoria() == "Legendario":
        print("🌟 ¡Wow! Creaste un Pokémon Legendario.")


if __name__ == "__main__":
    jugar()
