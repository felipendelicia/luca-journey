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


def cantidad_de_tipo(y, tipo):
    return int((np.array(y) == tipo).sum())


def ataque_promedio(X):
    return float(X[:, 0].mean())


def defensa_promedio(X):
    return float(X[:, 1].mean())


def promedio_por_tipo(X, y, tipo):
    return X[np.array(y) == tipo].mean(axis=0)


def clasificar_por_regla(stats):
    return 0 if stats[0] > stats[1] else 1


def cantidad_features(X):
    return X.shape[1]


def cantidad_muestras(X):
    return X.shape[0]


def entrenar_con_k(X, y, k):
    m = KNeighborsClassifier(n_neighbors=k)
    m.fit(X, y)
    return m


def predecir_varios(modelo, filas):
    return modelo.predict(filas).tolist()


def precision(modelo, X, y):
    return modelo.score(X, y)


def distancia_euclidea(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.sqrt(((a - b) ** 2).sum()))


def indice_mas_parecido(stats, X):
    stats = np.array(stats)
    return int(np.sqrt(((X - stats) ** 2).sum(axis=1)).argmin())


def contar_tipos(y):
    v, c = np.unique(y, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def ataque_maximo(X):
    return float(X[:, 0].max())


def indice_mas_fuerte(X):
    return int(X[:, 0].argmax())


def normalizar_min_max(X):
    return (X - X.min(axis=0)) / (X.max(axis=0) - X.min(axis=0))
