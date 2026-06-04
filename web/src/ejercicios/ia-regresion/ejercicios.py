"""
✏️ Ejercicios — ML: regresión

Clasificar predice una categoría; la REGRESIÓN predice un NÚMERO
(ej: el CP de un Pokémon a partir de su nivel). Usamos LinearRegression.
"""
import numpy as np
from sklearn.linear_model import LinearRegression


# 1) Entrená un modelo de regresión lineal con X e y. Devolvé el modelo.
def entrenar_regresion(X, y):
    """LinearRegression().fit(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# 2) Predecí el número para una fila. Devolvé un float.
def predecir(modelo, fila):
    """float(modelo.predict([fila])[0])."""
    # TU CÓDIGO ACÁ
    pass


# 3) Todo junto: entrená con (X, y) y predecí 'fila'. Devolvé un float.
def entrenar_y_predecir(X, y, fila):
    """Combiná los pasos."""
    # TU CÓDIGO ACÁ
    pass
