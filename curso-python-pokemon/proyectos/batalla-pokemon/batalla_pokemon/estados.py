"""
batalla_pokemon.estados — Estados alterados (paralizado, dormido, envenenado).

Las funciones reciben la "tirada" de azar como parámetro para que se puedan
testear sin depender del random real.
"""

PARALIZADO = "paralizado"
DORMIDO = "dormido"
ENVENENADO = "envenenado"

# Probabilidad de que un Pokémon paralizado no pueda moverse.
PROB_PARALISIS = 0.25


def aplicar_estado(pokemon, estado, turnos_sueno=2):
    """
    Aplica un estado alterado si el Pokémon no tiene ya uno. Devuelve True si lo aplicó.
    """
    if pokemon.estado is not None:
        return False
    pokemon.estado = estado
    if estado == DORMIDO:
        pokemon.turnos_dormido = turnos_sueno
    return True


def puede_atacar(pokemon, tirada):
    """
    Decide si el Pokémon puede atacar este turno según su estado.
    'tirada' es un número entre 0 y 1.
    Devuelve (puede_bool, mensaje).
    """
    if pokemon.estado == DORMIDO:
        # Cada turno dormido descuenta uno; al llegar a 0, se despierta.
        pokemon.turnos_dormido -= 1
        if pokemon.turnos_dormido <= 0:
            pokemon.estado = None
            return True, f"¡{pokemon.nombre} se despertó!"
        return False, f"{pokemon.nombre} está dormido 💤"

    if pokemon.estado == PARALIZADO:
        if tirada < PROB_PARALISIS:
            return False, f"{pokemon.nombre} está paralizado y no puede moverse ⚡"
        return True, ""

    # Sin estado (o envenenado, que igual puede atacar).
    return True, ""


def dano_por_estado(pokemon):
    """
    Daño al final del turno por estado (solo el veneno hace daño).
    Devuelve (dano, mensaje).
    """
    if pokemon.estado == ENVENENADO and not pokemon.esta_debilitado():
        # El veneno saca 1/8 del HP máximo (mínimo 1).
        dano = max(1, pokemon.hp_max // 8)
        pokemon.recibir_dano(dano)
        return dano, f"{pokemon.nombre} sufre {dano} de daño por veneno 🤢"
    return 0, ""
