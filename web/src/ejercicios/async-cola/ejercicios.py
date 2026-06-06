"""🎟️ Ejercicios — Cola productor/consumidor

Un patrón clásico de concurrencia: unos PRODUCEN tareas y las ponen en una cola; otros
las CONSUMEN. La cola es FIFO (first in, first out): el primero que entra, sale primero.
✅ Corregí cuando termines.
"""


# Encolar
# Agregá `item` al final de la cola (una lista) y devolvé la cola.
# Ejemplo:  encolar([1, 2], 3)  →  [1, 2, 3]
def encolar(cola, item):
    """Agregá item al final y devolvé la cola."""


# Desencolar (FIFO)
# Sacá y devolvé el PRIMER elemento de la cola (el más viejo). Si está vacía, devolvé None.
# Ejemplo:  desencolar([1, 2, 3])  →  1  (y la cola queda [2, 3])
def desencolar(cola):
    """Sacá y devolvé el primer elemento, o None si está vacía."""


# Espiar el siguiente
# Devolvé el primer elemento SIN sacarlo. Si la cola está vacía, devolvé None.
# Ejemplo:  siguiente([1, 2, 3])  →  1   ·   siguiente([])  →  None
def siguiente(cola):
    """Devolvé el primer elemento sin sacarlo."""


# Vaciar procesando
# Consumí toda la cola en orden FIFO y devolvé la lista de items en el orden en que se
# procesaron. La cola debe quedar vacía.
# Ejemplo:  vaciar([1, 2, 3])  →  [1, 2, 3]
def vaciar(cola):
    """Sacá todo en orden FIFO y devolvé la lista procesada."""
