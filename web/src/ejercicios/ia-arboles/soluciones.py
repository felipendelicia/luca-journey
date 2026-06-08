"""✅ Soluciones — ML: árboles de decisión"""
import numpy as np
from sklearn.tree import DecisionTreeClassifier


def entrenar_arbol(X, y):
    return DecisionTreeClassifier(random_state=0).fit(X, y)


def clasificar(modelo, fila):
    return int(modelo.predict([fila])[0])


def importancias(modelo):
    return list(modelo.feature_importances_)


def precision(modelo, X, y):
    return modelo.score(X, y)


def profundidad(modelo):
    return modelo.get_depth()


def cantidad_hojas(modelo):
    return modelo.get_n_leaves()


def importancias_lista(modelo):
    return modelo.feature_importances_.tolist()


def feature_mas_importante(modelo):
    return int(np.argmax(modelo.feature_importances_))


def entrenar_con_profundidad(X, y, prof):
    m = DecisionTreeClassifier(max_depth=prof, random_state=0)
    m.fit(X, y)
    return m


def clasificar_varios(modelo, filas):
    return modelo.predict(filas).tolist()


def cantidad_clases(y):
    return len(np.unique(y))


def contar_por_clase(y):
    v, c = np.unique(y, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def clase_mayoritaria(y):
    v, c = np.unique(y, return_counts=True)
    return int(v[c.argmax()])


def accuracy(pred, real):
    return float((np.array(pred) == np.array(real)).mean())


def cantidad_aciertos(pred, real):
    return int((np.array(pred) == np.array(real)).sum())


def etiquetas_unicas(y):
    return np.unique(y).tolist()


def cantidad_features(X):
    return X.shape[1]


def cantidad_muestras(X):
    return X.shape[0]


def predecir_y_contar(modelo, X):
    pred = modelo.predict(X)
    v, c = np.unique(pred, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def hay_clase(y, clase):
    return bool((np.array(y) == clase).any())
