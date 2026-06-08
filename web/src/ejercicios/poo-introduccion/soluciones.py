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


def nombres_de(equipo):
    return [p.nombre for p in equipo]


def nivel_promedio(equipo):
    return sum(p.nivel for p in equipo) / len(equipo)


def hay_debilitado(equipo):
    return any(p.esta_debilitado() for p in equipo)


def curar_a_todos(equipo):
    for p in equipo:
        p.hp = p.hp_max
    return equipo


def subir_a_todos(equipo):
    for p in equipo:
        p.subir_nivel()
    return equipo


def total_hp(equipo):
    return sum(p.hp for p in equipo)


def vivos(equipo):
    return [p for p in equipo if not p.esta_debilitado()]


def ordenar_por_nivel(equipo):
    return sorted(equipo, key=lambda p: p.nivel, reverse=True)


def clonar(pokemon):
    return Pokemon(pokemon.nombre, pokemon.tipo, pokemon.nivel)


def es_del_tipo(pokemon, tipo):
    return pokemon.tipo == tipo


def contar_de_tipo(equipo, tipo):
    return sum(1 for p in equipo if p.tipo == tipo)


def crear_equipo(nombres, tipo, nivel):
    return [Pokemon(n, tipo, nivel) for n in nombres]


def promedio_hp(equipo):
    return sum(p.porcentaje_hp() for p in equipo) / len(equipo)


def el_de_nombre(equipo, nombre):
    for p in equipo:
        if p.nombre == nombre:
            return p
    return None


def mas_debil_del_equipo(equipo):
    if not equipo:
        return None
    return min(equipo, key=lambda p: p.nivel)
