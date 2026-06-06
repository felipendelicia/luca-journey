"""🔶 Ejercicios — Algoritmos sobre la Pokédex

Juntás búsqueda, orden y conteo sobre una lista de Pokémon (cada uno un dict con
"nombre", "tipo" y "nivel"). ✅ Corregí cuando termines.
"""


# Contar por tipo
# Devolvé un dict tipo → cantidad de Pokémon de ese tipo.
# Ejemplo:  contar_tipos([{"nombre": "a", "tipo": "agua"}, {"nombre": "b", "tipo": "agua"}])
#               →  {"agua": 2}
def contar_tipos(pokes):
    """Devolvé un dict tipo → cantidad."""


# Ordenar por nivel
# Devolvé la lista de Pokémon ordenada por nivel de MAYOR a menor.
# Ejemplo:  ordenar_por_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}])
#               →  [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]
def ordenar_por_nivel(pokes):
    """Devolvé los pokes ordenados por nivel descendente."""


# Buscar por nombre
# Devolvé el primer Pokémon cuyo "nombre" coincida, o None si no está.
# Ejemplo:  buscar([{"nombre": "Pikachu"}], "Pikachu")  →  {"nombre": "Pikachu"}
def buscar(pokes, nombre):
    """Devolvé el primer poke con ese nombre, o None."""


# Top N
# Devolvé los NOMBRES de los `n` Pokémon de mayor nivel, de mayor a menor.
# Ejemplo:  top_n([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}, {"nombre": "c", "nivel": 12}], 2)
#               →  ["b", "c"]
def top_n(pokes, n):
    """Devolvé los nombres de los n de mayor nivel."""
