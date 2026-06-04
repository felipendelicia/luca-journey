"""✏️ Ejercicios — ML: preparar los datos

Antes de entrenar hay que preparar los datos: separar features (X) de etiquetas (y),
dividir en entrenamiento/prueba y a veces escalar. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Features y etiquetas
# Separá una matriz en X (todas las columnas menos la última) e y (la última).
# Pista: X = matriz[:, :-1] ; y = matriz[:, -1]. Devolvé la tupla (X, y).
def separar_columnas(matriz):
    """Devolvé (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Train / test
# Dividí en entrenamiento y prueba (25% de test), con random_state=42 para que sea
# reproducible. Devolvé los 4 valores de train_test_split.
# Pista: return train_test_split(X, y, test_size=0.25, random_state=42).
def dividir(X, y):
    """Devolvé X_train, X_test, y_train, y_test."""
    # TU CÓDIGO ACÁ
    pass


# Escalar los datos
# Escalá para que cada columna tenga media 0 y desvío 1. Pista: StandardScaler().fit_transform(X).
def escalar(X):
    """Devolvé el array escalado."""
    # TU CÓDIGO ACÁ
    pass


# ¿Cuántas features?
# Devolvé cuántas features (columnas) tiene X, como int. Pista: X.shape[1].
# Ejemplo:  una X de 5 filas y 3 columnas  →  3
def cantidad_features(X):
    """Devolvé la cantidad de columnas de X (int)."""
    # TU CÓDIGO ACÁ
    pass
