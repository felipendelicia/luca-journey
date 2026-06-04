"""
✏️ Ejercicios — Proyecto: clasificador Pokédex

Junta todo Unova: a partir de las stats de un Pokémon, un modelo predice su tipo.
Pipeline completo: preparar datos → entrenar → evaluar → predecir.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# 1) Separá la matriz en X (stats: todas menos la última columna) e y (el tipo: la última).
def preparar(matriz):
    """Devolvé (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Entrená un clasificador KNN(3) con X e y. Devolvé el modelo.
def entrenar(X, y):
    """KNeighborsClassifier(n_neighbors=3).fit(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# 3) Evaluá: dividí 50/50 (random_state=0), entrená un KNN(3) y devolvé la exactitud en test.
def evaluar(X, y):
    """Devolvé accuracy_score(y_test, predicciones)."""
    # TU CÓDIGO ACÁ
    pass


# 4) Predecí el tipo de un Pokémon a partir de sus stats. Devolvé un int.
def predecir_tipo(modelo, stats):
    """int(modelo.predict([stats])[0])."""
    # TU CÓDIGO ACÁ
    pass
