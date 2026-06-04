"""
✅ Semana 09 — Soluciones: POO Avanzado

Jerarquía de clases con herencia, polimorfismo, property, staticmethod,
classmethod y clase abstracta. Comentadas línea por línea.
"""

from abc import ABC, abstractmethod


class Pokemon(ABC):
    """Clase abstracta base."""

    # 1)
    def __init__(self, nombre, nivel):
        self.nombre = nombre
        self.nivel = nivel
        # _hp es "interno": se accede a través de la propiedad hp.
        self.hp_max = 100
        self._hp = 100

    # 2)
    @property
    def hp(self):
        # El getter simplemente devuelve el valor interno.
        return self._hp

    # 3)
    @hp.setter
    def hp(self, valor):
        # Validamos: el HP queda entre 0 y hp_max.
        if valor < 0:
            valor = 0
        if valor > self.hp_max:
            valor = self.hp_max
        self._hp = valor

    # 4)
    @abstractmethod
    def atacar(self):
        # Sin cuerpo: cada subclase está obligada a implementarlo.
        ...

    # 5)
    def recibir_dano(self, cantidad):
        # Usamos la propiedad: al asignar, el setter valida que no baje de 0.
        self.hp = self.hp - cantidad

    # 6)
    def esta_debilitado(self):
        return self.hp <= 0

    # 7)
    @staticmethod
    def es_tipo_valido(tipo):
        # No usa self: es una utilidad de la clase.
        return tipo in ["Fuego", "Agua", "Planta", "Electrico"]

    # 8)
    @classmethod
    def recien_nacido(cls, nombre):
        # cls es la clase concreta (PokemonFuego, etc.). Creamos nivel 1.
        return cls(nombre, 1)


# 9)
class PokemonFuego(Pokemon):
    def __init__(self, nombre, nivel):
        # super() ejecuta el __init__ del padre (setea nombre, nivel, hp).
        super().__init__(nombre, nivel)
        self.tipo = "Fuego"

    def atacar(self):
        # Sobrescribimos atacar con el ataque propio del tipo.
        return f"{self.nombre} usa Lanzallamas!"


# 10)
class PokemonAgua(Pokemon):
    def __init__(self, nombre, nivel):
        super().__init__(nombre, nivel)
        self.tipo = "Agua"

    def atacar(self):
        return f"{self.nombre} usa Pistola Agua!"


# 11)
class PokemonPlanta(Pokemon):
    def __init__(self, nombre, nivel):
        super().__init__(nombre, nivel)
        self.tipo = "Planta"

    def atacar(self):
        return f"{self.nombre} usa Latigo Cepa!"


# 12)
class PokemonElectrico(Pokemon):
    def __init__(self, nombre, nivel):
        super().__init__(nombre, nivel)
        self.tipo = "Electrico"

    def atacar(self):
        return f"{self.nombre} usa Impactrueno!"


# Tabla de ventajas: cada tipo le gana al tipo de la derecha.
_VENTAJAS = {
    "Fuego": "Planta",
    "Agua": "Fuego",
    "Planta": "Agua",
    "Electrico": "Agua",
}


# 13)
def tiene_ventaja(atacante, defensor):
    """¿El atacante tiene ventaja sobre el defensor?"""
    # Buscamos a qué tipo le gana el atacante y comparamos con el defensor.
    return _VENTAJAS.get(atacante.tipo) == defensor.tipo


# 14)
def multiplicador(atacante, defensor):
    """Multiplicador de daño según ventajas."""
    if tiene_ventaja(atacante, defensor):
        return 2.0
    # Si el defensor tiene ventaja sobre el atacante, el atacante pega flojo.
    if tiene_ventaja(defensor, atacante):
        return 0.5
    return 1.0


# 15)
def describir_ataques(equipo):
    """Polimorfismo: cada Pokémon ataca a su manera."""
    # El mismo atacar() da resultados distintos según la clase de cada uno.
    return [pokemon.atacar() for pokemon in equipo]


# 16)
def crear_por_tipo(tipo, nombre, nivel):
    """Fábrica: devuelve la subclase correcta según el tipo."""
    if tipo == "Fuego":
        return PokemonFuego(nombre, nivel)
    elif tipo == "Agua":
        return PokemonAgua(nombre, nivel)
    elif tipo == "Planta":
        return PokemonPlanta(nombre, nivel)
    elif tipo == "Electrico":
        return PokemonElectrico(nombre, nivel)
    else:
        return None


# 17)
def tipos_del_equipo(equipo):
    """Lista de tipos."""
    return [pokemon.tipo for pokemon in equipo]


# 18)
def equipo_balanceado(equipo):
    """True si no hay tipos repetidos."""
    tipos = tipos_del_equipo(equipo)
    # Un set elimina duplicados. Si tiene el mismo largo que la lista, no había repetidos.
    return len(set(tipos)) == len(tipos)


# 19)
def batalla_simple(a, b, dano):
    """'a' ataca a 'b' con ventaja de tipo aplicada."""
    # Calculamos el daño final con el multiplicador de tipo.
    dano_final = int(dano * multiplicador(a, b))
    # Se lo aplicamos al defensor.
    b.recibir_dano(dano_final)
    return dano_final


# 20)
def cantidad_por_tipo(equipo, tipo):
    """Cuántos Pokémon son del tipo dado."""
    cantidad = 0
    for pokemon in equipo:
        if pokemon.tipo == tipo:
            cantidad = cantidad + 1
    return cantidad
