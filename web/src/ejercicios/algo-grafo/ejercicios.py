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


# Cantidad de nodos
# Devolvé cuántos nodos tiene el grafo.
# Ejemplo:  cantidad_nodos({"a": ["b"], "b": ["a"]})  →  2
def cantidad_nodos(grafo):
    """Devolvé cuántos nodos hay."""
    # TU CÓDIGO ACÁ


# Nodos aislados
# Devolvé una lista con los nodos que no tienen ningún vecino.
# Ejemplo:  nodos_aislados({"a": [], "b": ["c"], "c": ["b"]})  →  ["a"]
def nodos_aislados(grafo):
    """Devolvé los nodos sin vecinos."""
    # TU CÓDIGO ACÁ


# Grado máximo
# Devolvé la mayor cantidad de vecinos que tiene algún nodo.
# Ejemplo:  grado_maximo({"a": ["b", "c"], "b": ["a"], "c": ["a"]})  →  2
def grado_maximo(grafo):
    """Devolvé el grado más alto."""
    # TU CÓDIGO ACÁ


# El más conectado
# Devolvé el nodo con más vecinos.
# Ejemplo:  nodo_mas_conectado({"a": ["b", "c"], "b": ["a"], "c": ["a"]})  →  "a"
def nodo_mas_conectado(grafo):
    """Devolvé el nodo de mayor grado."""
    # TU CÓDIGO ACÁ


# Grados de todos
# Devolvé un dict nodo → cantidad de vecinos.
# Ejemplo:  grados({"a": ["b"], "b": ["a", "c"], "c": ["b"]})  →  {"a": 1, "b": 2, "c": 1}
def grados(grafo):
    """Devolvé un dict nodo → grado."""
    # TU CÓDIGO ACÁ


# Vecinos en común
# Devolvé los vecinos que `a` y `b` comparten, en el orden de los vecinos de `a`.
# Ejemplo:  vecinos_comunes({"a": ["x", "y"], "b": ["y", "z"]}, "a", "b")  →  ["y"]
def vecinos_comunes(grafo, a, b):
    """Devolvé los vecinos comunes de a y b."""
    # TU CÓDIGO ACÁ


# Agregar una arista
# Conectá `a` y `b` en ambos sentidos (grafo no dirigido), sin duplicar. Creá los nodos si no
# existen y devolvé el grafo.
# Ejemplo:  agregar_arista({"a": []}, "a", "b")  →  {"a": ["b"], "b": ["a"]}
def agregar_arista(grafo, a, b):
    """Conectá a y b en ambos sentidos y devolvé el grafo."""
    # TU CÓDIGO ACÁ


# Quitar un nodo
# Sacá el nodo `n` del grafo y también de las listas de vecinos de los demás. Devolvé el grafo.
# Ejemplo:  quitar_nodo({"a": ["b"], "b": ["a"]}, "a")  →  {"b": []}
def quitar_nodo(grafo, n):
    """Quitá el nodo n y sus referencias."""
    # TU CÓDIGO ACÁ


# Recorrido en anchura (BFS)
# Devolvé la lista de nodos en el orden en que los visita una búsqueda en ANCHURA desde
# `origen` (con una cola).
# Ejemplo:  recorrido_bfs({"a": ["b", "c"], "b": ["a", "d"], "c": ["a"], "d": ["b"]}, "a")
#               →  ["a", "b", "c", "d"]
def recorrido_bfs(grafo, origen):
    """Devolvé el recorrido BFS desde origen."""
    # TU CÓDIGO ACÁ


# Recorrido en profundidad (DFS)
# Devolvé la lista de nodos en el orden en que los visita una búsqueda en PROFUNDIDAD desde
# `origen` (con recursión).
# Ejemplo:  recorrido_dfs({"a": ["b", "c"], "b": ["a", "d"], "c": ["a"], "d": ["b"]}, "a")
#               →  ["a", "b", "d", "c"]
def recorrido_dfs(grafo, origen):
    """Devolvé el recorrido DFS desde origen."""
    # TU CÓDIGO ACÁ


# ¿Hay camino?
# Devolvé True si se puede llegar de `a` a `b` siguiendo aristas.
# Ejemplo:  hay_camino({"a": ["b"], "b": ["a", "c"], "c": ["b"]}, "a", "c")  →  True
def hay_camino(grafo, a, b):
    """Devolvé True si hay camino de a a b."""
    # TU CÓDIGO ACÁ


# Distancia más corta
# Devolvé la cantidad MÍNIMA de aristas para ir de `origen` a `destino` (con BFS). Si no se
# puede llegar, devolvé -1.  Ejemplo:  distancia(..., "a", "d")  →  2  ·  origen==destino  →  0
def distancia(grafo, origen, destino):
    """Devolvé la distancia mínima en aristas, o -1."""
    # TU CÓDIGO ACÁ


# Componente conexa
# Devolvé una lista ORDENADA con todos los nodos a los que se puede llegar desde `origen`
# (incluido él).  Ejemplo:  componente({"a": ["b"], "b": ["a"], "c": []}, "a")  →  ["a", "b"]
def componente(grafo, origen):
    """Devolvé los nodos alcanzables desde origen, ordenados."""
    # TU CÓDIGO ACÁ


# Alcanzables en N pasos
# Devolvé una lista ORDENADA con los nodos a los que se llega desde `origen` en `pasos`
# aristas o menos (incluido origen).
# Ejemplo:  alcanzables_en({"a": ["b"], "b": ["a", "c"], "c": ["b"]}, "a", 1)  →  ["a", "b"]
def alcanzables_en(grafo, origen, pasos):
    """Devolvé los nodos alcanzables en 'pasos' pasos o menos."""
    # TU CÓDIGO ACÁ


# ¿Es una hoja?
# Devolvé True si el nodo tiene exactamente un vecino.
# Ejemplo:  es_hoja({"a": ["b"], "b": ["a", "c"]}, "a")  →  True
def es_hoja(grafo, nodo):
    """Devolvé True si el nodo tiene un solo vecino."""
    # TU CÓDIGO ACÁ


# Cantidad de conexiones
# Devolvé la suma de los grados de todos los nodos (cuántas entradas de vecinos hay en total).
# Ejemplo:  cantidad_conexiones({"a": ["b"], "b": ["a"]})  →  2
def cantidad_conexiones(grafo):
    """Devolvé la suma de los grados."""
    # TU CÓDIGO ACÁ
