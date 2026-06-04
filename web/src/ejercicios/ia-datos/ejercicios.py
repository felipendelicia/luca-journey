"""
✏️ Ejercicios — ML: preparar los datos

Antes de entrenar hay que preparar los datos: separar features (X) de etiquetas (y),
dividir en entrenamiento/prueba, y a veces escalar para que todo esté en la misma medida.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# 1) Separá una matriz en X (todas las columnas menos la última) e y (la última).
def separar_columnas(matriz):
    """Devolvé una tupla (X, y). Pista: matriz[:, :-1] y matriz[:, -1]."""
    # TU CÓDIGO ACÁ
    pass


# 2) Dividí en entrenamiento y prueba (25% test). Usá random_state=42 para que sea
#    reproducible. Devolvé lo que devuelve train_test_split (4 valores).
def dividir(X, y):
    """return train_test_split(X, y, test_size=0.25, random_state=42)."""
    # TU CÓDIGO ACÁ
    pass


# 3) Escalá los datos para que cada columna tenga media 0 y desvío 1.
def escalar(X):
    """Usá StandardScaler().fit_transform(X). Devolvé el array escalado."""
    # TU CÓDIGO ACÁ
    pass


# 4) ¿Cuántas features (columnas) tiene X? Devolvé un int.
def cantidad_features(X):
    """Pista: X.shape[1]."""
    # TU CÓDIGO ACÁ
    pass
