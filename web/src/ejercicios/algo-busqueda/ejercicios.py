"""🔎 Ejercicios — Búsqueda lineal y binaria

Buscar es lo más común en programación. La búsqueda LINEAL mira uno por uno; la BINARIA
(sobre una lista ordenada) parte el problema al medio cada vez: mucho más rápida.
✅ Corregí cuando termines.
"""


# Búsqueda lineal
# Recorré la lista y devolvé el ÍNDICE donde está `x`. Si no está, devolvé -1.
# (Hacelo a mano con un bucle, sin usar .index().)
# Ejemplo:  busqueda_lineal([10, 20, 30], 20)  →  1   ·   busqueda_lineal([10], 99)  →  -1
def busqueda_lineal(lista, x):
    """Devolvé el índice de x, o -1."""


# ¿Está?
# Devolvé True si `x` aparece en la lista, False si no.
# Ejemplo:  contiene([1, 2, 3], 2)  →  True
def contiene(lista, x):
    """Devolvé True si x está en la lista."""


# Búsqueda binaria
# `ordenada` viene de menor a mayor. Buscá `x` partiendo el rango al medio cada vez y
# devolvé su ÍNDICE, o -1 si no está. (Implementala vos, sin .index().)
# Ejemplo:  busqueda_binaria([1, 3, 5, 7, 9], 7)  →  3   ·   busqueda_binaria([1, 3, 5], 4)  →  -1
def busqueda_binaria(ordenada, x):
    """Devolvé el índice de x por búsqueda binaria, o -1."""


# Primero mayor
# En una lista ordenada, devolvé el primer elemento ESTRICTAMENTE mayor que `x`. Si no
# hay ninguno, devolvé None.
# Ejemplo:  primero_mayor([1, 3, 5, 7], 4)  →  5   ·   primero_mayor([1, 2], 9)  →  None
def primero_mayor(ordenada, x):
    """Devolvé el primer elemento mayor que x, o None."""
