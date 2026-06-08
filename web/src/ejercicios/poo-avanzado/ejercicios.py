"""✏️ Ejercicios — POO: Avanzado

Herencia, polimorfismo, properties y métodos estáticos/de clase. Construís una
clase abstracta Pokemon y sus hijas por tipo. ✅ Corregir al terminar.
"""

from abc import ABC, abstractmethod


# Clase base abstracta
# Pokemon abstracta (no se instancia directo): HP con property (getter + setter que
# valida 0..hp_max), un método abstracto, uno estático y uno de clase. Implementá los 8.
class Pokemon(ABC):
    """Clase abstracta base."""

    # __init__: guardá nombre y nivel. Creá self._hp = 100 y self.hp_max = 100.
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    # Propiedad hp (getter): devolvé self._hp.
    @property
    def hp(self):
        # TU CÓDIGO ACÁ
        pass

    # Setter de hp: guardá el valor en self._hp, nunca menor a 0 ni mayor a self.hp_max.
    @hp.setter
    def hp(self, valor):
        # TU CÓDIGO ACÁ
        pass

    # Método abstracto atacar: las hijas DEBEN implementarlo (acá no hace nada).
    @abstractmethod
    def atacar(self):
        ...

    # recibir_dano(cantidad): restá 'cantidad' al hp (usá la propiedad, que valida).
    def recibir_dano(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # esta_debilitado(): devolvé True si self.hp es 0 o menos.
    def esta_debilitado(self):
        # TU CÓDIGO ACÁ
        pass

    # es_tipo_valido(tipo): método ESTÁTICO. True si 'tipo' está en
    # ["Fuego", "Agua", "Planta", "Electrico"].
    @staticmethod
    def es_tipo_valido(tipo):
        # TU CÓDIGO ACÁ
        pass

    # recien_nacido(nombre): método de CLASE. Devolvé una instancia nivel 1 (usá cls(nombre, 1)).
    @classmethod
    def recien_nacido(cls, nombre):
        # TU CÓDIGO ACÁ
        pass


# Subclase: Pokémon de Fuego
# Hereda de Pokemon. En __init__ llamá a super() y seteá self.tipo = "Fuego".
# atacar()  →  "<nombre> usa Lanzallamas!"
class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# Subclase: Pokémon de Agua
# Tipo "Agua".  atacar()  →  "<nombre> usa Pistola Agua!"
class PokemonAgua(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# Subclase: Pokémon de Planta
# Tipo "Planta".  atacar()  →  "<nombre> usa Latigo Cepa!"
class PokemonPlanta(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# Subclase: Pokémon Eléctrico
# Tipo "Electrico".  atacar()  →  "<nombre> usa Impactrueno!"
class PokemonElectrico(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# Reglas de ventaja:  Fuego→Planta · Agua→Fuego · Planta→Agua · Electrico→Agua

# ¿Tiene ventaja?
# Recibís dos objetos Pokemon. Devolvé True si el tipo del atacante le gana al del defensor.
# Ejemplo:  un PokemonAgua vs un PokemonFuego  →  tiene_ventaja(agua, fuego)  →  True
def tiene_ventaja(atacante, defensor):
    """Devolvé True si atacante tiene ventaja de tipo sobre defensor."""
    # TU CÓDIGO ACÁ
    pass


# Multiplicador de daño
# Devolvé 2.0 si el atacante tiene ventaja, 0.5 si el defensor la tiene sobre el atacante,
# y 1.0 en cualquier otro caso.
# Ejemplo:  agua vs fuego  →  2.0   ·   fuego vs agua  →  0.5
def multiplicador(atacante, defensor):
    """Devolvé el multiplicador de daño según las ventajas."""
    # TU CÓDIGO ACÁ
    pass


# Describir ataques (polimorfismo)
# 'equipo' es una lista de Pokemon de distintos tipos. Devolvé la lista con el resultado
# de atacar() de cada uno (¡cada tipo ataca distinto!).
# Ejemplo:  [PokemonFuego("Vulpix",5)]  →  ["Vulpix usa Lanzallamas!"]
def describir_ataques(equipo):
    """Devolvé la lista de strings de atacar() de cada Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# Fábrica por tipo
# Devolvé una instancia de la subclase correcta según 'tipo' ("Fuego"→PokemonFuego, etc.).
# Si el tipo no es válido, devolvé None.
# Ejemplo:  crear_por_tipo("Agua", "Squirtle", 5)  →  un PokemonAgua
def crear_por_tipo(tipo, nombre, nivel):
    """Devolvé la instancia de la subclase correcta según 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# Tipos del equipo
# Devolvé una lista con el .tipo de cada Pokémon del equipo.
# Ejemplo:  [PokemonFuego(...), PokemonAgua(...)]  →  ["Fuego", "Agua"]
def tipos_del_equipo(equipo):
    """Devolvé los tipos de cada Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# ¿Equipo balanceado?
# Devolvé True si TODOS los Pokémon son de tipos distintos (sin repetidos).
# Ejemplo:  tipos ["Fuego","Agua"]  →  True   ·   ["Fuego","Fuego"]  →  False
def equipo_balanceado(equipo):
    """Devolvé True si no hay tipos repetidos."""
    # TU CÓDIGO ACÁ
    pass


# Batalla simple
# 'a' ataca a 'b' con 'dano', multiplicado por la ventaja de tipo. Aplicá ese daño a 'b'
# y devolvé el daño final (int) aplicado.
# Ejemplo:  agua ataca a fuego con dano=20  →  daño final 40 (×2 por ventaja)
def batalla_simple(a, b, dano):
    """Aplicá daño con ventaja de tipo a 'b' y devolvé el daño final (int)."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos de un tipo
# Devolvé cuántos Pokémon del equipo son del 'tipo' dado.
# Ejemplo:  equipo con 2 de Fuego  →  cantidad_por_tipo(equipo, "Fuego")  →  2
def cantidad_por_tipo(equipo, tipo):
    """Devolvé cuántos Pokémon son del tipo dado."""
    # TU CÓDIGO ACÁ
    pass


# HP total del equipo
# 'equipo' es una lista de Pokémon. Devolvé la suma de los hp de todos.
# Ejemplo:  dos Pokémon recién creados (100 HP c/u)  →  total_hp(equipo)  →  200
def total_hp(equipo):
    """Devolvé la suma de los hp del equipo."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el objeto Pokémon con el nivel más alto. Si el equipo está vacío, devolvé None.
def equipo_mas_fuerte(equipo):
    """Devolvé el Pokémon de mayor nivel (o None si está vacío)."""
    # TU CÓDIGO ACÁ
    pass


# Contar por tipo
# Devolvé un diccionario {tipo: cantidad} con cuántos Pokémon hay de cada tipo.
# Ejemplo:  dos de Fuego y uno de Agua  →  {"Fuego": 2, "Agua": 1}
def contar_tipos(equipo):
    """Devolvé un dict {tipo: cantidad}."""
    # TU CÓDIGO ACÁ
    pass


# Nombres ordenados por nivel
# Devolvé una lista con los NOMBRES, del nivel más alto al más bajo.
# Ejemplo:  niveles 5, 40, 20  →  ["Alto", "Medio", "Bajo"]
def nombres_por_nivel(equipo):
    """Devolvé los nombres ordenados de mayor a menor nivel."""
    # TU CÓDIGO ACÁ
    pass


# Clonar un Pokémon
# Devolvé un Pokémon NUEVO, de la MISMA clase que el original, con su mismo nombre y nivel.
# (No copies a mano cada subclase: hay una forma de preguntarle a un objeto de qué clase es.)
def clonar(pokemon):
    """Devolvé una copia nueva del pokemon, de su misma clase."""
    # TU CÓDIGO ACÁ
    pass


# El mejor contra un rival
# Devolvé el primer Pokémon del equipo que tenga VENTAJA de tipo sobre 'defensor'.
# Si ninguno tiene ventaja, devolvé None.  (Reusá tiene_ventaja.)
def mejor_contra(equipo, defensor):
    """Devolvé el primero con ventaja sobre defensor, o None."""
    # TU CÓDIGO ACÁ
    pass


# Cuántos siguen en pie
# Devolvé cuántos Pokémon del equipo NO están debilitados.
# Ejemplo:  uno con HP y otro en 0  →  cuantos_vivos(equipo)  →  1
def cuantos_vivos(equipo):
    """Devolvé cuántos Pokémon no están debilitados."""
    # TU CÓDIGO ACÁ
    pass
