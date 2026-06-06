"""🧵 Ejercicios — Repartir tareas

Concurrencia = repartir trabajo entre varios "workers" para avanzar en paralelo. Acá
distribuís tareas y mirás que queden equilibradas. ✅ Corregí cuando termines.
"""


# Repartir en round-robin
# Repartí las `tareas` entre `n` workers dando una a cada uno por turno (round-robin).
# Devolvé una lista de n listas.
# Ejemplo:  repartir([1, 2, 3, 4, 5], 2)  →  [[1, 3, 5], [2, 4]]
def repartir(tareas, n):
    """Devolvé n listas con las tareas repartidas por turno."""


# Carga de cada worker
# Devolvé una lista con cuántas tareas tiene cada bucket.
# Ejemplo:  carga_de([[1, 3, 5], [2, 4]])  →  [3, 2]
def carga_de(buckets):
    """Devolvé la cantidad de tareas de cada bucket."""


# Worker más libre
# `cargas` es una lista de números (tareas por worker). Devolvé el ÍNDICE del worker
# con menos carga (el primero si hay empate).
# Ejemplo:  worker_libre([3, 1, 2])  →  1
def worker_libre(cargas):
    """Devolvé el índice de la menor carga."""


# ¿Está equilibrado?
# Devolvé True si entre el bucket más lleno y el más vacío hay como mucho 1 de diferencia.
# Ejemplo:  equilibrado([[1, 3], [2, 4]])  →  True   ·   equilibrado([[1, 2, 3], [4]])  →  False
def equilibrado(buckets):
    """Devolvé True si la diferencia de tamaños es <= 1."""
