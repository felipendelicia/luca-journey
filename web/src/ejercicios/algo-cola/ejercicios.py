"""🚶 Ejercicios — Cola (queue)

Una cola es FIFO: el primero que llega es el primero que se atiende (como la fila del
Centro Pokémon). Se usa para turnos y para recorrer "a lo ancho" (BFS).
✅ Corregí cuando termines.
"""


# Encolar
# Agregá `x` al FINAL de la fila (una lista) y devolvé la cola.
# Ejemplo:  encolar([1, 2], 3)  →  [1, 2, 3]
def encolar(cola, x):
    """Agregá x al final y devolvé la cola."""


# Atender (FIFO)
# Sacá y devolvé el PRIMERO de la fila (el que llegó antes). Si está vacía, devolvé None.
# Ejemplo:  atender([1, 2, 3])  →  1  (la cola queda [2, 3])
def atender(cola):
    """Sacá y devolvé el primero, o None si está vacía."""


# Cuántos esperan
# Devolvé cuántos hay en la fila.
# Ejemplo:  en_espera([1, 2, 3])  →  3
def en_espera(cola):
    """Devolvé la cantidad en la cola."""


# Orden de atención
# Devolvé una lista con los elementos en el orden en que se van a atender (sin modificar
# la cola). Ejemplo:  orden_de_atencion([1, 2, 3])  →  [1, 2, 3]
def orden_de_atencion(cola):
    """Devolvé los elementos en orden FIFO (lista nueva)."""
