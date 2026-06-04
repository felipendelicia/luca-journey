"""✅ Soluciones — Proyecto: clasificador Pokédex"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def preparar(matriz):
    return matriz[:, :-1], matriz[:, -1]


def entrenar(X, y):
    return KNeighborsClassifier(n_neighbors=3).fit(X, y)


def evaluar(X, y):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
    modelo = KNeighborsClassifier(n_neighbors=3).fit(X_tr, y_tr)
    return accuracy_score(y_te, modelo.predict(X_te))


def predecir_tipo(modelo, stats):
    return int(modelo.predict([stats])[0])
