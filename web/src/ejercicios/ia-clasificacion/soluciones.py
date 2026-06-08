"""✅ Soluciones — ML: clasificación"""
import numpy as np
from sklearn.neighbors import KNeighborsClassifier


def entrenar_clasificador(X, y):
    return KNeighborsClassifier(n_neighbors=3).fit(X, y)


def clasificar(modelo, fila):
    return int(modelo.predict([fila])[0])


def clasificar_varios(modelo, filas):
    return [int(v) for v in modelo.predict(filas)]


def precision(modelo, X, y):
    return modelo.score(X, y)


def cantidad_clases(y):
    return len(np.unique(y))


def contar_por_clase(y):
    v, c = np.unique(y, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def clase_mayoritaria(y):
    v, c = np.unique(y, return_counts=True)
    return int(v[c.argmax()])


def etiquetas_unicas(y):
    return np.unique(y).tolist()


def accuracy(pred, real):
    return float((np.array(pred) == np.array(real)).mean())


def cantidad_aciertos(pred, real):
    return int((np.array(pred) == np.array(real)).sum())


def cantidad_errores(pred, real):
    return int((np.array(pred) != np.array(real)).sum())


def tasa_error(pred, real):
    return float((np.array(pred) != np.array(real)).mean())


def todas_correctas(pred, real):
    return bool((np.array(pred) == np.array(real)).all())


def indices_incorrectos(pred, real):
    return np.where(np.array(pred) != np.array(real))[0].tolist()


def es_correcta(pred, real, i):
    return bool(np.array(pred)[i] == np.array(real)[i])


def entrenar_con_vecinos(X, y, k):
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X, y)
    return m


def predecir_y_contar(modelo, X):
    pred = modelo.predict(X)
    v, c = np.unique(pred, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def mayoria_predicha(modelo, X):
    pred = modelo.predict(X)
    v, c = np.unique(pred, return_counts=True)
    return int(v[c.argmax()])


def cantidad_de_clase(y, clase):
    return int((np.array(y) == clase).sum())


def hay_clase(y, clase):
    return bool((np.array(y) == clase).any())
