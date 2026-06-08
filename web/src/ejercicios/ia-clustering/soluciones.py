"""✅ Soluciones — ML: clustering (no supervisado)"""
import numpy as np
from sklearn.cluster import KMeans


def agrupar(X, k):
    return KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)


def etiquetas(modelo):
    return [int(e) for e in modelo.labels_]


def a_que_grupo(modelo, fila):
    return int(modelo.predict([fila])[0])


def cantidad_grupos(modelo):
    return modelo.n_clusters


def a_que_grupos(modelo, filas):
    return modelo.predict(filas).tolist()


def tamano_grupos(modelo):
    v, c = np.unique(modelo.labels_, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def mismo_grupo(modelo, fila1, fila2):
    pred = modelo.predict([fila1, fila2])
    return bool(pred[0] == pred[1])


def agrupar_con_k(X, k):
    m = KMeans(n_clusters=k, random_state=0, n_init=10)
    m.fit(X)
    return m


def distancia_euclidea(a, b):
    a = np.array(a)
    b = np.array(b)
    return float(np.sqrt(((a - b) ** 2).sum()))


def indice_mas_cercano(punto, puntos):
    punto = np.array(punto)
    puntos = np.array(puntos)
    return int(np.sqrt(((puntos - punto) ** 2).sum(axis=1)).argmin())


def cantidad_por_etiqueta(etiquetas):
    v, c = np.unique(etiquetas, return_counts=True)
    return {int(a): int(b) for a, b in zip(v, c)}


def grupos_distintos(etiquetas):
    return np.unique(etiquetas).tolist()


def grupo_mayoritario(etiquetas):
    v, c = np.unique(etiquetas, return_counts=True)
    return int(v[c.argmax()])


def cantidad_puntos_en(etiquetas, grupo):
    return int((np.array(etiquetas) == grupo).sum())


def promedio_de_grupo(X, etiquetas, grupo):
    return X[np.array(etiquetas) == grupo].mean(axis=0)


def cantidad_muestras(X):
    return X.shape[0]


def cantidad_features(X):
    return X.shape[1]


def centro_mas_cercano(modelo, punto):
    return int(modelo.predict([punto])[0])


def cantidad_grupos_usados(etiquetas):
    return len(np.unique(etiquetas))


def inercia_positiva(modelo):
    return bool(modelo.inertia_ > 0)
