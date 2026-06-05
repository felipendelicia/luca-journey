# Líder Elesa — Evaluar un modelo (solución de referencia).
# El preamble (X_EVAL, Y_EVAL) está en meta.json y se antepone al corregir.

from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier


def calcular_precision(y_real, y_pred):
    return accuracy_score(y_real, y_pred)


def dividir_y_evaluar(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=0)
    modelo = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
    return accuracy_score(y_test, modelo.predict(X_test))


def score_modelo(modelo, X_test, y_test):
    return modelo.score(X_test, y_test)


def evaluar_completo(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)
    modelo = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    return {
        "precision": accuracy_score(y_test, y_pred),
        "n_test": int(len(y_test)),
    }
