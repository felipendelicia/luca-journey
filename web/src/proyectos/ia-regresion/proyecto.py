# Líder Clay — Predecir números (solución de referencia).
# El preamble (NIVELES, CP_REAL) está en meta.json y se antepone al corregir.

from sklearn.linear_model import LinearRegression


def entrenar_regresion(X, y):
    return LinearRegression().fit(X, y)


def predecir_cp(modelo, fila):
    return float(modelo.predict([fila])[0])


def coeficientes(modelo):
    return float(modelo.coef_[0]), float(modelo.intercept_)


def cp_varios(niveles_lista):
    modelo = entrenar_regresion(NIVELES, CP_REAL)
    return [round(predecir_cp(modelo, [n]), 1) for n in niveles_lista]
