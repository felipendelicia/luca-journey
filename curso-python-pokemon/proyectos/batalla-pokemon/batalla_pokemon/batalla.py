"""
batalla_pokemon.batalla — La lógica de la batalla por turnos.

La clase Batalla aplica movimientos, calcula daño con efectividad de tipo,
gasta PP y aplica estados. El azar entra por 'rng' (una función que devuelve un
float entre 0 y 1), que se puede reemplazar en los tests para hacerlo determinista.
"""

import random

from . import tipos, estados


class Batalla:
    def __init__(self, p1, p2, rng=None):
        self.p1 = p1
        self.p2 = p2
        # rng() devuelve un float en [0, 1). Por defecto, azar real.
        self.rng = rng if rng is not None else random.random

    def calcular_dano(self, movimiento, defensor):
        """Devuelve (dano, multiplicador) según el tipo del movimiento y el defensor."""
        mult = tipos.efectividad(movimiento.tipo, defensor.tipo)
        dano = int(movimiento.poder * mult)
        return dano, mult

    def ejecutar_movimiento(self, atacante, defensor, indice_movimiento):
        """
        Ejecuta el movimiento 'indice_movimiento' de 'atacante' contra 'defensor'.
        Devuelve una lista de mensajes describiendo lo que pasó.
        """
        mensajes = []

        # 1) ¿El estado lo deja atacar?
        puede, msg = estados.puede_atacar(atacante, self.rng())
        if msg:
            mensajes.append(msg)
        if not puede:
            return mensajes

        # 2) Validamos el movimiento y sus PP.
        if indice_movimiento < 0 or indice_movimiento >= len(atacante.movimientos):
            mensajes.append("Movimiento inválido.")
            return mensajes
        movimiento = atacante.movimientos[indice_movimiento]
        if not movimiento.usable():
            mensajes.append(f"¡{movimiento.nombre} no tiene PP!")
            return mensajes

        # 3) Gastamos PP y aplicamos el daño.
        movimiento.usar()
        dano, mult = self.calcular_dano(movimiento, defensor)
        defensor.recibir_dano(dano)
        mensajes.append(f"{atacante.nombre} usó {movimiento.nombre}! ({dano} de daño)")
        texto = tipos.texto_efectividad(mult)
        if texto:
            mensajes.append(texto)

        # 4) ¿El movimiento aplica un estado alterado?
        if (movimiento.efecto and not defensor.esta_debilitado()
                and defensor.estado is None):
            if self.rng() < movimiento.prob_efecto:
                estados.aplicar_estado(defensor, movimiento.efecto)
                mensajes.append(f"¡{defensor.nombre} quedó {movimiento.efecto}!")

        return mensajes

    def fin_de_turno(self, pokemon):
        """Aplica el daño de estado (veneno) al final del turno."""
        _, msg = estados.dano_por_estado(pokemon)
        return [msg] if msg else []

    def terminada(self):
        """¿Terminó la batalla (alguno debilitado)?"""
        return self.p1.esta_debilitado() or self.p2.esta_debilitado()

    def ganador(self):
        """Devuelve el Pokémon ganador, o None si sigue."""
        if self.p2.esta_debilitado() and not self.p1.esta_debilitado():
            return self.p1
        if self.p1.esta_debilitado() and not self.p2.esta_debilitado():
            return self.p2
        return None


def elegir_movimiento_cpu(pokemon, rng=None):
    """
    La CPU elige al azar un movimiento con PP disponible.
    Devuelve el índice del movimiento (en pokemon.movimientos), o None si no puede.
    """
    rng = rng if rng is not None else random.random
    indices_usables = [
        i for i, m in enumerate(pokemon.movimientos) if m.usable()
    ]
    if not indices_usables:
        return None
    # Elegimos uno usando la tirada (sin depender de random.choice directamente).
    posicion = int(rng() * len(indices_usables))
    if posicion >= len(indices_usables):
        posicion = len(indices_usables) - 1
    return indices_usables[posicion]
