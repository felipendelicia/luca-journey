"""✏️ Ejercicios — Consumir una API

Cuando tu programa le pide datos a una API (ej: la PokéAPI), recibe JSON. Acá practicás
PROCESAR esas respuestas (extraer, filtrar, manejar errores). Te pasamos la respuesta
ya como texto JSON. ✅ Corregir al terminar.
"""
import json


# Extraer los tipos
# La respuesta es {"name": "pikachu", "tipos": ["electrico"]}. Devolvé la lista de 'tipos'.
# Ejemplo:  extraer_tipos('{"name": "vulpix", "tipos": ["fuego"]}')  →  ["fuego"]
def extraer_tipos(texto):
    """Devolvé la lista de la clave 'tipos'."""
    # TU CÓDIGO ACÁ
    pass


# Nombre y nivel (tupla)
# A partir de {"nombre": .., "nivel": ..}, devolvé la tupla (nombre, nivel).
# Ejemplo:  nombre_y_nivel('{"nombre": "Pikachu", "nivel": 25}')  →  ("Pikachu", 25)
def nombre_y_nivel(texto):
    """Devolvé (nombre, nivel)."""
    # TU CÓDIGO ACÁ
    pass


# Filtrar por tipo
# La respuesta es una LISTA de Pokémon (cada uno con 'nombre' y 'tipo'). Devolvé los
# NOMBRES de los que sean del 'tipo' pedido.
# Ejemplo:  filtrar_por_tipo('[{"nombre":"Vulpix","tipo":"Fuego"}]', "Fuego")  →  ["Vulpix"]
def filtrar_por_tipo(texto, tipo):
    """Devolvé los nombres de los Pokémon de ese 'tipo'."""
    # TU CÓDIGO ACÁ
    pass


# Manejar la respuesta
# Si el status es 200, devolvé los datos (json.loads(texto)). Si no, devolvé None.
# Ejemplo:  manejar_respuesta(200, '{"ok": 1}')  →  {"ok": 1}   ·   manejar_respuesta(404, "...")  →  None
def manejar_respuesta(status, texto):
    """Parseá solo si status == 200; si no, devolvé None."""
    # TU CÓDIGO ACÁ
    pass


# Contar resultados
# La respuesta es {"results": [...]}. Devolvé cuántos resultados hay.
# Ejemplo:  contar_resultados('{"results": [1, 2, 3]}')  →  3
def contar_resultados(texto):
    """Devolvé la cantidad de elementos en 'results'."""
    # TU CÓDIGO ACÁ
    pass


# El primer resultado
# La respuesta es {"results": [{"name": ..}, ...]}. Devolvé el 'name' del primero.
# Ejemplo:  primer_resultado('{"results": [{"name": "pikachu"}]}')  →  "pikachu"
def primer_resultado(texto):
    """Devolvé el 'name' del primer elemento de 'results'."""
    # TU CÓDIGO ACÁ
    pass
