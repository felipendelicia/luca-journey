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


def cantidad_muestras(X):
    return X.shape[0]


def promedio_features(X):
    return X.mean(axis=0)


def desviacion_features(X):
    return X.std(axis=0)


def minimo_features(X):
    return X.min(axis=0)


def maximo_features(X):
    return X.max(axis=0)


def normalizar_min_max(X):
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))


def agregar_columna(X, col):
    return np.column_stack([X, col])


def quitar_columna(X, i):
    return np.delete(X, i, axis=1)


def primera_columna(X):
    return X[:, 0]


def etiquetas(matriz):
    return matriz[:, -1]


def features(matriz):
    return matriz[:, :-1]


def balanceado(y):
    _, cuentas = np.unique(y, return_counts=True)
    return bool(len(set(cuentas.tolist())) == 1)


def dividir_manual(X, frac):
    k = int(len(X) * frac)
    return X[:k], X[k:]


def contar_clases(y):
    valores, cuentas = np.unique(y, return_counts=True)
    return {int(v): int(c) for v, c in zip(valores, cuentas)}


def proporcion_clase(y, clase):
    return float((np.array(y) == clase).mean())


def mezclar_indices(n, seed):
    return np.random.RandomState(seed).permutation(n).tolist()
