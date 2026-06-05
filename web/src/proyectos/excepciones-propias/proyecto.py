# Líder Korrina — Errores a medida (solución de referencia).

class ErrorPokemon(Exception):
    pass

def verificar_vivo(hp):
    if hp <= 0:
        raise ErrorPokemon("El Pokémon se debilitó")
    return hp

class ErrorNivel(Exception):
    pass

def subir_nivel(nivel, cantidad):
    if cantidad < 0:
        raise ErrorNivel("La cantidad debe ser positiva")
    if nivel + cantidad > 100:
        raise ErrorNivel("No se puede superar el nivel 100")
    return nivel + cantidad

def intentar_subir(nivel, cantidad):
    try:
        return subir_nivel(nivel, cantidad)
    except ErrorNivel:
        return nivel

def combate_seguro(hp, nivel_actual, xp_ganada):
    try:
        verificar_vivo(hp)
    except ErrorPokemon:
        return {"resultado": "derrota", "nivel": nivel_actual}
    nuevo_nivel = intentar_subir(nivel_actual, xp_ganada)
    return {"resultado": "victoria", "nivel": nuevo_nivel}
