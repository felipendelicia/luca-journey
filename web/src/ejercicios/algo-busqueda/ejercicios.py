"""🔎 Ejercicios — Búsqueda lineal y binaria

Buscar es lo más común en programación. La búsqueda LINEAL mira uno por uno; la BINARIA
(sobre una lista ordenada) parte el problema al medio cada vez: mucho más rápida.
✅ Corregí cuando termines.
"""


# Búsqueda lineal
# Recorré la lista y devolvé el ÍNDICE donde está `x`. Si no está, devolvé -1.
# (Hacelo a mano con un bucle, sin usar .index().)
# Ejemplo:  busqueda_lineal([10, 20, 30], 20)  →  1   ·   busqueda_lineal([10], 99)  →  -1
def busqueda_lineal(lista, x):
    """Devolvé el índice de x, o -1."""


# ¿Está?
# Devolvé True si `x` aparece en la lista, False si no.
# Ejemplo:  contiene([1, 2, 3], 2)  →  True
def contiene(lista, x):
    """Devolvé True si x está en la lista."""


# Búsqueda binaria
# `ordenada` viene de menor a mayor. Buscá `x` partiendo el rango al medio cada vez y
# devolvé su ÍNDICE, o -1 si no está. (Implementala vos, sin .index().)
# Ejemplo:  busqueda_binaria([1, 3, 5, 7, 9], 7)  →  3   ·   busqueda_binaria([1, 3, 5], 4)  →  -1
def busqueda_binaria(ordenada, x):
    """Devolvé el índice de x por búsqueda binaria, o -1."""


# Primero mayor
# En una lista ordenada, devolvé el primer elemento ESTRICTAMENTE mayor que `x`. Si no
# hay ninguno, devolvé None.
# Ejemplo:  primero_mayor([1, 3, 5, 7], 4)  →  5   ·   primero_mayor([1, 2], 9)  →  None
def primero_mayor(ordenada, x):
    """Devolvé el primer elemento mayor que x, o None."""


# Contar apariciones
# Devolvé cuántas veces aparece `x` en la lista (sin usar .count()).
# Ejemplo:  cuenta_apariciones([1, 2, 2, 3, 2], 2)  →  3
def cuenta_apariciones(lista, x):
    """Devolvé cuántas veces está x en la lista."""
    # TU CÓDIGO ACÁ


# Índice del mínimo
# Devolvé el ÍNDICE del valor más chico (sin usar min() ni .index()).
# Ejemplo:  indice_minimo([30, 10, 20])  →  1
def indice_minimo(lista):
    """Devolvé el índice del valor mínimo."""
    # TU CÓDIGO ACÁ


# Índice del máximo
# Devolvé el ÍNDICE del valor más grande (sin usar max() ni .index()).
# Ejemplo:  indice_maximo([30, 10, 20])  →  0
def indice_maximo(lista):
    """Devolvé el índice del valor máximo."""
    # TU CÓDIGO ACÁ


# Última aparición
# Devolvé el ÍNDICE de la ÚLTIMA vez que aparece `x`, o -1 si no está.
# Ejemplo:  ultimo_indice([1, 2, 1, 3], 1)  →  2
def ultimo_indice(lista, x):
    """Devolvé el índice de la última aparición de x, o -1."""
    # TU CÓDIGO ACÁ


# Todos los índices
# Devolvé una lista con TODOS los índices donde aparece `x`.
# Ejemplo:  todos_los_indices([5, 1, 5, 5], 5)  →  [0, 2, 3]
def todos_los_indices(lista, x):
    """Devolvé la lista de índices donde está x."""
    # TU CÓDIGO ACÁ


# Primer par
# Devolvé el primer número PAR de la lista, o None si no hay ninguno.
# Ejemplo:  primer_par([3, 7, 4, 9])  →  4
def primer_par(lista):
    """Devolvé el primer número par, o None."""
    # TU CÓDIGO ACÁ


# ¿Hay repetidos?
# Devolvé True si algún elemento aparece más de una vez.
# Ejemplo:  hay_repetidos([1, 2, 3, 2])  →  True   ·   hay_repetidos([1, 2, 3])  →  False
def hay_repetidos(lista):
    """Devolvé True si hay elementos repetidos."""
    # TU CÓDIGO ACÁ


# Primer repetido
# Devolvé el primer elemento que ya había aparecido antes. Si no hay, devolvé None.
# Ejemplo:  primer_repetido([1, 2, 3, 2, 1])  →  2
def primer_repetido(lista):
    """Devolvé el primer elemento repetido, o None."""
    # TU CÓDIGO ACÁ


# ¿Dos que suman?
# Devolvé True si HAY dos elementos (en distintas posiciones) que sumados dan `objetivo`.
# Ejemplo:  dos_que_suman([2, 7, 4], 11)  →  True   ·   dos_que_suman([2, 7, 4], 100)  →  False
def dos_que_suman(lista, objetivo):
    """Devolvé True si dos elementos suman objetivo."""
    # TU CÓDIGO ACÁ


# El más cercano
# Devolvé el elemento de la lista cuyo valor esté MÁS CERCA de `x`.
# Ejemplo:  mas_cercano([1, 5, 9], 6)  →  5
def mas_cercano(lista, x):
    """Devolvé el elemento más cercano a x."""
    # TU CÓDIGO ACÁ


# ¿Está ordenada?
# Devolvé True si la lista está ordenada de menor a mayor (cada elemento ≥ al anterior).
# Ejemplo:  esta_ordenada([1, 2, 2, 5])  →  True   ·   esta_ordenada([1, 3, 2])  →  False
def esta_ordenada(lista):
    """Devolvé True si la lista está ordenada de menor a mayor."""
    # TU CÓDIGO ACÁ


# Cuántos menores
# `ordenada` viene de menor a mayor. Devolvé cuántos elementos son ESTRICTAMENTE menores que `x`.
# Ejemplo:  cuantos_menores([1, 3, 5, 7], 5)  →  2
def cuantos_menores(ordenada, x):
    """Devolvé cuántos elementos son menores que x."""
    # TU CÓDIGO ACÁ


# Buscar texto
# Devolvé el ÍNDICE donde empieza la primera aparición de `sub` dentro de `texto`,
# o -1 si no aparece. (Hacelo a mano, sin .find() ni .index().)
# Ejemplo:  buscar_texto("pikachu", "ka")  →  2
def buscar_texto(texto, sub):
    """Devolvé el índice donde empieza sub en texto, o -1."""
    # TU CÓDIGO ACÁ


# Contar en rango
# Devolvé cuántos elementos están entre `a` y `b`, ambos incluidos.
# Ejemplo:  contar_en_rango([1, 5, 8, 10], 5, 9)  →  2
def contar_en_rango(lista, a, b):
    """Devolvé cuántos elementos están entre a y b (inclusive)."""
    # TU CÓDIGO ACÁ


# Intersección
# Devolvé una lista con los elementos que están en `a` Y TAMBIÉN en `b`, en el orden de `a`
# y sin repetir.
# Ejemplo:  interseccion([1, 2, 3, 2], [2, 3, 9])  →  [2, 3]
def interseccion(a, b):
    """Devolvé los elementos comunes a a y b, en orden de a, sin repetir."""
    # TU CÓDIGO ACÁ


# Posición para insertar
# `ordenada` viene de menor a mayor. Devolvé el índice donde habría que insertar `x` para
# que la lista SIGA ordenada (la primera posición cuyo valor sea ≥ x).
# Ejemplo:  posicion_para_insertar([1, 3, 5], 4)  →  2
def posicion_para_insertar(ordenada, x):
    """Devolvé el índice donde insertar x para mantener el orden."""
    # TU CÓDIGO ACÁ
