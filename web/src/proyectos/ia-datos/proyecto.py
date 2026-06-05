# Líder Lenora — Preparar los datos (solución de referencia).
# El preamble (DATASET) está en meta.json y se antepone al corregir.

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def separar_columnas(matriz):
    X = matriz[:, :-1]
    y = matriz[:, -1]
    return X, y


def dividir(X, y):
    return train_test_split(X, y, test_size=0.25, random_state=42)


def escalar(X):
    return StandardScaler().fit_transform(X)


def preparar_datos(dataset):
    X, y = separar_columnas(dataset)
    X_train, X_test, y_train, y_test = dividir(X, y)
    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)
    return X_train, X_test, y_train, y_test
