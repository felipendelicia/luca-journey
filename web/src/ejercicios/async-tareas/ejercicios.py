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


# Total de tareas
# `buckets` es una lista de listas (las tareas de cada worker). Devolvé el total de tareas.
# Ejemplo:  total_tareas([["a"], ["b", "c"]])  →  3
def total_tareas(buckets):
    """Devolvé la suma de tareas de todos los workers."""
    # TU CÓDIGO ACÁ


# Cargas
# Devolvé una lista con la cantidad de tareas de cada worker.
# Ejemplo:  cargas([["a"], ["b", "c"]])  →  [1, 2]
def cargas(buckets):
    """Devolvé la cantidad de tareas por worker."""
    # TU CÓDIGO ACÁ


# El más cargado
# Devolvé el ÍNDICE del worker con más tareas (el primero si hay empate).
def mas_cargado(buckets):
    """Devolvé el índice del worker con más tareas."""
    # TU CÓDIGO ACÁ


# El menos cargado
# Devolvé el ÍNDICE del worker con menos tareas (el primero si hay empate).
def menos_cargado(buckets):
    """Devolvé el índice del worker con menos tareas."""
    # TU CÓDIGO ACÁ


# Promedio de carga
# Devolvé el promedio de tareas por worker.
# Ejemplo:  promedio_carga([["a"], ["b", "c"]])  →  1.5
def promedio_carga(buckets):
    """Devolvé el promedio de tareas por worker."""
    # TU CÓDIGO ACÁ


# Diferencia de carga
# Devolvé la diferencia entre el worker más cargado y el menos cargado.
# Ejemplo:  diferencia_carga([["a"], ["b", "c", "d"]])  →  2
def diferencia_carga(buckets):
    """Devolvé max(cargas) - min(cargas)."""
    # TU CÓDIGO ACÁ


# Repartir round-robin
# Repartí `tareas` entre `n` workers dando una a cada uno por turno. Devolvé la lista de listas.
# Ejemplo:  repartir_round_robin(["a", "b", "c"], 2)  →  [["a", "c"], ["b"]]
def repartir_round_robin(tareas, n):
    """Repartí las tareas entre n workers por turno."""
    # TU CÓDIGO ACÁ


# Agregar al menos cargado
# Agregá `tarea` al worker con menos tareas y devolvé los buckets.
def agregar_a_menos_cargado(buckets, tarea):
    """Agregá la tarea al worker más libre."""
    # TU CÓDIGO ACÁ


# Todas las tareas
# Devolvé una sola lista con todas las tareas de todos los workers, en orden.
# Ejemplo:  todas_las_tareas([["a"], ["b", "c"]])  →  ["a", "b", "c"]
def todas_las_tareas(buckets):
    """Devolvé todas las tareas en una sola lista."""
    # TU CÓDIGO ACÁ


# ¿Quién la tiene?
# Devolvé el ÍNDICE del worker que tiene `tarea`, o -1 si ninguno.
def quien_tiene(buckets, tarea):
    """Devolvé el índice del worker que tiene la tarea, o -1."""
    # TU CÓDIGO ACÁ


# Tareas de un worker
# Devolvé la lista de tareas del worker `i`.
def tareas_de(buckets, i):
    """Devolvé las tareas del worker i."""
    # TU CÓDIGO ACÁ


# Cantidad de workers
# Devolvé cuántos workers hay.
def cantidad_workers(buckets):
    """Devolvé la cantidad de workers."""
    # TU CÓDIGO ACÁ


# ¿Hay alguno vacío?
# Devolvé True si algún worker no tiene tareas.
def hay_vacio(buckets):
    """Devolvé True si algún worker está vacío."""
    # TU CÓDIGO ACÁ


# Mover una tarea
# Sacá la PRIMERA tarea del worker `origen` y agregala al final del worker `destino`. Devolvé
# los buckets. Si el origen está vacío, no hagas nada.
def mover_una(buckets, origen, destino):
    """Mové una tarea de origen a destino."""
    # TU CÓDIGO ACÁ


# ¿Están equilibrados?
# Devolvé True si la diferencia de carga entre el más y el menos cargado es 1 o menos.
def estan_equilibrados(buckets):
    """Devolvé True si la diferencia de carga es <= 1."""
    # TU CÓDIGO ACÁ


# El worker más grande
# Devolvé la LISTA de tareas del worker con más tareas.
def worker_mas_grande(buckets):
    """Devolvé las tareas del worker más cargado."""
    # TU CÓDIGO ACÁ
