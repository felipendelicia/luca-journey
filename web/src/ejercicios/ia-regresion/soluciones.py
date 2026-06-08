"""✅ Soluciones — ML: regresión"""
import numpy as np
from sklearn.linear_model import LinearRegression


def entrenar_regresion(X, y):
    return LinearRegression().fit(X, y)


def predecir(modelo, fila):
    return float(modelo.predict([fila])[0])


def entrenar_y_predecir(X, y, fila):
    modelo = LinearRegression().fit(X, y)
    return float(modelo.predict([fila])[0])


def predecir_varios(modelo, filas):
    return modelo.predict(filas).tolist()


def coeficiente(modelo):
    return float(modelo.coef_[0])


def intercepto(modelo):
    return float(modelo.intercept_)


def r2(modelo, X, y):
    return modelo.score(X, y)


def error_absoluto(pred, real):
    return float(np.abs(np.array(pred) - np.array(real)).mean())


def error_cuadratico(pred, real):
    return float(((np.array(pred) - np.array(real)) ** 2).mean())


def residuos(pred, real):
    return (np.array(real) - np.array(pred)).tolist()


def predecir_con_formula(m, b, x):
    return m * x + b


def promedio(valores):
    return float(np.array(valores).mean())


def mayor_error(pred, real):
    return float(np.abs(np.array(pred) - np.array(real)).max())


def pendiente_manual(x1, y1, x2, y2):
    return (y2 - y1) / (x2 - x1)


def ordenada_manual(x, y, m):
    return y - m * x


def predecir_recta(m, b, xs):
    return [m * x + b for x in xs]


def suma_cuadrados(pred, real):
    return float(((np.array(pred) - np.array(real)) ** 2).sum())


def raiz_error_cuadratico(pred, real):
    return float(np.sqrt(((np.array(pred) - np.array(real)) ** 2).mean()))


def entrenar_y_r2(X, y):
    m = LinearRegression().fit(X, y)
    return m.score(X, y)


def cantidad_muestras(X):
    return X.shape[0]
