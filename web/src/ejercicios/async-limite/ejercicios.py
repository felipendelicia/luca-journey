"""🚦 Ejercicios — Límite de concurrencia

Lanzar 10.000 descargas a la vez tira todo abajo. Por eso se LIMITA cuántas corren
juntas (un "semáforo"): se procesan de a lotes. Acá manejás ese límite.
✅ Corregí cuando termines.
"""
import math


# Partir en lotes
# Partí `items` en lotes de hasta `tam` elementos cada uno (en orden).
# Ejemplo:  por_lotes([1, 2, 3, 4, 5], 2)  →  [[1, 2], [3, 4], [5]]
def por_lotes(items, tam):
    """Devolvé lotes de hasta tam elementos."""


# ¿Cuántos lotes?
# Devolvé cuántos lotes de tamaño `tam` hacen falta para `total` items (techo).
# Ejemplo:  cantidad_lotes(5, 2)  →  3
def cantidad_lotes(total, tam):
    """Devolvé el techo de total / tam."""


# ¿Cabe uno más?
# Devolvé True si todavía se puede lanzar otra tarea sin pasar el `maximo` de concurrentes.
# Ejemplo:  cabe(2, 3)  →  True   ·   cabe(3, 3)  →  False
def cabe(activos, maximo):
    """Devolvé True si activos es menor que maximo."""


# Limitar la tanda
# Devolvé como mucho los primeros `maximo` pedidos de la lista.
# Ejemplo:  limitar([1, 2, 3, 4], 2)  →  [1, 2]
def limitar(pedidos, maximo):
    """Devolvé los primeros maximo pedidos."""
