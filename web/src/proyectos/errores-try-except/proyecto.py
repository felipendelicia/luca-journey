# Líder Viola — Cazadora de errores (solución de referencia).
# El preamble (POKEDEX) está en meta.json y se antepone al corregir.

def dividir_seguro(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return None

def a_entero(texto):
    try:
        return int(texto)
    except ValueError:
        return 0

def buscar_pokemon(nombre):
    try:
        return POKEDEX[nombre]
    except KeyError:
        return None

def nivel_seguro(nombre, divisor):
    poke = buscar_pokemon(nombre)
    if poke is None:
        return -1
    resultado = dividir_seguro(poke["nivel"], divisor)
    if resultado is None:
        return -1
    return resultado
