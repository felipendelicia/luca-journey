"""✅ Soluciones — ML: regresión"""
import numpy as np
from sklearn.linear_model import LinearRegression


def entrenar_regresion(X, y):
    return LinearRegression().fit(X, y)


def predecir(modelo, fila):
    return float(modelo.predict([fila])[0])


def entrenar_y_predecir(X, y, fila):
    modelo = LinearRegression().fit(X, y)
    return float(modelo.predict([fila])[0])
