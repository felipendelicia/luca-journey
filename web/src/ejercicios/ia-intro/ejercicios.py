"""✏️ Ejercicios — ML: tu primer modelo

Machine Learning = enseñarle a un modelo con EJEMPLOS para que después prediga solo.
Le das X (datos) e y (respuestas), hace .fit() y después .predict(). Usamos un
clasificador de vecinos (KNN). ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


# Crear el modelo (KNN)
# Devolvé un clasificador KNN que mire al vecino más cercano. Pista: KNeighborsClassifier(n_neighbors=1).
def crear_modelo():
    """Devolvé un KNeighborsClassifier(n_neighbors=1)."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar (fit)
# Entrená el modelo con los datos X y las etiquetas y, y devolvé el modelo entrenado.
# Pista: modelo.fit(X, y); return modelo.
def entrenar(modelo, X, y):
    """Entrená el modelo y devolvelo."""
    # TU CÓDIGO ACÁ
    pass


# Predecir (predict)
# Predecí la etiqueta de UNA fila y devolvé un int. Pista: int(modelo.predict([fila])[0]).
# Ejemplo:  para stats de Fuego  →  predecir(modelo, [88, 42])  →  0
def predecir(modelo, fila):
    """Devolvé la predicción de 'fila' como int."""
    # TU CÓDIGO ACÁ
    pass


# Todo junto
# Creá un KNN(1), entrenalo con (X, y) y predecí 'fila'. Devolvé un int.
def entrenar_y_predecir(X, y, fila):
    """Combiná crear + entrenar + predecir."""
    # TU CÓDIGO ACÁ
    pass
