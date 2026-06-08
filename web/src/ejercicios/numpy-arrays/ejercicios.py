"""✏️ Ejercicios — NumPy: Arrays

Arrays de NumPy (importado como np): crear, operar vectorizado, slicing y máscaras.
✅ Corregir al terminar.
"""
import numpy as np


# Lista a array
# Convertí una lista de niveles en un array de NumPy. Pista: np.array(...).
# Ejemplo:  crear_equipo([5, 12, 30])  →  array([ 5, 12, 30])
def crear_equipo(niveles):
    """Devolvé un np.array con los valores de la lista."""
    # TU CÓDIGO ACÁ
    pass


# Rango de niveles
# Devolvé un array con los niveles del 1 al n (inclusive). Pista: np.arange.
# Ejemplo:  rango_niveles(5)  →  array([1, 2, 3, 4, 5])
def rango_niveles(n):
    """Devolvé array([1, 2, ..., n])."""
    # TU CÓDIGO ACÁ
    pass


# Tanque vacío
# Devolvé un array de n ceros. Pista: np.zeros.
# Ejemplo:  tanque_vacio(3)  →  array([0., 0., 0.])
def tanque_vacio(n):
    """Devolvé un array de n ceros."""
    # TU CÓDIGO ACÁ
    pass


# Doblar ataque (vectorizado)
# Duplicá cada valor del array, sin usar un for (NumPy opera todo de una).
# Ejemplo:  doblar_ataque(np.array([10, 20, 30]))  →  array([20, 40, 60])
def doblar_ataque(ataques):
    """Devolvé el array con cada elemento × 2."""
    # TU CÓDIGO ACÁ
    pass


# Sumar stats
# Sumá dos arrays del mismo tamaño, elemento a elemento.
# Ejemplo:  sumar_stats(np.array([1, 2]), np.array([3, 4]))  →  array([4, 6])
def sumar_stats(a, b):
    """Devolvé la suma elemento a elemento."""
    # TU CÓDIGO ACÁ
    pass


# Primeros tres
# Devolvé los primeros 3 elementos del array (slicing).
# Ejemplo:  primeros_tres(np.array([5, 1, 8, 3, 9]))  →  array([5, 1, 8])
def primeros_tres(arr):
    """Devolvé los primeros 3 elementos."""
    # TU CÓDIGO ACÁ
    pass


# Superan el umbral
# Devolvé solo los valores mayores al umbral. Pista: máscara booleana arr[arr > umbral].
# Ejemplo:  superan_umbral(np.array([10, 40, 25]), 30)  →  array([40])
def superan_umbral(arr, umbral):
    """Devolvé los elementos de arr que son > umbral."""
    # TU CÓDIGO ACÁ
    pass


# Forma del array
# Devolvé la forma (shape) del array como tupla. Pista: arr.shape.
# Ejemplo:  un array de 2 filas y 3 columnas  →  forma(arr)  →  (2, 3)
def forma(arr):
    """Devolvé arr.shape."""
    # TU CÓDIGO ACÁ
    pass


# Aplanar matriz
# Convertí una matriz 2D en un array 1D. Pista: .flatten() o .ravel().
# Ejemplo:  aplanar(np.array([[1, 2], [3, 4]]))  →  array([1, 2, 3, 4])
def aplanar(matriz):
    """Devolvé la versión 1D de la matriz."""
    # TU CÓDIGO ACÁ
    pass


# Sumar dos arrays
# Devolvé la suma elemento a elemento (vectorizado, sin for).
# Ejemplo:  sumar_arrays(np.array([1, 2]), np.array([10, 20]))  →  array([11, 22])
def sumar_arrays(a, b):
    """Devolvé a + b."""
    # TU CÓDIGO ACÁ
    pass


# Mayores a n (máscara)
# Devolvé un array con solo los elementos mayores que `n` (usá una máscara booleana).
# Ejemplo:  mayores_a(np.array([5, 20, 12, 30]), 15)  →  array([20, 30])
def mayores_a(a, n):
    """Devolvé los elementos mayores que n."""
    # TU CÓDIGO ACÁ
    pass


# Contar mayores
# Devolvé CUÁNTOS elementos son mayores que `n` (como int).
# Ejemplo:  contar_mayores(np.array([5, 20, 30]), 15)  →  2
def contar_mayores(a, n):
    """Devolvé cuántos elementos son mayores que n."""
    # TU CÓDIGO ACÁ
    pass


# Array lleno de un valor
# Devolvé un array de `n` elementos, todos iguales a `valor`. Pista: np.full.
# Ejemplo:  array_de(7, 3)  →  array([7, 7, 7])
def array_de(valor, n):
    """Devolvé un array de n veces valor."""
    # TU CÓDIGO ACÁ
    pass


# Invertir
# Devolvé el array al revés (sin usar for).
# Ejemplo:  invertir_array(np.array([1, 2, 3]))  →  array([3, 2, 1])
def invertir_array(a):
    """Devolvé el array invertido."""
    # TU CÓDIGO ACÁ
    pass


# Primeros n
# Devolvé los primeros `n` elementos.
def primeros_n(a, n):
    """Devolvé los primeros n elementos."""
    # TU CÓDIGO ACÁ
    pass


# Últimos n
# Devolvé los últimos `n` elementos.
def ultimos_n(a, n):
    """Devolvé los últimos n elementos."""
    # TU CÓDIGO ACÁ
    pass


# Multiplicar por k
# Devolvé el array con cada elemento multiplicado por `k`.
def multiplicar_por(a, k):
    """Devolvé a × k."""
    # TU CÓDIGO ACÁ
    pass


# Reemplazar negativos por 0
# Devolvé un array NUEVO donde los valores negativos quedan en 0 (los demás igual).
# Ejemplo:  reemplazar_negativos(np.array([-3, 5, -1, 2]))  →  array([0, 5, 0, 2])
def reemplazar_negativos(a):
    """Devolvé el array con los negativos en 0."""
    # TU CÓDIGO ACÁ
    pass


# Índices donde
# Devolvé los ÍNDICES donde el array vale `n`. Pista: np.where.
# Ejemplo:  indices_donde(np.array([5, 9, 5, 1]), 5)  →  array([0, 2])
def indices_donde(a, n):
    """Devolvé los índices donde a == n."""
    # TU CÓDIGO ACÁ
    pass


# Concatenar
# Devolvé un array con los elementos de `a` seguidos por los de `b`. Pista: np.concatenate.
# Ejemplo:  concatenar(np.array([1, 2]), np.array([3, 4]))  →  array([1, 2, 3, 4])
def concatenar(a, b):
    """Devolvé a y b concatenados."""
    # TU CÓDIGO ACÁ
    pass
