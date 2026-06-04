"""
✏️ Ejercicios — ML: clasificación

Clasificar = predecir una CATEGORÍA (ej: el tipo de un Pokémon a partir de sus stats).
Usamos KNeighborsClassifier: mira los k vecinos más parecidos y vota.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# 1) Entrená un clasificador KNN con k=3 vecinos. Devolvé el modelo entrenado.
def entrenar_clasificador(X, y):
    """KNeighborsClassifier(n_neighbors=3).fit(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Clasificá una fila. Devolvé la categoría como int.
def clasificar(modelo, fila):
    """int(modelo.predict([fila])[0])."""
    # TU CÓDIGO ACÁ
    pass


# 3) Clasificá VARIAS filas de una. Devolvé una lista de ints.
def clasificar_varios(modelo, filas):
    """Pista: [int(v) for v in modelo.predict(filas)]."""
    # TU CÓDIGO ACÁ
    pass
