"""✏️ Ejercicios — Proyecto: clasificador Pokédex

Junta todo Unova: a partir de las stats de un Pokémon, un modelo predice su tipo.
Pipeline completo: preparar → entrenar → evaluar → predecir. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# Preparar los datos
# Separá la matriz en X (stats: todas las columnas menos la última) e y (el tipo: la última).
# Devolvé (X, y). Pista: matriz[:, :-1] y matriz[:, -1].
def preparar(matriz):
    """Devolvé (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar el clasificador
# Entrená un KNN(3) con X e y y devolvé el modelo. Pista: KNeighborsClassifier(n_neighbors=3).fit(X, y).
def entrenar(X, y):
    """Devolvé un KNN(3) entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Evaluar
# Dividí 50/50 (random_state=0), entrená un KNN(3) y devolvé la exactitud en el test.
# Pista: accuracy_score(y_test, modelo.predict(X_test)).
def evaluar(X, y):
    """Devolvé la exactitud sobre el test."""
    # TU CÓDIGO ACÁ
    pass


# Predecir el tipo
# Predecí el tipo de un Pokémon a partir de sus stats. Devolvé un int.
# Pista: int(modelo.predict([stats])[0]).
# Ejemplo:  predecir_tipo(modelo, [85, 45])  →  0   (Fuego)
def predecir_tipo(modelo, stats):
    """Devolvé el tipo predicho (int)."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de un tipo
# Devolvé cuántas muestras de `y` son del tipo `tipo` (int).
def cantidad_de_tipo(y, tipo):
    """Devolvé cuántas son de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Ataque promedio
# X tiene [ataque, defensa] por fila. Devolvé el promedio de la columna de ataque (la 0).
def ataque_promedio(X):
    """Devolvé el ataque promedio."""
    # TU CÓDIGO ACÁ
    pass


# Defensa promedio
# Devolvé el promedio de la columna de defensa (la 1).
def defensa_promedio(X):
    """Devolvé la defensa promedio."""
    # TU CÓDIGO ACÁ
    pass


# Promedio por tipo
# Devolvé el promedio (por columna) de las filas de X cuyo tipo (en `y`) sea `tipo`.
def promedio_por_tipo(X, y, tipo):
    """Devolvé el promedio de stats de ese tipo."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar por regla
# Sin ML: devolvé 0 (Fuego) si el ataque es mayor que la defensa, o 1 (Agua) si no.
# `stats` es [ataque, defensa].  Ejemplo:  clasificar_por_regla([90, 40])  →  0
def clasificar_por_regla(stats):
    """Devolvé 0 o 1 según ataque vs defensa."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de features
# Devolvé cuántas columnas tiene X.
def cantidad_features(X):
    """Devolvé la cantidad de columnas de X."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de muestras
# Devolvé cuántas filas tiene X.
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar con k vecinos
# Creá un KNeighborsClassifier con n_neighbors=k, entrenalo con (X, y) y devolvelo.
def entrenar_con_k(X, y, k):
    """Devolvé un KNN con k vecinos, ya entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Predecir varios
# Devolvé las predicciones del modelo para una lista de filas, como lista.
def predecir_varios(modelo, filas):
    """Devolvé las predicciones, como lista."""
    # TU CÓDIGO ACÁ
    pass


# Precisión
# Devolvé modelo.score(X, y).
def precision(modelo, X, y):
    """Devolvé la precisión del modelo."""
    # TU CÓDIGO ACÁ
    pass


# Distancia euclídea
# Devolvé la distancia euclídea entre dos puntos `a` y `b`.
def distancia_euclidea(a, b):
    """Devolvé la distancia entre a y b."""
    # TU CÓDIGO ACÁ
    pass


# El Pokémon más parecido
# Devolvé el ÍNDICE de la fila de X más cercana (en distancia euclídea) a `stats`.
def indice_mas_parecido(stats, X):
    """Devolvé el índice de la fila más parecida."""
    # TU CÓDIGO ACÁ
    pass


# Contar tipos
# Devolvé un dict tipo → cantidad.
def contar_tipos(y):
    """Devolvé un dict tipo → cantidad."""
    # TU CÓDIGO ACÁ
    pass


# Ataque máximo
# Devolvé el mayor valor de la columna de ataque (la 0).
def ataque_maximo(X):
    """Devolvé el ataque máximo."""
    # TU CÓDIGO ACÁ
    pass


# El de mayor ataque
# Devolvé el ÍNDICE de la fila con el ataque más alto. Pista: X[:, 0].argmax().
def indice_mas_fuerte(X):
    """Devolvé el índice del de mayor ataque."""
    # TU CÓDIGO ACÁ
    pass


# Normalizar min-max
# Devolvé X escalado por columna a 0..1: (X - mínimo) / (máximo - mínimo).
def normalizar_min_max(X):
    """Devolvé X normalizado a 0..1 por columna."""
    # TU CÓDIGO ACÁ
    pass
