"""✏️ Ejercicios — ML: clasificación

Clasificar = predecir una CATEGORÍA (ej: el tipo de un Pokémon por sus stats). Usamos
KNeighborsClassifier: mira los k vecinos más parecidos y vota. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# Entrenar el clasificador
# Entrená un clasificador KNN con k=3 vecinos y devolvé el modelo. Pista: KNeighborsClassifier(n_neighbors=3).fit(X, y).
def entrenar_clasificador(X, y):
    """Devolvé un KNN(3) entrenado con (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar uno
# Clasificá una fila y devolvé la categoría como int. Pista: int(modelo.predict([fila])[0]).
# Ejemplo:  clasificar(modelo, [89, 41])  →  0
def clasificar(modelo, fila):
    """Devolvé la categoría de 'fila' (int)."""
    # TU CÓDIGO ACÁ
    pass


# Clasificar varios
# Clasificá VARIAS filas de una y devolvé una lista de ints.
# Pista: [int(v) for v in modelo.predict(filas)].
# Ejemplo:  clasificar_varios(modelo, [[89, 41], [41, 89]])  →  [0, 1]
def clasificar_varios(modelo, filas):
    """Devolvé la lista de categorías (ints)."""
    # TU CÓDIGO ACÁ
    pass
