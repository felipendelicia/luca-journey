"""
✏️ Ejercicios — ML: tu primer modelo

Machine Learning = enseñarle a un modelo con EJEMPLOS para que después prediga
solo. Le das X (datos) e y (la respuesta correcta), hace .fit(), y luego .predict().
Acá usamos un clasificador de vecinos (KNN).
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# 1) Creá un clasificador KNN que mire al vecino más cercano (n_neighbors=1).
def crear_modelo():
    """Devolvé un KNeighborsClassifier(n_neighbors=1)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Entrená el modelo con los datos X y las etiquetas y. Devolvé el modelo entrenado.
def entrenar(modelo, X, y):
    """Llamá modelo.fit(X, y) y devolvé el modelo."""
    # TU CÓDIGO ACÁ
    pass


# 3) Predecí la etiqueta de UNA fila. Devolvé un int.
def predecir(modelo, fila):
    """modelo.predict([fila])[0]  -> convertilo a int."""
    # TU CÓDIGO ACÁ
    pass


# 4) Todo junto: creá un KNN(1), entrenalo con (X, y) y predecí 'fila'. Devolvé un int.
def entrenar_y_predecir(X, y, fila):
    """Combiná los pasos anteriores."""
    # TU CÓDIGO ACÁ
    pass
