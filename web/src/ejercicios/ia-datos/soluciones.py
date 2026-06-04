"""✅ Soluciones — ML: preparar los datos"""
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def separar_columnas(matriz):
    return matriz[:, :-1], matriz[:, -1]


def dividir(X, y):
    return train_test_split(X, y, test_size=0.25, random_state=42)


def escalar(X):
    return StandardScaler().fit_transform(X)


def cantidad_features(X):
    return X.shape[1]
