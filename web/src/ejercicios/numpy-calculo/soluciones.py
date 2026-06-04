"""✅ Soluciones — NumPy: Cálculo numérico"""
import numpy as np


# 1) Devolvé la suma de todos los valores del array.
def total_stats(arr):
    """Para [10, 20, 30] devolvé 60."""
    return arr.sum()


# 2) Devolvé el promedio (media) del array.
def promedio(arr):
    """Para [10, 20, 30] devolvé 20.0."""
    return arr.mean()


# 3) Devolvé el valor máximo del array.
def mas_fuerte(arr):
    """Devolvé el máximo de arr."""
    return arr.max()


# 4) Devolvé el desvío estándar del array (arr.std()).
def desviacion(arr):
    """Devolvé el desvío estándar."""
    return arr.std()


# 5) Sumá una matriz 2D por COLUMNA. Usá axis=0.
def suma_por_columna(matriz):
    """Para [[1,2],[3,4]] devolvé array([4, 6])."""
    return matriz.sum(axis=0)


# 6) Sumá una matriz 2D por FILA. Usá axis=1.
def suma_por_fila(matriz):
    """Para [[1,2],[3,4]] devolvé array([3, 7])."""
    return matriz.sum(axis=1)


# 7) Contá cuántos valores del array son mayores al umbral. Devolvé un int.
def contar_mayores(arr, umbral):
    """Usá una máscara booleana y .sum(). Devolvé un int."""
    return int((arr > umbral).sum())


# 8) Normalizá el array al rango 0..1:  (x - min) / (max - min).
def normalizar(arr):
    """Devolvé el array escalado entre 0 y 1."""
    return (arr - arr.min()) / (arr.max() - arr.min())


# 9) Reemplazá los valores negativos por 0 (los demás quedan igual). Usá np.where.
def sin_negativos(arr):
    """Para [-3, 5, -1, 8] devolvé array([0, 5, 0, 8])."""
    return np.where(arr < 0, 0, arr)
