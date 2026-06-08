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


# Cuántos chunks
# Devolvé en cuántos bloques de tamaño `tam` se parte `items` (el último puede ser más chico).
# Ejemplo:  cuantos_chunks([1, 2, 3, 4, 5], 2)  →  3
def cuantos_chunks(items, tam):
    """Devolvé cuántos bloques de tam salen."""
    # TU CÓDIGO ACÁ


# El chunk i
# Devolvé el bloque número `i` (empezando en 0) de tamaño `tam`.
# Ejemplo:  chunk_n([1, 2, 3, 4, 5], 2, 1)  →  [3, 4]
def chunk_n(items, tam, i):
    """Devolvé el bloque i de tamaño tam."""
    # TU CÓDIGO ACÁ


# Tamaños de los chunks
# Devolvé una lista con el tamaño de cada bloque.
# Ejemplo:  tamanos_chunks([1, 2, 3, 4, 5], 2)  →  [2, 2, 1]
def tamanos_chunks(items, tam):
    """Devolvé el tamaño de cada bloque."""
    # TU CÓDIGO ACÁ


# El último chunk
# Devolvé el último bloque, o [] si no hay items.
def ultimo_chunk(items, tam):
    """Devolvé el último bloque."""
    # TU CÓDIGO ACÁ


# Tamaño por hilo
# Si repartís `total` items entre `hilos` hilos, devolvé cuántos le tocan a cada uno (redondeando
# para arriba).  Ejemplo:  tamano_por_hilo(10, 3)  →  4
def tamano_por_hilo(total, hilos):
    """Devolvé el tamaño por hilo (redondeo hacia arriba)."""
    # TU CÓDIGO ACÁ


# El chunk más grande
# `chunks` es una lista de listas. Devolvé el bloque con más items.
def chunk_mas_grande(chunks):
    """Devolvé el bloque más grande."""
    # TU CÓDIGO ACÁ


# Total de items
# Devolvé la cantidad total de items sumando todos los bloques.
def total_items(chunks):
    """Devolvé el total de items en todos los bloques."""
    # TU CÓDIGO ACÁ


# ¿Balanceado?
# Devolvé True si la diferencia de tamaño entre el bloque más grande y el más chico es 1 o menos.
def balanceado(chunks):
    """Devolvé True si los bloques están balanceados."""
    # TU CÓDIGO ACÁ


# Dividir en N partes
# Partí `items` en EXACTAMENTE `n` bloques lo más parejos posible (los primeros se llevan el
# resto). Devolvé la lista de bloques.
# Ejemplo:  dividir_en_n([1, 2, 3, 4, 5], 2)  →  [[1, 2, 3], [4, 5]]
def dividir_en_n(items, n):
    """Partí items en n bloques parejos."""
    # TU CÓDIGO ACÁ


# Promedio de tamaño
# Devolvé el tamaño promedio de los bloques.
def promedio_tamano(chunks):
    """Devolvé el tamaño promedio de los bloques."""
    # TU CÓDIGO ACÁ


# Bloques no vacíos
# Devolvé solo los bloques que tienen al menos un item.
def chunks_no_vacios(chunks):
    """Devolvé los bloques no vacíos."""
    # TU CÓDIGO ACÁ


# ¿En qué chunk cae?
# Devolvé en qué bloque (empezando en 0) cae la posición `pos`, con bloques de tamaño `tam`.
# Ejemplo:  indice_de_chunk([1, 2, 3, 4, 5], 2, 3)  →  1
def indice_de_chunk(items, tam, pos):
    """Devolvé el índice del bloque donde cae pos."""
    # TU CÓDIGO ACÁ


# ¿Entra en N bloques?
# Devolvé True si `total` items, en bloques de `tam`, entran en `max_chunks` bloques o menos.
def cabe_en_chunks(total, tam, max_chunks):
    """Devolvé True si entra en max_chunks bloques."""
    # TU CÓDIGO ACÁ


# Asignar round-robin
# Repartí `items` entre `hilos` hilos por turno. Devolvé un dict índice_de_hilo → lista de items.
# Ejemplo:  asignar_round_robin(["a", "b", "c"], 2)  →  {0: ["a", "c"], 1: ["b"]}
def asignar_round_robin(items, hilos):
    """Devolvé un dict hilo → items."""
    # TU CÓDIGO ACÁ


# El primer chunk
# Devolvé el primer bloque de tamaño `tam`.
def primer_chunk(items, tam):
    """Devolvé el primer bloque."""
    # TU CÓDIGO ACÁ


# El chunk más chico
# Devolvé el bloque con menos items.
def chunk_mas_chico(chunks):
    """Devolvé el bloque más chico."""
    # TU CÓDIGO ACÁ
