"""✅ Soluciones — NumPy: Arrays"""
import numpy as np


# 1) Convertí una lista de niveles en un array de NumPy.
def crear_equipo(niveles):
    """Recibí una lista (ej: [5, 12, 30]) y devolvé un np.array con esos valores."""
    return np.array(niveles)


# 2) Devolvé un array con los niveles del 1 al n (inclusive). Usá np.arange.
def rango_niveles(n):
    """Para n=5 devolvé array([1, 2, 3, 4, 5])."""
    return np.arange(1, n + 1)


# 3) Devolvé un array de n ceros. Usá np.zeros.
def tanque_vacio(n):
    """Para n=3 devolvé array([0., 0., 0.])."""
    return np.zeros(n)


# 4) Duplicá cada valor del array (vectorizado, sin for).
def doblar_ataque(ataques):
    """Recibí un array y devolvé otro con cada elemento multiplicado por 2."""
    return ataques * 2


# 5) Sumá dos arrays elemento a elemento.
def sumar_stats(a, b):
    """Recibí dos arrays del mismo tamaño y devolvé la suma elemento a elemento."""
    return a + b


# 6) Devolvé los primeros 3 elementos del array (slicing).
def primeros_tres(arr):
    """Devolvé un array con los primeros 3 elementos."""
    return arr[:3]


# 7) Devolvé solo los valores mayores al umbral (máscara booleana).
def superan_umbral(arr, umbral):
    """Devolvé un array con los elementos de arr que son > umbral."""
    return arr[arr > umbral]


# 8) Devolvé la forma (shape) del array como una tupla.
def forma(arr):
    """Devolvé arr.shape (una tupla)."""
    return arr.shape


# 9) Aplaná una matriz 2D a un array 1D. Usá .flatten() o .ravel().
def aplanar(matriz):
    """Recibí un array 2D y devolvé su versión 1D."""
    return matriz.flatten()


def sumar_arrays(a, b):
    return a + b


def mayores_a(a, n):
    return a[a > n]


def contar_mayores(a, n):
    return int((a > n).sum())


def array_de(valor, n):
    return np.full(n, valor)


def invertir_array(a):
    return a[::-1]


def primeros_n(a, n):
    return a[:n]


def ultimos_n(a, n):
    return a[-n:]


def multiplicar_por(a, k):
    return a * k


def reemplazar_negativos(a):
    b = a.copy()
    b[b < 0] = 0
    return b


def indices_donde(a, n):
    return np.where(a == n)[0]


def concatenar(a, b):
    return np.concatenate([a, b])
