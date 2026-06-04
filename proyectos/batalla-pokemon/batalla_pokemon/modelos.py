"""
batalla_pokemon.modelos — Las clases Movimiento y Pokemon.
"""


class Movimiento:
    """Un ataque con tipo, poder y PP (cantidad de usos)."""

    def __init__(self, nombre, tipo, poder, pp, efecto=None, prob_efecto=0.0):
        self.nombre = nombre
        self.tipo = tipo
        self.poder = poder
        self.pp = pp
        self.pp_max = pp
        # efecto: None, "paralizar", "dormir", "envenenar"
        self.efecto = efecto
        # probabilidad (0 a 1) de que el efecto se aplique al golpear.
        self.prob_efecto = prob_efecto

    def usable(self):
        """¿Le quedan PP?"""
        return self.pp > 0

    def usar(self):
        """Gasta 1 PP (sin bajar de 0)."""
        if self.pp > 0:
            self.pp -= 1

    def __repr__(self):
        return f"Movimiento({self.nombre!r}, {self.tipo!r}, poder={self.poder}, pp={self.pp})"


class Pokemon:
    """Un Pokémon de batalla: HP, tipo, movimientos y estado alterado."""

    def __init__(self, nombre, tipo, hp, movimientos):
        self.nombre = nombre
        self.tipo = tipo
        self.hp = hp
        self.hp_max = hp
        self.movimientos = list(movimientos)
        # Estado alterado: None, "paralizado", "dormido", "envenenado".
        self.estado = None
        # Cuántos turnos le quedan de sueño.
        self.turnos_dormido = 0

    def esta_debilitado(self):
        return self.hp <= 0

    def recibir_dano(self, cantidad):
        """Resta daño sin bajar de 0."""
        self.hp -= cantidad
        if self.hp < 0:
            self.hp = 0

    def curar(self, cantidad):
        """Suma HP sin pasar el máximo."""
        self.hp += cantidad
        if self.hp > self.hp_max:
            self.hp = self.hp_max

    def movimientos_usables(self):
        """Lista de movimientos con PP disponibles."""
        return [m for m in self.movimientos if m.usable()]

    def porcentaje_hp(self):
        return int((self.hp / self.hp_max) * 100) if self.hp_max else 0

    def __repr__(self):
        return f"Pokemon({self.nombre!r}, {self.tipo!r}, hp={self.hp}/{self.hp_max})"
