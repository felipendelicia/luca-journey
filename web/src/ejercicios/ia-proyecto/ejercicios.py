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
