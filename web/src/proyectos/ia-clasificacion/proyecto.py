# Líder Burgh — Clasificar tipos (solución de referencia).
# El preamble (X_DATOS, Y_DATOS) está en meta.json y se antepone al corregir.

from sklearn.neighbors import KNeighborsClassifier

NOMBRES_TIPO = {0: "Fuego", 1: "Agua", 2: "Planta"}


def entrenar_clasificador(X, y):
    return KNeighborsClassifier(n_neighbors=3).fit(X, y)


def clasificar(modelo, fila):
    return int(modelo.predict([fila])[0])


def clasificar_varios(modelo, filas):
    return [int(v) for v in modelo.predict(filas)]


def tipo_nombre(X_train, y_train, stats):
    modelo = entrenar_clasificador(X_train, y_train)
    return NOMBRES_TIPO[clasificar(modelo, stats)]
