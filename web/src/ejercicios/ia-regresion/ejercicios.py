"""✏️ Ejercicios — ML: regresión

Clasificar predice una categoría; la REGRESIÓN predice un NÚMERO (ej: el CP de un
Pokémon a partir de su nivel). Usamos LinearRegression. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.linear_model import LinearRegression


# Entrenar la regresión
# Entrená un modelo de regresión lineal con X e y, y devolvé el modelo.
# Pista: LinearRegression().fit(X, y).
def entrenar_regresion(X, y):
    """Devolvé una LinearRegression entrenada."""
    # TU CÓDIGO ACÁ
    pass


# Predecir un número
# Predecí el número para una fila y devolvé un float. Pista: float(modelo.predict([fila])[0]).
# Ejemplo:  con la relación y = 2x + 1  →  predecir(modelo, [10])  →  21.0
def predecir(modelo, fila):
    """Devolvé la predicción de 'fila' como float."""
    # TU CÓDIGO ACÁ
    pass


# Todo junto
# Entrená con (X, y) y predecí 'fila'. Devolvé un float.
def entrenar_y_predecir(X, y, fila):
    """Combiná entrenar + predecir."""
    # TU CÓDIGO ACÁ
    pass
