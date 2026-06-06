"""🔢 Ejercicios — Ordenar listas

Ordenar es un clásico. Python tiene sorted(), pero entender CÓMO se ordena te enseña a
pensar algoritmos. Acá implementás el orden a mano. ✅ Corregí cuando termines.
"""


# Índice del mínimo
# Devolvé el índice del elemento más chico de la lista (el primero si hay empate).
# (Sin usar min().) Ejemplo:  indice_minimo([30, 10, 20])  →  1
def indice_minimo(lista):
    """Devolvé el índice del valor mínimo."""


# ¿Está ordenada?
# Devolvé True si la lista está de menor a mayor (cada elemento <= el siguiente).
# Ejemplo:  esta_ordenada([1, 2, 2, 3])  →  True   ·   esta_ordenada([3, 1])  →  False
def esta_ordenada(lista):
    """Devolvé True si la lista está ordenada ascendente."""


# Ordenamiento burbuja
# Ordená la lista de menor a mayor con el método BURBUJA (comparar pares vecinos e
# intercambiarlos). Devolvé una lista NUEVA ordenada (no uses sorted()).
# Ejemplo:  ordenar_burbuja([3, 1, 2])  →  [1, 2, 3]
def ordenar_burbuja(lista):
    """Devolvé una lista nueva ordenada con burbuja."""


# Ordenamiento por selección
# Ordená buscando el mínimo y poniéndolo adelante, repetidamente. Devolvé una lista NUEVA.
# (Podés apoyarte en indice_minimo.) Ejemplo:  ordenar_seleccion([3, 1, 2])  →  [1, 2, 3]
def ordenar_seleccion(lista):
    """Devolvé una lista nueva ordenada por selección."""
