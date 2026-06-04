"""✅ Soluciones — ML: tu primer modelo"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def crear_modelo():
    return KNeighborsClassifier(n_neighbors=1)


def entrenar(modelo, X, y):
    modelo.fit(X, y)
    return modelo


def predecir(modelo, fila):
    return int(modelo.predict([fila])[0])


def entrenar_y_predecir(X, y, fila):
    modelo = KNeighborsClassifier(n_neighbors=1)
    modelo.fit(X, y)
    return int(modelo.predict([fila])[0])
