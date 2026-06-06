"""🗂️ Ejercicios — Diccionarios y sets

Los diccionarios (hash maps) y los sets buscan en tiempo casi instantáneo. Son la
herramienta para contar, deduplicar y comparar colecciones. ✅ Corregí cuando termines.
"""


# Frecuencias
# Contá cuántas veces aparece cada elemento y devolvé un dict elemento → cantidad.
# Ejemplo:  frecuencias(["a", "b", "a", "c", "a"])  →  {"a": 3, "b": 1, "c": 1}
def frecuencias(items):
    """Devolvé un dict con la cantidad de cada elemento."""


# Sin duplicados
# Devolvé la lista sin repetidos, MANTENIENDO el orden de la primera aparición.
# Ejemplo:  sin_duplicados([3, 1, 3, 2, 1])  →  [3, 1, 2]
def sin_duplicados(items):
    """Devolvé los elementos únicos, en orden de aparición."""


# El más común
# Devolvé el elemento que más se repite. Si hay empate, devolvé el que aparece primero.
# Ejemplo:  mas_comun(["a", "b", "a", "c"])  →  "a"
def mas_comun(items):
    """Devolvé el elemento más frecuente."""


# Intersección
# Devolvé los elementos que están en AMBAS listas, sin repetidos y ORDENADOS.
# Ejemplo:  interseccion([1, 2, 3, 4], [2, 4, 6])  →  [2, 4]
def interseccion(a, b):
    """Devolvé los elementos comunes, únicos y ordenados."""
