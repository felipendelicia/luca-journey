"""✅ Soluciones — ML: evaluar modelos"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score


def precision(y_real, y_pred):
    return accuracy_score(y_real, y_pred)


def evaluar(X, y):
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.5, random_state=0)
    modelo = KNeighborsClassifier(n_neighbors=1).fit(X_tr, y_tr)
    return accuracy_score(y_te, modelo.predict(X_te))


def score_modelo(modelo, X_test, y_test):
    return modelo.score(X_test, y_test)
