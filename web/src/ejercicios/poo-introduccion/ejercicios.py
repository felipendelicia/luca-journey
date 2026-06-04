"""✏️ Ejercicios — POO: Introducción

Vas a construir, paso a paso, una clase Pokemon y una clase Entrenador.
Implementá cada método siguiendo el comentario que tiene arriba. ✅ Corregir al terminar.
"""


# Clase Pokémon
# Construí la clase Pokemon: guarda nombre, tipo, nivel y HP, y sabe atacar, recibir
# daño, curarse, subir de nivel y compararse. Implementá los 10 métodos de abajo.
class Pokemon:
    """Un Pokémon con nombre, tipo, nivel y HP."""

    # __init__: guardá nombre, tipo y nivel como atributos.
    # Además creá self.hp = 100 y self.hp_max = 100.
    def __init__(self, nombre, tipo, nivel):
        # TU CÓDIGO ACÁ
        pass

    # __str__: devolvé "<nombre> (<tipo>, Nivel <nivel>)".
    # Ejemplo:  str(p)  →  "Pikachu (Electrico, Nivel 25)"
    def __str__(self):
        # TU CÓDIGO ACÁ
        pass

    # __repr__: devolvé "Pokemon('<nombre>', '<tipo>', <nivel>)".
    # Ejemplo:  repr(p)  →  "Pokemon('Pikachu', 'Electrico', 25)"
    def __repr__(self):
        # TU CÓDIGO ACÁ
        pass

    # atacar(): devolvé "<nombre> ataca con un golpe de tipo <tipo>!".
    def atacar(self):
        # TU CÓDIGO ACÁ
        pass

    # recibir_dano(cantidad): bajá self.hp en 'cantidad', sin que quede negativo.
    def recibir_dano(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # esta_debilitado(): devolvé True si self.hp es 0 o menos.
    def esta_debilitado(self):
        # TU CÓDIGO ACÁ
        pass

    # curar(cantidad): subí self.hp en 'cantidad', sin pasar self.hp_max.
    def curar(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # subir_nivel(): sumá 1 a self.nivel.
    def subir_nivel(self):
        # TU CÓDIGO ACÁ
        pass

    # es_mas_fuerte_que(otro): devolvé True si self.nivel > otro.nivel.
    def es_mas_fuerte_que(self, otro):
        # TU CÓDIGO ACÁ
        pass

    # porcentaje_hp(): devolvé el HP como porcentaje entero del máximo.
    # Ejemplo:  hp=50, hp_max=100  →  50
    def porcentaje_hp(self):
        # TU CÓDIGO ACÁ
        pass


# Clase Entrenador
# Un Entrenador con un nombre y un equipo de objetos Pokemon. Implementá los 7 métodos.
class Entrenador:
    """Un Entrenador con un nombre y un equipo de Pokémon."""

    # __init__: guardá self.nombre y creá self.equipo = [] (lista vacía).
    def __init__(self, nombre):
        # TU CÓDIGO ACÁ
        pass

    # agregar(pokemon): agregá el objeto pokemon a self.equipo.
    def agregar(self, pokemon):
        # TU CÓDIGO ACÁ
        pass

    # cantidad(): devolvé cuántos Pokémon tiene el equipo.
    def cantidad(self):
        # TU CÓDIGO ACÁ
        pass

    # tiene_equipo(): devolvé True si el equipo tiene al menos un Pokémon.
    def tiene_equipo(self):
        # TU CÓDIGO ACÁ
        pass

    # nombres(): devolvé una lista con el nombre de cada Pokémon del equipo.
    def nombres(self):
        # TU CÓDIGO ACÁ
        pass

    # nivel_total(): devolvé la suma de los niveles de todos los Pokémon.
    def nivel_total(self):
        # TU CÓDIGO ACÁ
        pass

    # el_mas_fuerte(): devolvé el objeto Pokemon con el nivel más alto.
    # Si el equipo está vacío, devolvé None.
    def el_mas_fuerte(self):
        # TU CÓDIGO ACÁ
        pass


# Tu Pokémon inicial
# Devolvé un objeto Pokemon: "Pikachu", tipo "Electrico", nivel 5.
# Ejemplo:  crear_pokemon_inicial().nombre  →  "Pikachu"
def crear_pokemon_inicial():
    """Devolvé un Pokemon Pikachu nivel 5."""
    # TU CÓDIGO ACÁ
    pass


# ¡A batallar!
# El atacante le hace 'dano' al defensor (usá recibir_dano). Devolvé True si el
# defensor quedó debilitado, False si no.
# Ejemplo:  un defensor con 100 HP y dano=100  →  batallar(...)  →  True
def batallar(atacante, defensor, dano):
    """Aplicá daño al defensor y devolvé si quedó debilitado."""
    # TU CÓDIGO ACÁ
    pass


# Contar debilitados
# 'equipo' es una lista de objetos Pokemon. Devolvé cuántos están debilitados.
# Ejemplo:  un equipo con 2 Pokémon en 0 HP  →  contar_debilitados(equipo)  →  2
def contar_debilitados(equipo):
    """Devolvé cuántos Pokémon de la lista están debilitados."""
    # TU CÓDIGO ACÁ
    pass
