"""✅ Soluciones — ML: clustering (no supervisado)"""
import numpy as np
from sklearn.cluster import KMeans


def agrupar(X, k):
    return KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)


def etiquetas(modelo):
    return [int(e) for e in modelo.labels_]


def a_que_grupo(modelo, fila):
    return int(modelo.predict([fila])[0])
