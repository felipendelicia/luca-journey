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
