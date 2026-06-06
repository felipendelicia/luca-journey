"""🕸️ Ejercicios — Dividir trabajo (hilos)

Otra forma de paralelizar: partir el trabajo en bloques CONTIGUOS y darle uno a cada
hilo. Acá calculás esos bloques. ✅ Corregí cuando termines.
"""
import math


# Dividir en n bloques contiguos
# Partí `items` en `n` bloques lo más parejos posible, manteniendo el orden. Si no divide
# justo, los primeros bloques se quedan con uno de más.
# Ejemplo:  dividir([1, 2, 3, 4, 5, 6], 3)  →  [[1, 2], [3, 4], [5, 6]]
#           dividir([1, 2, 3, 4, 5], 2)     →  [[1, 2, 3], [4, 5]]
def dividir(items, n):
    """Devolvé n bloques contiguos lo más parejos posible."""


# Tamaño de cada bloque
# Si repartís `total` items en `n` hilos, ¿cuántos entran como MÁXIMO por hilo?
# (redondeá hacia arriba). Ejemplo:  tamano_chunk(10, 3)  →  4
def tamano_chunk(total, n):
    """Devolvé el techo de total / n."""


# ¿Cuántos hilos necesito?
# Si cada hilo procesa `por_hilo` items, ¿cuántos hilos hacen falta para `total`?
# (redondeá hacia arriba). Ejemplo:  cuantos_hilos(10, 4)  →  3
def cuantos_hilos(total, por_hilo):
    """Devolvé el techo de total / por_hilo."""


# Volver a juntar
# Recibís una lista de bloques y devolvés todos los items en una sola lista (en orden).
# Ejemplo:  aplanar([[1, 2], [3, 4], [5]])  →  [1, 2, 3, 4, 5]
def aplanar(chunks):
    """Devolvé todos los items de los bloques en una lista."""
