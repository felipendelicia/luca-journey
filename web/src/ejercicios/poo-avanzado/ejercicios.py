"""
✏️ Semana 09 — Ejercicios: POO Avanzado

Vas a construir una jerarquía de clases: una clase abstracta Pokemon y sus hijas
por tipo (Fuego, Agua, Planta, Eléctrico). Completá donde dice '# TU CÓDIGO ACÁ'.

Respuestas en soluciones.py. Para probar tu trabajo, en test_ejercicios.py
cambiá _cargar("soluciones") por _cargar("ejercicios").
"""

from abc import ABC, abstractmethod


class Pokemon(ABC):
    """Clase abstracta base. No se puede instanciar directamente."""

    # 1) __init__: guardá nombre y nivel. Creá self._hp = 100 y self.hp_max = 100.
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    # 2) Propiedad hp: devolvé self._hp (getter).
    @property
    def hp(self):
        # TU CÓDIGO ACÁ
        pass

    # 3) Setter de hp: guardá el valor en self._hp, pero nunca menor a 0
    #    ni mayor a self.hp_max.
    @hp.setter
    def hp(self, valor):
        # TU CÓDIGO ACÁ
        pass

    # 4) Método abstracto atacar: las hijas DEBEN implementarlo.
    @abstractmethod
    def atacar(self):
        ...

    # 5) recibir_dano(cantidad): restá 'cantidad' a self.hp (usá la propiedad,
    #    que ya valida que no baje de 0).
    def recibir_dano(self, cantidad):
        # TU CÓDIGO ACÁ
        pass

    # 6) esta_debilitado(): devolvé True si self.hp es 0 o menos.
    def esta_debilitado(self):
        # TU CÓDIGO ACÁ
        pass

    # 7) es_tipo_valido(tipo): método ESTÁTICO. Devolvé True si 'tipo' está en
    #    ["Fuego", "Agua", "Planta", "Electrico"].
    @staticmethod
    def es_tipo_valido(tipo):
        # TU CÓDIGO ACÁ
        pass

    # 8) recien_nacido(nombre): método de CLASE. Devolvé una instancia nivel 1.
    #    Pista: usá cls(nombre, 1).
    @classmethod
    def recien_nacido(cls, nombre):
        # TU CÓDIGO ACÁ
        pass


# 9) PokemonFuego: hereda de Pokemon. En __init__ llamá a super() y seteá
#    self.tipo = "Fuego". atacar() devuelve "<nombre> usa Lanzallamas!".
class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# 10) PokemonAgua: tipo "Agua". atacar() -> "<nombre> usa Pistola Agua!".
class PokemonAgua(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# 11) PokemonPlanta: tipo "Planta". atacar() -> "<nombre> usa Latigo Cepa!".
class PokemonPlanta(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# 12) PokemonElectrico: tipo "Electrico". atacar() -> "<nombre> usa Impactrueno!".
class PokemonElectrico(Pokemon):
    def __init__(self, nombre, nivel):
        # TU CÓDIGO ACÁ
        pass

    def atacar(self):
        # TU CÓDIGO ACÁ
        pass


# ----------------------------------------------------------------------
# Funciones que usan el polimorfismo y las ventajas de tipo.
# ----------------------------------------------------------------------

# Reglas de ventaja (qué tipo le gana a qué tipo):
#   Fuego -> Planta ; Agua -> Fuego ; Planta -> Agua ; Electrico -> Agua

# 13) tiene_ventaja(atacante, defensor): recibí dos objetos Pokemon y devolvé
#     True si el tipo del atacante tiene ventaja sobre el del defensor.
def tiene_ventaja(atacante, defensor):
    """Devolvé True si atacante tiene ventaja de tipo sobre defensor."""
    # TU CÓDIGO ACÁ
    pass


# 14) multiplicador(atacante, defensor): devolvé 2.0 si el atacante tiene ventaja,
#     0.5 si el defensor tiene ventaja sobre el atacante, 1.0 en otro caso.
def multiplicador(atacante, defensor):
    """Devolvé el multiplicador de daño según las ventajas de tipo."""
    # TU CÓDIGO ACÁ
    pass


# 15) describir_ataques(equipo): recibí una lista de Pokemon (de distintos tipos)
#     y devolvé una lista con el resultado de atacar() de cada uno (polimorfismo).
def describir_ataques(equipo):
    """Devolvé la lista de strings de atacar() de cada Pokémon."""
    # TU CÓDIGO ACÁ
    pass


# 16) crear_por_tipo(tipo, nombre, nivel): FÁBRICA. Devolvé una instancia de la
#     clase correcta según 'tipo' ("Fuego"->PokemonFuego, etc.).
#     Si el tipo no es válido, devolvé None.
def crear_por_tipo(tipo, nombre, nivel):
    """Devolvé la instancia de la subclase correcta según 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# 17) tipos_del_equipo(equipo): devolvé una lista con el .tipo de cada Pokémon.
def tipos_del_equipo(equipo):
    """Devolvé los tipos de cada Pokémon del equipo."""
    # TU CÓDIGO ACÁ
    pass


# 18) equipo_balanceado(equipo): devolvé True si TODOS los Pokémon son de
#     tipos distintos (no hay tipos repetidos).
def equipo_balanceado(equipo):
    """Devolvé True si no hay tipos repetidos en el equipo."""
    # TU CÓDIGO ACÁ
    pass


# 19) batalla_simple(a, b, dano): 'a' ataca a 'b' con 'dano', multiplicado por la
#     ventaja de tipo. Aplicá ese daño a 'b'. Devolvé el daño final (int) aplicado.
def batalla_simple(a, b, dano):
    """Aplicá daño con ventaja de tipo a 'b' y devolvé el daño final (int)."""
    # TU CÓDIGO ACÁ
    pass


# 20) cantidad_por_tipo(equipo, tipo): devolvé cuántos Pokémon del equipo son
#     del 'tipo' dado.
def cantidad_por_tipo(equipo, tipo):
    """Devolvé cuántos Pokémon del equipo son del tipo dado."""
    # TU CÓDIGO ACÁ
    pass
