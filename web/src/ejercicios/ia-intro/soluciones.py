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


def predecir_varios(modelo, filas):
    return modelo.predict(filas).tolist()


def cantidad_clases(y):
    return len(np.unique(y))


def precision(modelo, X, y):
    return modelo.score(X, y)


def contar_por_clase(y):
    valores, cuentas = np.unique(y, return_counts=True)
    return {int(v): int(c) for v, c in zip(valores, cuentas)}


def clase_mayoritaria(y):
    valores, cuentas = np.unique(y, return_counts=True)
    return int(valores[cuentas.argmax()])


def accuracy_manual(pred, real):
    pred = np.array(pred)
    real = np.array(real)
    return float((pred == real).mean())


def etiquetas_unicas(y):
    return np.unique(y).tolist()


def promedio_por_columna(X):
    return X.mean(axis=0)


def escalar_0_1(X):
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))


def cantidad_features(X):
    return X.shape[1]


def cantidad_muestras(X):
    return X.shape[0]


def distancia_euclidea(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.sqrt(((a - b) ** 2).sum()))


def indice_mas_cercano(punto, puntos):
    punto = np.array(punto)
    puntos = np.array(puntos)
    dists = np.sqrt(((puntos - punto) ** 2).sum(axis=1))
    return int(dists.argmin())


def cantidad_correctas(pred, real):
    pred = np.array(pred)
    real = np.array(real)
    return int((pred == real).sum())


def matriz_a_lista(X):
    return X.tolist()


def entrenar_con_k(X, y, k):
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X, y)
    return m
