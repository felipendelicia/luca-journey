"""✏️ Ejercicios — ML: evaluar modelos

Un modelo solo sirve si ACIERTA. Se separa en entrenamiento y prueba, y se mide la
EXACTITUD (accuracy) sobre datos que el modelo nunca vio. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# Exactitud (accuracy)
# Calculá la proporción de aciertos comparando lo real con lo predicho.
# Pista: accuracy_score(y_real, y_pred).
# Ejemplo:  precision([0, 1, 1, 0], [0, 1, 0, 0])  →  0.75   (3 de 4)
def precision(y_real, y_pred):
    """Devolvé accuracy_score(y_real, y_pred)."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar y evaluar
# Dividí 50/50 (test_size=0.5, random_state=0), entrená un KNN(1) con el train y devolvé
# la exactitud sobre el test. Pista: accuracy_score(y_test, modelo.predict(X_test)).
def evaluar(X, y):
    """Devolvé la exactitud del KNN(1) sobre el test."""
    # TU CÓDIGO ACÁ
    pass


# El score del modelo
# Devolvé el score de un modelo YA entrenado sobre datos de prueba. Pista: modelo.score(X_test, y_test).
def score_modelo(modelo, X_test, y_test):
    """Devolvé modelo.score(X_test, y_test)."""
    # TU CÓDIGO ACÁ
    pass
