"""
✏️ Ejercicios — ML: evaluar modelos

Un modelo solo sirve si ACIERTA. Para saberlo, se separa en entrenamiento y prueba,
y se mide la EXACTITUD (accuracy) sobre datos que el modelo nunca vio.
"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


# 1) Calculá la exactitud comparando lo real con lo predicho. Usá accuracy_score.
def precision(y_real, y_pred):
    """Devolvé accuracy_score(y_real, y_pred) (proporción de aciertos, 0 a 1)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Entrená un KNN(1) con el 50% de los datos y devolvé la exactitud sobre el otro 50%.
#    Usá train_test_split(..., test_size=0.5, random_state=0).
def evaluar(X, y):
    """Dividí, entrená con train, y devolvé accuracy_score(y_test, predicciones)."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé el score de un modelo ya entrenado sobre datos de prueba. Usá modelo.score.
def score_modelo(modelo, X_test, y_test):
    """Pista: modelo.score(X_test, y_test)."""
    # TU CÓDIGO ACÁ
    pass
