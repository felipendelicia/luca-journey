"""
✏️ Semana 08 — Ejercicios: POO Introducción

Vas a construir, paso a paso, una clase Pokemon (de básica a con batalla) y una
clase Entrenador. Completá donde dice '# TU CÓDIGO ACÁ'.

Los 20 ejercicios están numerados en los comentarios. Respuestas en soluciones.py.
Para probar tu trabajo: en test_ejercicios.py cambiá _cargar("soluciones")
por _cargar("ejercicios").
"""


class Pokemon:
    """Un Pokémon con nombre, tipo, nivel y HP."""

    # 1) En __init__, guardá nombre, tipo y nivel como atributos.
    #    Además, creá self.hp = 100 y self.hp_max = 100.
    def __init__(self, nombre, tipo, nivel):
        # TU CÓDIGO ACÁ
        pass

    # 2) __str__: devolvé "<nombre> (<tipo>, Nivel <nivel>)".
    #    Ej: "Pikachu (Electrico, Nivel 25)"
    def __str__(self):
        # TU CÓDIGO ACÁ
        pass

    # 3) __repr__: devolvé "Pokemon('<nombre>', '<tipo>', <nivel>)".
    #    Ej: "Pokemon('Pikachu', 'Electrico', 25)"
    def __repr__(self):
        # TU CÓDIGO ACÁ
        pass

    # 4) atacar(): devolvé "<nombre> ataca con un golpe de tipo <tipo>!".
    def atacar(self):
        # TU CÓDIGO ACÁ
        pass

    # 5) recibir_dano(cantidad): bajá self.hp en 'cantidad', sin que quede negativo.
    def recibir_dano(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # 6) esta_debilitado(): devolvé True si self.hp es 0 o menos.
    def esta_debilitado(self):
        # TU CÓDIGO ACÁ
        pass

    # 7) curar(cantidad): subí self.hp en 'cantidad', sin pasar self.hp_max.
    def curar(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # 8) subir_nivel(): sumá 1 a self.nivel.
    def subir_nivel(self):
        # TU CÓDIGO ACÁ
        pass

    # 9) es_mas_fuerte_que(otro): devolvé True si self.nivel > otro.nivel.
    def es_mas_fuerte_que(self, otro):
        # TU CÓDIGO ACÁ
        pass

    # 10) porcentaje_hp(): devolvé el HP como porcentaje entero del máximo.
    #     Ej: hp=50, hp_max=100 -> 50. hp=100 -> 100.
    def porcentaje_hp(self):
        # TU CÓDIGO ACÁ
        pass


class Entrenador:
    """Un Entrenador con un nombre y un equipo de Pokémon (objetos Pokemon)."""

    # 11) __init__: guardá self.nombre y creá self.equipo = [] (lista vacía).
    def __init__(self, nombre):
        # TU CÓDIGO ACÁ
        pass

    # 12) agregar(pokemon): agregá el objeto pokemon a self.equipo.
    def agregar(self, pokemon):
        # TU CÓDIGO ACÁ
        pass

    # 13) cantidad(): devolvé cuántos Pokémon tiene el equipo.
    def cantidad(self):
        # TU CÓDIGO ACÁ
        pass

    # 14) tiene_equipo(): devolvé True si el equipo tiene al menos un Pokémon.
    def tiene_equipo(self):
        # TU CÓDIGO ACÁ
        pass

    # 15) nombres(): devolvé una lista con el nombre de cada Pokémon del equipo.
    def nombres(self):
        # TU CÓDIGO ACÁ
        pass

    # 16) nivel_total(): devolvé la suma de los niveles de todos los Pokémon.
    def nivel_total(self):
        # TU CÓDIGO ACÁ
        pass

    # 17) el_mas_fuerte(): devolvé el objeto Pokemon con el nivel más alto.
    #     Si el equipo está vacío, devolvé None.
    def el_mas_fuerte(self):
        # TU CÓDIGO ACÁ
        pass


# ----------------------------------------------------------------------
# Funciones que usan objetos Pokemon.
# ----------------------------------------------------------------------

# 18) crear_pokemon_inicial(): devolvé un objeto Pokemon "Pikachu", "Electrico", nivel 5.
def crear_pokemon_inicial():
    """Devolvé un Pokemon Pikachu nivel 5."""
    # TU CÓDIGO ACÁ
    pass


# 19) batallar(atacante, defensor, dano): el atacante le hace 'dano' al defensor.
#     Devolvé True si el defensor quedó debilitado, False si no.
def batallar(atacante, defensor, dano):
    """Aplicá daño al defensor y devolvé si quedó debilitado."""
    # TU CÓDIGO ACÁ
    pass


# 20) contar_debilitados(equipo): recibí una lista de objetos Pokemon y devolvé
#     cuántos están debilitados.
def contar_debilitados(equipo):
    """Devolvé cuántos Pokémon de la lista están debilitados."""
    # TU CÓDIGO ACÁ
    pass
