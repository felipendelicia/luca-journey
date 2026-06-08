"""✏️ Ejercicios — ML: regresión

Clasificar predice una categoría; la REGRESIÓN predice un NÚMERO (ej: el CP de un
Pokémon a partir de su nivel). Usamos LinearRegression. ✅ Corregir al terminar.
"""
import numpy as np
from sklearn.linear_model import LinearRegression


# Entrenar la regresión
# Entrená un modelo de regresión lineal con X e y, y devolvé el modelo.
# Pista: LinearRegression().fit(X, y).
def entrenar_regresion(X, y):
    """Devolvé una LinearRegression entrenada."""
    # TU CÓDIGO ACÁ
    pass


# Predecir un número
# Predecí el número para una fila y devolvé un float. Pista: float(modelo.predict([fila])[0]).
# Ejemplo:  con la relación y = 2x + 1  →  predecir(modelo, [10])  →  21.0
def predecir(modelo, fila):
    """Devolvé la predicción de 'fila' como float."""
    # TU CÓDIGO ACÁ
    pass


# Todo junto
# Entrená con (X, y) y predecí 'fila'. Devolvé un float.
def entrenar_y_predecir(X, y, fila):
    """Combiná entrenar + predecir."""
    # TU CÓDIGO ACÁ
    pass


# Predecir varios
# Devolvé las predicciones del modelo para una lista de filas, como lista.
def predecir_varios(modelo, filas):
    """Devolvé las predicciones para varias filas, como lista."""
    # TU CÓDIGO ACÁ
    pass


# Coeficiente (pendiente)
# Devolvé el coeficiente (la pendiente) del modelo, como float. Pista: modelo.coef_[0].
def coeficiente(modelo):
    """Devolvé la pendiente del modelo."""
    # TU CÓDIGO ACÁ
    pass


# Intercepto
# Devolvé el intercepto (la ordenada al origen) del modelo, como float. Pista: modelo.intercept_.
def intercepto(modelo):
    """Devolvé el intercepto del modelo."""
    # TU CÓDIGO ACÁ
    pass


# R²
# Devolvé el R² del modelo sobre (X, y). Pista: modelo.score(X, y).
def r2(modelo, X, y):
    """Devolvé modelo.score(X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Error absoluto medio
# Devolvé el promedio del valor absoluto de (predicho - real).
def error_absoluto(pred, real):
    """Devolvé el error absoluto medio."""
    # TU CÓDIGO ACÁ
    pass


# Error cuadrático medio
# Devolvé el promedio de (predicho - real) al cuadrado.
def error_cuadratico(pred, real):
    """Devolvé el error cuadrático medio."""
    # TU CÓDIGO ACÁ
    pass


# Residuos
# Devolvé (real - predicho) para cada valor, como lista.
def residuos(pred, real):
    """Devolvé los residuos (real - predicho)."""
    # TU CÓDIGO ACÁ
    pass


# Predecir con la fórmula
# Dada la pendiente `m`, el intercepto `b` y un valor `x`, devolvé m*x + b.
def predecir_con_formula(m, b, x):
    """Devolvé m*x + b."""
    # TU CÓDIGO ACÁ
    pass


# Promedio
# Devolvé el promedio de una lista de valores, como float.
def promedio(valores):
    """Devolvé el promedio."""
    # TU CÓDIGO ACÁ
    pass


# El mayor error
# Devolvé el mayor valor absoluto de (predicho - real).
def mayor_error(pred, real):
    """Devolvé el mayor error absoluto."""
    # TU CÓDIGO ACÁ
    pass


# Pendiente entre dos puntos
# Dados dos puntos (x1, y1) y (x2, y2), devolvé la pendiente: (y2 - y1) / (x2 - x1).
def pendiente_manual(x1, y1, x2, y2):
    """Devolvé la pendiente entre dos puntos."""
    # TU CÓDIGO ACÁ
    pass


# Ordenada al origen
# Dado un punto (x, y) y la pendiente `m`, devolvé el intercepto: y - m*x.
def ordenada_manual(x, y, m):
    """Devolvé y - m*x."""
    # TU CÓDIGO ACÁ
    pass


# Predecir una recta
# Dada la pendiente `m`, el intercepto `b` y una lista `xs`, devolvé [m*x + b para cada x].
def predecir_recta(m, b, xs):
    """Devolvé la recta evaluada en cada x."""
    # TU CÓDIGO ACÁ
    pass


# Suma de cuadrados
# Devolvé la suma de (predicho - real) al cuadrado.
def suma_cuadrados(pred, real):
    """Devolvé la suma de los errores al cuadrado."""
    # TU CÓDIGO ACÁ
    pass


# Raíz del error cuadrático (RMSE)
# Devolvé la raíz cuadrada del error cuadrático medio.
def raiz_error_cuadratico(pred, real):
    """Devolvé el RMSE."""
    # TU CÓDIGO ACÁ
    pass


# Entrenar y devolver R²
# Entrená una LinearRegression con (X, y) y devolvé su R² sobre los mismos datos.
def entrenar_y_r2(X, y):
    """Devolvé el R² de un modelo entrenado con (X, y)."""
    # TU CÓDIGO ACÁ
    pass


# Cantidad de muestras
# Devolvé cuántas filas tiene X.
def cantidad_muestras(X):
    """Devolvé la cantidad de filas de X."""
    # TU CÓDIGO ACÁ
    pass
