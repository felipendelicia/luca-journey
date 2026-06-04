"""✅ Soluciones — ML: árboles de decisión"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


def entrenar_arbol(X, y):
    return DecisionTreeClassifier(random_state=0).fit(X, y)


def clasificar(modelo, fila):
    return int(modelo.predict([fila])[0])


def importancias(modelo):
    return list(modelo.feature_importances_)
