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


# Tamaño
# Devolvé cuántos items hay en la cola.
def tamano(cola):
    """Devolvé la cantidad de items."""
    # TU CÓDIGO ACÁ


# ¿Vacía?
# Devolvé True si la cola no tiene items.
def esta_vacia(cola):
    """Devolvé True si la cola está vacía."""
    # TU CÓDIGO ACÁ


# Espacio libre
# Devolvé cuántos lugares quedan, dada una `capacidad`.
# Ejemplo:  espacio_libre(["a"], 3)  →  2
def espacio_libre(cola, capacidad):
    """Devolvé capacidad - cantidad de items."""
    # TU CÓDIGO ACÁ


# ¿Cabe uno más?
# Devolvé True si la cantidad de items es MENOR que la capacidad.
def cabe(cola, capacidad):
    """Devolvé True si todavía cabe un item."""
    # TU CÓDIGO ACÁ


# ¿Está llena?
# Devolvé True si la cantidad de items llegó (o superó) la capacidad.
def esta_llena(cola, capacidad):
    """Devolvé True si la cola está llena."""
    # TU CÓDIGO ACÁ


# Encolar varios
# Agregá todos los `items` al final de la cola, en orden, y devolvé la cola.
def encolar_varios(cola, items):
    """Encolá todos los items."""
    # TU CÓDIGO ACÁ


# Desencolar varios
# Sacá y devolvé los primeros `n` items (o menos si no alcanzan), en orden.
# Ejemplo:  desencolar_varios(["a", "b", "c"], 2)  →  ["a", "b"]
def desencolar_varios(cola, n):
    """Devolvé los primeros n items, sacándolos."""
    # TU CÓDIGO ACÁ


# Próximos
# Devolvé los primeros `n` items SIN sacarlos.
def proximos(cola, n):
    """Devolvé los primeros n items sin sacarlos."""
    # TU CÓDIGO ACÁ


# ¿Está en la cola?
# Devolvé True si `item` está en la cola.
def hay(cola, item):
    """Devolvé True si item está en la cola."""
    # TU CÓDIGO ACÁ


# Posición
# Devolvé el puesto de `item` (el primero es 1), o -1 si no está.
def posicion(cola, item):
    """Devolvé el puesto de item (desde 1), o -1."""
    # TU CÓDIGO ACÁ


# Contar
# Devolvé cuántas veces aparece `item` en la cola.
def contar(cola, item):
    """Devolvé cuántas veces está item."""
    # TU CÓDIGO ACÁ


# Rotar
# Mové los primeros `n` items al final, conservando el orden. Devolvé la cola.
def rotar(cola, n):
    """Mové los primeros n al final."""
    # TU CÓDIGO ACÁ


# Dividir en lotes
# Devolvé una lista de listas, partiendo `items` en bloques de tamaño `tam`.
# Ejemplo:  dividir_en_lotes([1, 2, 3, 4, 5], 2)  →  [[1, 2], [3, 4], [5]]
def dividir_en_lotes(items, tam):
    """Partí los items en lotes de tam."""
    # TU CÓDIGO ACÁ


# Procesar todos
# Aplicá `func` a cada item de la cola y devolvé la lista de resultados.
# Ejemplo:  procesar_todos([1, 2, 3], lambda x: x*2)  →  [2, 4, 6]
def procesar_todos(cola, func):
    """Devolvé func aplicada a cada item."""
    # TU CÓDIGO ACÁ


# Invertir
# Devolvé una cola NUEVA con el orden invertido.
def invertir_cola(cola):
    """Devolvé la cola invertida."""
    # TU CÓDIGO ACÁ


# Mover al final
# Mové la primera aparición de `item` al final de la cola y devolvela.
def mover_al_final(cola, item):
    """Mové item al final de la cola."""
    # TU CÓDIGO ACÁ
