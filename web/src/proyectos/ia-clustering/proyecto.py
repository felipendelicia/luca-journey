# Líder Brycen — Clustering (solución de referencia).
# El preamble (X_CLUSTER) está en meta.json y se antepone al corregir.

from sklearn.cluster import KMeans


def agrupar(X, k):
    return KMeans(n_clusters=k, random_state=0, n_init=10).fit(X)


def etiquetas(modelo):
    return [int(e) for e in modelo.labels_]


def a_que_grupo(modelo, fila):
    return int(modelo.predict([fila])[0])


def resumen_clusters(X, k):
    modelo = agrupar(X, k)
    labs = etiquetas(modelo)
    return {g: labs.count(g) for g in range(k)}
