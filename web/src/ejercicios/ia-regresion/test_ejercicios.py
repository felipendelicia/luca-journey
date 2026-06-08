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


def _m():
    return LinearRegression().fit(X, y)


def test_predecir_varios():
    assert np.allclose(modulo.predecir_varios(_m(), [[5], [6]]), [11.0, 13.0])


def test_coeficiente():
    assert round(modulo.coeficiente(_m()), 5) == 2.0


def test_intercepto():
    assert round(modulo.intercepto(_m()), 5) == 1.0


def test_r2():
    assert round(modulo.r2(_m(), X, y), 5) == 1.0


def test_error_absoluto():
    assert modulo.error_absoluto([1, 2, 3], [1, 2, 5]) == 2 / 3


def test_error_cuadratico():
    assert modulo.error_cuadratico([1, 2, 3], [1, 2, 5]) == 4 / 3


def test_residuos():
    assert modulo.residuos([1, 2], [3, 5]) == [2, 3]


def test_predecir_con_formula():
    assert modulo.predecir_con_formula(2, 1, 5) == 11


def test_promedio():
    assert modulo.promedio([2, 4, 6]) == 4.0


def test_mayor_error():
    assert modulo.mayor_error([1, 2, 3], [1, 2, 6]) == 3.0


def test_pendiente_manual():
    assert modulo.pendiente_manual(1, 3, 2, 5) == 2.0


def test_ordenada_manual():
    assert modulo.ordenada_manual(1, 3, 2) == 1


def test_predecir_recta():
    assert modulo.predecir_recta(2, 1, [1, 2, 3]) == [3, 5, 7]


def test_suma_cuadrados():
    assert modulo.suma_cuadrados([1, 2], [1, 4]) == 4.0


def test_raiz_error_cuadratico():
    assert round(modulo.raiz_error_cuadratico([1, 2, 3], [1, 2, 5]), 4) == round((4 / 3) ** 0.5, 4)


def test_entrenar_y_r2():
    assert round(modulo.entrenar_y_r2(X, y), 5) == 1.0


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(X) == 4
