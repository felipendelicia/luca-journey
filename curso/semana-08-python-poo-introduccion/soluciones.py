"""
✅ Semana 08 — Soluciones: POO Introducción

Clase Pokemon, clase Entrenador y funciones. Comentadas línea por línea.
"""


class Pokemon:
    """Un Pokémon con nombre, tipo, nivel y HP."""

    # 1)
    def __init__(self, nombre, tipo, nivel):
        # 'self' es este objeto. Guardamos cada dato como atributo suyo.
        self.nombre = nombre
        self.tipo = tipo
        self.nivel = nivel
        # Todo Pokémon arranca con 100 de HP (actual y máximo).
        self.hp = 100
        self.hp_max = 100

    # 2)
    def __str__(self):
        # Texto lindo para el usuario.
        return f"{self.nombre} ({self.tipo}, Nivel {self.nivel})"

    # 3)
    def __repr__(self):
        # Texto técnico para debug. Reproduce cómo se creó el objeto.
        return f"Pokemon('{self.nombre}', '{self.tipo}', {self.nivel})"

    # 4)
    def atacar(self):
        return f"{self.nombre} ataca con un golpe de tipo {self.tipo}!"

    # 5)
    def recibir_dano(self, cantidad):
        # Bajamos el HP.
        self.hp = self.hp - cantidad
        # El HP nunca queda negativo.
        if self.hp < 0:
            self.hp = 0

    # 6)
    def esta_debilitado(self):
        return self.hp <= 0

    # 7)
    def curar(self, cantidad):
        # Subimos el HP.
        self.hp = self.hp + cantidad
        # No puede superar el máximo.
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    # 8)
    def subir_nivel(self):
        self.nivel = self.nivel + 1

    # 9)
    def es_mas_fuerte_que(self, otro):
        # Comparamos el nivel de este Pokémon con el del otro objeto.
        return self.nivel > otro.nivel

    # 10)
    def porcentaje_hp(self):
        # Regla de tres simple: hp sobre hp_max, por 100.
        return int((self.hp / self.hp_max) * 100)


class Entrenador:
    """Un Entrenador con nombre y un equipo de objetos Pokemon."""

    # 11)
    def __init__(self, nombre):
        self.nombre = nombre
        # El equipo arranca vacío.
        self.equipo = []

    # 12)
    def agregar(self, pokemon):
        self.equipo.append(pokemon)

    # 13)
    def cantidad(self):
        return len(self.equipo)

    # 14)
    def tiene_equipo(self):
        return len(self.equipo) > 0

    # 15)
    def nombres(self):
        # Por cada Pokémon del equipo, sacamos su atributo nombre.
        return [pokemon.nombre for pokemon in self.equipo]

    # 16)
    def nivel_total(self):
        total = 0
        for pokemon in self.equipo:
            total = total + pokemon.nivel
        return total

    # 17)
    def el_mas_fuerte(self):
        # Si no hay nadie, devolvemos None.
        if len(self.equipo) == 0:
            return None
        # Asumimos que el primero es el más fuerte y comparamos con el resto.
        mejor = self.equipo[0]
        for pokemon in self.equipo:
            if pokemon.nivel > mejor.nivel:
                mejor = pokemon
        return mejor


# ----------------------------------------------------------------------
# Funciones que usan objetos Pokemon.
# ----------------------------------------------------------------------

# 18)
def crear_pokemon_inicial():
    """Pikachu nivel 5."""
    # Creamos y devolvemos un objeto Pokemon.
    return Pokemon("Pikachu", "Electrico", 5)


# 19)
def batallar(atacante, defensor, dano):
    """El atacante daña al defensor; devolvemos si quedó debilitado."""
    # Reusamos el método del objeto para aplicar el daño.
    defensor.recibir_dano(dano)
    # Y consultamos su estado con otro método.
    return defensor.esta_debilitado()


# 20)
def contar_debilitados(equipo):
    """Contá los Pokémon debilitados de la lista."""
    cantidad = 0
    for pokemon in equipo:
        if pokemon.esta_debilitado():
            cantidad = cantidad + 1
    return cantidad
