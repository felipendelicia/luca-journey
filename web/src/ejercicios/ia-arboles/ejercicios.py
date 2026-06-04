"""
✏️ Ejercicios — ML: árboles de decisión

Un árbol de decisión aprende reglas tipo "si ataque > 25 entonces Fuego". Es fácil
de entender y te dice qué tan IMPORTANTE fue cada feature para decidir.
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# 1) Entrená un árbol de decisión. Usá random_state=0 para que sea reproducible.
def entrenar_arbol(X, y):
    """DecisionTreeClassifier(random_state=0).fit(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Clasificá una fila con el árbol. Devolvé un int.
def clasificar(modelo, fila):
    """int(modelo.predict([fila])[0])."""
    # TU CÓDIGO ACÁ
    pass


# 3) Devolvé la importancia de cada feature (una lista de floats).
def importancias(modelo):
    """Pista: list(modelo.feature_importances_)."""
    # TU CÓDIGO ACÁ
    pass
