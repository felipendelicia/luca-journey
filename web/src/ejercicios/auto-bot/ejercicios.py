"""🤖 Ejercicios — Automatizador (bot)

Un bot encadena pasos: normaliza datos, los filtra y los agrupa. Acá practicás ese
"pipeline" sobre una lista de Pokémon (cada uno un dict). ✅ Corregí cuando termines.
"""


# Normalizar un nombre
# Devolvé el nombre sin espacios al borde y en minúsculas (para comparar sin líos).
# Ejemplo:  normalizar("  Pikachu ")  →  "pikachu"
def normalizar(nombre):
    """Devolvé el nombre limpio y en minúsculas."""


# Filtrar por nivel
# `pokes` es una lista de dicts con clave "nivel". Devolvé solo los que tengan
# nivel mayor o igual a `minimo`.
# Ejemplo:  filtrar_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}], 10)
#               →  [{"nombre": "b", "nivel": 20}]
def filtrar_nivel(pokes, minimo):
    """Devolvé los pokes con nivel >= minimo."""


# Agrupar por tipo
# Cada poke es un dict con "nombre" y "tipo". Devolvé un dict que para cada tipo liste
# los NOMBRES de los Pokémon de ese tipo (en el orden en que aparecen).
# Ejemplo:  agrupar_por_tipo([{"nombre": "Squirtle", "tipo": "agua"},
#                             {"nombre": "Charmander", "tipo": "fuego"},
#                             {"nombre": "Psyduck", "tipo": "agua"}])
#               →  {"agua": ["Squirtle", "Psyduck"], "fuego": ["Charmander"]}
def agrupar_por_tipo(pokes):
    """Devolvé un dict tipo → lista de nombres."""


# Contar
# Devolvé cuántos Pokémon hay en la lista.
# Ejemplo:  contar([{"nombre": "a"}, {"nombre": "b"}])  →  2
def contar(pokes):
    """Devolvé la cantidad de pokes."""
