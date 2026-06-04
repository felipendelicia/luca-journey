"""
✏️ Ejercicios — Consumir una API

Cuando tu programa le pide datos a una API (ej: la PokéAPI), recibe JSON.
Acá practicás PROCESAR esas respuestas (extraer, filtrar, manejar errores).
Te pasamos la respuesta ya como texto JSON.
"""
import json


# 1) La respuesta es {"name": "pikachu", "tipos": ["electrico"]}. Devolvé la lista de tipos.
def extraer_tipos(texto):
    """Devolvé la lista que está en la clave 'tipos'."""
    # TU CÓDIGO ACÁ
    pass


# 2) Devolvé una tupla (nombre, nivel) a partir de {"nombre": .., "nivel": ..}.
def nombre_y_nivel(texto):
    """Devolvé (nombre, nivel)."""
    # TU CÓDIGO ACÁ
    pass


# 3) La respuesta es una LISTA de Pokémon (cada uno con 'nombre' y 'tipo').
#    Devolvé los NOMBRES de los que sean del tipo pedido.
def filtrar_por_tipo(texto, tipo):
    """Devolvé una lista con los nombres de los Pokémon de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# 4) Si el status es 200, devolvé los datos (json.loads(texto)). Si no, devolvé None.
def manejar_respuesta(status, texto):
    """Manejá el caso de error: solo parseás si status == 200."""
    # TU CÓDIGO ACÁ
    pass


# 5) La respuesta es {"results": [...]}. Devolvé cuántos resultados hay.
def contar_resultados(texto):
    """Devolvé la cantidad de elementos en la lista 'results'."""
    # TU CÓDIGO ACÁ
    pass


# 6) La respuesta es {"results": [{"name": ..}, ...]}. Devolvé el name del primero.
def primer_resultado(texto):
    """Devolvé el 'name' del primer elemento de 'results'."""
    # TU CÓDIGO ACÁ
    pass
