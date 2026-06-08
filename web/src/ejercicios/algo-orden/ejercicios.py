"""🔢 Ejercicios — Ordenar listas

Ordenar es un clásico. Python tiene sorted(), pero entender CÓMO se ordena te enseña a
pensar algoritmos. Acá implementás el orden a mano. ✅ Corregí cuando termines.
"""


# Índice del mínimo
# Devolvé el índice del elemento más chico de la lista (el primero si hay empate).
# (Sin usar min().) Ejemplo:  indice_minimo([30, 10, 20])  →  1
def indice_minimo(lista):
    """Devolvé el índice del valor mínimo."""


# ¿Está ordenada?
# Devolvé True si la lista está de menor a mayor (cada elemento <= el siguiente).
# Ejemplo:  esta_ordenada([1, 2, 2, 3])  →  True   ·   esta_ordenada([3, 1])  →  False
def esta_ordenada(lista):
    """Devolvé True si la lista está ordenada ascendente."""


# Ordenamiento burbuja
# Ordená la lista de menor a mayor con el método BURBUJA (comparar pares vecinos e
# intercambiarlos). Devolvé una lista NUEVA ordenada (no uses sorted()).
# Ejemplo:  ordenar_burbuja([3, 1, 2])  →  [1, 2, 3]
def ordenar_burbuja(lista):
    """Devolvé una lista nueva ordenada con burbuja."""


# Ordenamiento por selección
# Ordená buscando el mínimo y poniéndolo adelante, repetidamente. Devolvé una lista NUEVA.
# (Podés apoyarte en indice_minimo.) Ejemplo:  ordenar_seleccion([3, 1, 2])  →  [1, 2, 3]
def ordenar_seleccion(lista):
    """Devolvé una lista nueva ordenada por selección."""


# Ordenamiento por inserción
# Ordená de menor a mayor con el método INSERCIÓN (tomar cada elemento y meterlo en su
# lugar entre los ya ordenados). Devolvé una lista NUEVA, sin usar sorted().
# Ejemplo:  ordenar_insercion([3, 1, 2])  →  [1, 2, 3]
def ordenar_insercion(lista):
    """Devolvé la lista ordenada con inserción."""
    # TU CÓDIGO ACÁ


# Ordenar de mayor a menor
# Devolvé la lista ordenada de MAYOR a menor. (Acá sí podés usar sorted con su parámetro.)
# Ejemplo:  ordenar_desc([1, 3, 2])  →  [3, 2, 1]
def ordenar_desc(lista):
    """Devolvé la lista ordenada de mayor a menor."""
    # TU CÓDIGO ACÁ


# El segundo más chico
# Devolvé el segundo valor más chico de la lista (asumí que tiene al menos 2 elementos).
# Ejemplo:  segundo_menor([5, 1, 3])  →  3
def segundo_menor(lista):
    """Devolvé el segundo valor más chico."""
    # TU CÓDIGO ACÁ


# Mediana
# Devolvé la mediana: el valor del medio si la cantidad es impar, o el promedio de los dos
# del medio si es par. Ordená primero.
# Ejemplo:  mediana([3, 1, 2])  →  2   ·   mediana([1, 2, 3, 4])  →  2.5
def mediana(lista):
    """Devolvé la mediana de la lista."""
    # TU CÓDIGO ACÁ


# Los N más grandes
# Devolvé los `n` valores más grandes, ordenados de mayor a menor.
# Ejemplo:  top_n([4, 1, 7, 3], 2)  →  [7, 4]
def top_n(lista, n):
    """Devolvé los n valores más grandes, de mayor a menor."""
    # TU CÓDIGO ACÁ


# Ordenar por longitud
# `palabras` es una lista de strings. Devolvela ordenada por LARGO (de más corta a más larga).
# Ejemplo:  ordenar_por_longitud(["onix", "pi", "eevee"])  →  ["pi", "onix", "eevee"]
def ordenar_por_longitud(palabras):
    """Devolvé las palabras ordenadas por longitud."""
    # TU CÓDIGO ACÁ


# Mezclar dos ordenadas
# `a` y `b` ya vienen ordenadas de menor a mayor. Devolvé UNA lista con todos los elementos,
# también ordenada, recorriendo ambas a la vez (sin volver a ordenar todo).
# Ejemplo:  mezclar_ordenadas([1, 4], [2, 3, 5])  →  [1, 2, 3, 4, 5]
def mezclar_ordenadas(a, b):
    """Devolvé la mezcla ordenada de a y b."""
    # TU CÓDIGO ACÁ


# ¿Ordenada de mayor a menor?
# Devolvé True si la lista está de MAYOR a menor.
# Ejemplo:  esta_ordenada_desc([5, 3, 1])  →  True   ·   esta_ordenada_desc([1, 2])  →  False
def esta_ordenada_desc(lista):
    """Devolvé True si la lista está de mayor a menor."""
    # TU CÓDIGO ACÁ


# Únicos ordenados
# Devolvé los valores SIN repetir, ordenados de menor a mayor.
# Ejemplo:  unicos_ordenados([3, 1, 3, 2, 1])  →  [1, 2, 3]
def unicos_ordenados(lista):
    """Devolvé los valores únicos, ordenados."""
    # TU CÓDIGO ACÁ


# Invertir
# Devolvé una lista NUEVA con los elementos al revés, hecho a mano (sin [::-1] ni .reverse()).
# Ejemplo:  invertir([1, 2, 3])  →  [3, 2, 1]
def invertir(lista):
    """Devolvé la lista al revés."""
    # TU CÓDIGO ACÁ


# El k-ésimo más chico
# Devolvé el k-ésimo valor más chico (k empieza en 1: k=1 es el mínimo).
# Ejemplo:  kesimo_menor([7, 3, 9, 1], 2)  →  3
def kesimo_menor(lista, k):
    """Devolvé el k-ésimo valor más chico (k desde 1)."""
    # TU CÓDIGO ACÁ


# Ordenar por valor absoluto
# Devolvé la lista ordenada según el valor ABSOLUTO de cada número.
# Ejemplo:  ordenar_absoluto([-5, 2, -1, 3])  →  [-1, 2, 3, -5]
def ordenar_absoluto(lista):
    """Devolvé la lista ordenada por valor absoluto."""
    # TU CÓDIGO ACÁ


# Contar intercambios
# Devolvé cuántos INTERCAMBIOS hace el ordenamiento burbuja para ordenar la lista.
# Ejemplo:  contar_swaps_burbuja([2, 1])  →  1   ·   contar_swaps_burbuja([1, 2, 3])  →  0
def contar_swaps_burbuja(lista):
    """Devolvé cuántos swaps hace burbuja al ordenar."""
    # TU CÓDIGO ACÁ


# Ordenar por una clave
# `personas` es una lista de diccionarios. Devolvela ordenada por el valor de `clave`.
# Ejemplo:  ordenar_por_clave([{"n": "A", "nv": 9}, {"n": "B", "nv": 3}], "nv")
#           →  [{"n": "B", "nv": 3}, {"n": "A", "nv": 9}]
def ordenar_por_clave(personas, clave):
    """Devolvé los diccionarios ordenados por personas[i][clave]."""
    # TU CÓDIGO ACÁ


# El podio
# Devolvé los 3 valores más grandes, de mayor a menor (o menos, si la lista es más corta).
# Ejemplo:  podio([4, 9, 1, 7, 2])  →  [9, 7, 4]
def podio(lista):
    """Devolvé los 3 más grandes, de mayor a menor."""
    # TU CÓDIGO ACÁ


# El rango
# Devolvé la diferencia entre el valor más grande y el más chico.
# Ejemplo:  rango([3, 9, 1])  →  8
def rango(lista):
    """Devolvé máximo - mínimo."""
    # TU CÓDIGO ACÁ
