"""🧪 Tests — ML: regresión"""
import importlib.util
import os

import numpy as np
from sklearn.linear_model import LinearRegression

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iareg_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# relación lineal exacta: y = 2*x + 1
X = np.array([[1], [2], [3], [4]])
y = np.array([3, 5, 7, 9])


def test_entrenar_regresion():
    m = modulo.entrenar_regresion(X, y)
    assert isinstance(m, LinearRegression)
    assert abs(m.predict([[5]])[0] - 11) < 1e-6


def test_predecir():
    m = LinearRegression().fit(X, y)
    assert abs(modulo.predecir(m, [10]) - 21) < 1e-6
    assert isinstance(modulo.predecir(m, [10]), float)


def test_entrenar_y_predecir():
    assert abs(modulo.entrenar_y_predecir(X, y, [6]) - 13) < 1e-6
