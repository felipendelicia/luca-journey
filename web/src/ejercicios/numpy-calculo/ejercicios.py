"""✏️ Ejercicios — NumPy: Cálculo numérico

Agregaciones, ejes (axis), máscaras booleanas y np.where. ✅ Corregir al terminar.
"""
import numpy as np


# Suma total
# Devolvé la suma de todos los valores del array.
# Ejemplo:  total_stats(np.array([10, 20, 30]))  →  60
def total_stats(arr):
    """Devolvé la suma de arr."""
    # TU CÓDIGO ACÁ
    pass


# Promedio
# Devolvé el promedio (media) del array.
# Ejemplo:  promedio(np.array([10, 20, 30]))  →  20.0
def promedio(arr):
    """Devolvé el promedio de arr."""
    # TU CÓDIGO ACÁ
    pass


# El más fuerte
# Devolvé el valor máximo del array.
# Ejemplo:  mas_fuerte(np.array([45, 90, 12]))  →  90
def mas_fuerte(arr):
    """Devolvé el máximo de arr."""
    # TU CÓDIGO ACÁ
    pass


# Desvío estándar
# Devolvé el desvío estándar del array. Pista: arr.std().
# Ejemplo:  desviacion(np.array([10, 10, 10]))  →  0.0
def desviacion(arr):
    """Devolvé el desvío estándar."""
    # TU CÓDIGO ACÁ
    pass


# Suma por columna
# Sumá una matriz 2D por COLUMNA. Pista: axis=0.
# Ejemplo:  suma_por_columna(np.array([[1, 2], [3, 4]]))  →  array([4, 6])
def suma_por_columna(matriz):
    """Devolvé la suma por columna (axis=0)."""
    # TU CÓDIGO ACÁ
    pass


# Suma por fila
# Sumá una matriz 2D por FILA. Pista: axis=1.
# Ejemplo:  suma_por_fila(np.array([[1, 2], [3, 4]]))  →  array([3, 7])
def suma_por_fila(matriz):
    """Devolvé la suma por fila (axis=1)."""
    # TU CÓDIGO ACÁ
    pass


# Contar mayores
# Contá cuántos valores del array son mayores al umbral. Pista: (arr > umbral).sum().
# Devolvé un int.
# Ejemplo:  contar_mayores(np.array([10, 40, 25, 80]), 30)  →  2
def contar_mayores(arr, umbral):
    """Devolvé cuántos valores son > umbral (int)."""
    # TU CÓDIGO ACÁ
    pass


# Normalizar 0..1
# Escalá el array al rango 0 a 1 con la fórmula (x - min) / (max - min).
# Ejemplo:  normalizar(np.array([0, 5, 10]))  →  array([0. , 0.5, 1. ])
def normalizar(arr):
    """Devolvé el array escalado entre 0 y 1."""
    # TU CÓDIGO ACÁ
    pass


# Sin negativos
# Reemplazá los valores negativos por 0 (los demás quedan igual). Pista: np.where.
# Ejemplo:  sin_negativos(np.array([-3, 5, -1, 8]))  →  array([0, 5, 0, 8])
def sin_negativos(arr):
    """Devolvé el array con los negativos puestos en 0."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo
# Devolvé el valor más chico del array, como int.
def minimo(arr):
    """Devolvé el mínimo (int)."""
    # TU CÓDIGO ACÁ
    pass


# Máximo
# Devolvé el valor más grande del array, como int.
def maximo(arr):
    """Devolvé el máximo (int)."""
    # TU CÓDIGO ACÁ
    pass


# Rango
# Devolvé la diferencia entre el máximo y el mínimo, como int.
# Ejemplo:  rango(np.array([3, 9, 1]))  →  8
def rango(arr):
    """Devolvé máximo - mínimo (int)."""
    # TU CÓDIGO ACÁ
    pass


# Producto
# Devolvé el producto de todos los elementos, como int. Pista: .prod().
# Ejemplo:  producto(np.array([2, 3, 4]))  →  24
def producto(arr):
    """Devolvé el producto de los elementos (int)."""
    # TU CÓDIGO ACÁ
    pass


# Raíz cuadrada (vectorizada)
# Devolvé un array con la raíz cuadrada de cada elemento. Pista: np.sqrt.
# Ejemplo:  raiz(np.array([4, 9, 16]))  →  array([2., 3., 4.])
def raiz(arr):
    """Devolvé la raíz de cada elemento."""
    # TU CÓDIGO ACÁ
    pass


# Suma acumulada
# Devolvé un array con la suma acumulada. Pista: np.cumsum.
# Ejemplo:  acumulado(np.array([1, 2, 3, 4]))  →  array([1, 3, 6, 10])
def acumulado(arr):
    """Devolvé la suma acumulada."""
    # TU CÓDIGO ACÁ
    pass


# Media por fila
# `matriz` es 2D. Devolvé un array con el PROMEDIO de cada fila (usá axis=1).
# Ejemplo:  media_por_fila(np.array([[2, 4], [10, 20]]))  →  array([ 3., 15.])
def media_por_fila(matriz):
    """Devolvé el promedio de cada fila."""
    # TU CÓDIGO ACÁ
    pass


# Máximo por columna
# Devolvé un array con el MÁXIMO de cada columna (usá axis=0).
# Ejemplo:  maximo_por_columna(np.array([[1, 9], [7, 2]]))  →  array([7, 9])
def maximo_por_columna(matriz):
    """Devolvé el máximo de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Recortar al rango (clip)
# Devolvé un array donde cada valor queda entre `lo` y `hi`. Pista: np.clip.
# Ejemplo:  clip_valores(np.array([-5, 50, 200]), 0, 100)  →  array([  0,  50, 100])
def clip_valores(arr, lo, hi):
    """Devolvé el array recortado a [lo, hi]."""
    # TU CÓDIGO ACÁ
    pass


# Proporción de mayores
# Devolvé la FRACCIÓN de elementos mayores que `n` (un float entre 0 y 1).
# Ejemplo:  proporcion_mayores(np.array([1, 2, 3, 4]), 2)  →  0.5
def proporcion_mayores(arr, n):
    """Devolvé la fracción de elementos mayores que n."""
    # TU CÓDIGO ACÁ
    pass


# Dejar los mayores, el resto 0
# Devolvé un array donde los valores mayores que `n` quedan igual y el resto pasa a 0.
# Pista: np.where.  Ejemplo:  donde_mayor(np.array([1, 5, 2, 9]), 3)  →  array([0, 5, 0, 9])
def donde_mayor(arr, n):
    """Devolvé los mayores que n, el resto en 0."""
    # TU CÓDIGO ACÁ
    pass
