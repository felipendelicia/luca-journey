"""✏️ Ejercicios — ML: árboles de decisión

Un árbol aprende reglas tipo "si ataque > 25 entonces Fuego". Es fácil de entender y
te dice qué tan IMPORTANTE fue cada feature para decidir. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


# Entrenar el árbol
# Entrená un árbol de decisión con random_state=0 (para que sea reproducible).
# Pista: DecisionTreeClassifier(random_state=0).fit(X, y).
def entrenar_arbol(X, y):
    """Devolvé un árbol entrenado."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar con el árbol
# Clasificá una fila y devolvé un int. Pista: int(modelo.predict([fila])[0]).
def clasificar(modelo, fila):
    """Devolvé la categoría de 'fila' (int)."""
    # TU CÓDIGO ACÁ
    pass


# Importancia de las features
# Devolvé la importancia de cada feature como lista de floats. Pista: list(modelo.feature_importances_).
# Ejemplo:  si solo la 1ra feature decide  →  [1.0, 0.0]
def importancias(modelo):
    """Devolvé la lista de importancias."""
    # TU CÓDIGO ACÁ
    pass
