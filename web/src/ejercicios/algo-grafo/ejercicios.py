"""🕸️ Ejercicios — Grafos

Un grafo son nodos conectados por aristas (mapas, redes sociales, rutas). Lo guardamos
como un diccionario: cada nodo → lista de sus vecinos. ✅ Corregí cuando termines.
"""


# Vecinos de un nodo
# Devolvé la lista de vecinos de `nodo`. Si el nodo no está en el grafo, devolvé [].
# Ejemplo:  vecinos({"a": ["b", "c"]}, "a")  →  ["b", "c"]
#           vecinos({"a": ["b"]}, "z")       →  []
def vecinos(grafo, nodo):
    """Devolvé la lista de vecinos de nodo (o [] si no está)."""


# Grado de un nodo
# El grado es cuántos vecinos tiene. Devolvelo.
# Ejemplo:  grado({"a": ["b", "c"]}, "a")  →  2
def grado(grafo, nodo):
    """Devolvé la cantidad de vecinos de nodo."""


# ¿Hay arista?
# Devolvé True si existe una conexión de `a` hacia `b` (b está entre los vecinos de a).
# Ejemplo:  hay_arista({"a": ["b"]}, "a", "b")  →  True
def hay_arista(grafo, a, b):
    """Devolvé True si b es vecino de a."""


# Todos los nodos
# Devolvé la lista de nodos del grafo, ORDENADA alfabéticamente.
# Ejemplo:  nodos({"c": [], "a": [], "b": []})  →  ["a", "b", "c"]
def nodos(grafo):
    """Devolvé los nodos del grafo, ordenados."""
