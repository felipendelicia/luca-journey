"""✅ Soluciones — ML: clasificación"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def entrenar_clasificador(X, y):
    return KNeighborsClassifier(n_neighbors=3).fit(X, y)


def clasificar(modelo, fila):
    return int(modelo.predict([fila])[0])


def clasificar_varios(modelo, filas):
    return [int(v) for v in modelo.predict(filas)]
