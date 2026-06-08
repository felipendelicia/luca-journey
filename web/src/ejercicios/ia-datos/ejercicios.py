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


# Cantidad de muestras
# Devolvé cuántas filas tiene X. Pista: X.shape[0].
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass


# Promedio de cada feature
# Devolvé el promedio de cada columna de X. Pista: X.mean(axis=0).
def promedio_features(X):
    """Devolvé el promedio de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Desviación de cada feature
# Devolvé la desviación estándar de cada columna. Pista: X.std(axis=0).
def desviacion_features(X):
    """Devolvé la desviación de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Mínimo de cada feature
# Devolvé el mínimo de cada columna. Pista: X.min(axis=0).
def minimo_features(X):
    """Devolvé el mínimo de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Máximo de cada feature
# Devolvé el máximo de cada columna. Pista: X.max(axis=0).
def maximo_features(X):
    """Devolvé el máximo de cada columna."""
    # TU CÓDIGO ACÁ
    pass


# Normalizar min-max
# Devolvé X escalado por columna a 0..1: (X - mínimo) / (máximo - mínimo).
def normalizar_min_max(X):
    """Devolvé X normalizado a 0..1 por columna."""
    # TU CÓDIGO ACÁ
    pass


# Agregar una columna
# Devolvé X con `col` agregada como nueva columna al final. Pista: np.column_stack([X, col]).
def agregar_columna(X, col):
    """Devolvé X con una columna nueva al final."""
    # TU CÓDIGO ACÁ
    pass


# Quitar una columna
# Devolvé X sin la columna número `i`. Pista: np.delete(X, i, axis=1).
def quitar_columna(X, i):
    """Devolvé X sin la columna i."""
    # TU CÓDIGO ACÁ
    pass


# Primera columna
# Devolvé la primera columna de X. Pista: X[:, 0].
def primera_columna(X):
    """Devolvé la primera columna de X."""
    # TU CÓDIGO ACÁ
    pass


# Etiquetas
# 'matriz' tiene las features y, en la ÚLTIMA columna, la etiqueta. Devolvé la última columna.
# Pista: matriz[:, -1].
def etiquetas(matriz):
    """Devolvé la última columna (las etiquetas)."""
    # TU CÓDIGO ACÁ
    pass


# Features
# Devolvé todas las columnas de `matriz` MENOS la última. Pista: matriz[:, :-1].
def features(matriz):
    """Devolvé todas las columnas menos la última."""
    # TU CÓDIGO ACÁ
    pass


# ¿Está balanceado?
# Devolvé True si todas las clases de `y` tienen la MISMA cantidad de muestras.
def balanceado(y):
    """Devolvé True si las clases están balanceadas."""
    # TU CÓDIGO ACÁ
    pass


# Dividir manual
# Devolvé (primera_parte, segunda_parte) partiendo X en la fila `int(len(X) * frac)`.
# Ejemplo:  con 4 filas y frac=0.5  →  las primeras 2 y las últimas 2.
def dividir_manual(X, frac):
    """Devolvé X partido en la fracción frac."""
    # TU CÓDIGO ACÁ
    pass


# Contar clases
# Devolvé un dict clase → cantidad. Pista: np.unique(y, return_counts=True).
def contar_clases(y):
    """Devolvé un dict clase → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Proporción de una clase
# Devolvé la FRACCIÓN de muestras que son de la clase `clase` (float).
def proporcion_clase(y, clase):
    """Devolvé la proporción de esa clase."""
    # TU CÓDIGO ACÁ
    pass


# Mezclar índices
# Devolvé una lista con los números de 0 a n-1 MEZCLADOS, usando `seed` para que el
# resultado sea reproducible. Pista: np.random.RandomState(seed).permutation(n).
def mezclar_indices(n, seed):
    """Devolvé los índices 0..n-1 mezclados (con seed)."""
    # TU CÓDIGO ACÁ
    pass
