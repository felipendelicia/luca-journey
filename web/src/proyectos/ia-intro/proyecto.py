# Líder Cilan — Tu primer modelo (solución de referencia).
# El preamble (X_TRAIN, Y_TRAIN) está en meta.json y se antepone al corregir.

from sklearn.neighbors import KNeighborsClassifier


def crear_modelo():
    return KNeighborsClassifier(n_neighbors=1)


def entrenar(modelo, X, y):
    modelo.fit(X, y)
    return modelo


def predecir(modelo, fila):
    return int(modelo.predict([fila])[0])


def clasificador_completo(X_train, y_train, nuevos):
    modelo = crear_modelo()
    modelo = entrenar(modelo, X_train, y_train)
    return [predecir(modelo, fila) for fila in nuevos]
