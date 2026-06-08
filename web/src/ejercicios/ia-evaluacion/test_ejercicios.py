"""🧪 Tests — ML: evaluar modelos"""
import importlib.util
import os

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaeval_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_precision():
    assert modulo.precision([0, 1, 1, 0], [0, 1, 0, 0]) == 0.75
    assert modulo.precision([1, 1, 1], [1, 1, 1]) == 1.0


def test_evaluar():
    # dos grupos bien separados -> el modelo acierta todo
    X = np.array([[90, 40], [88, 42], [86, 44], [40, 90], [42, 88], [44, 86]])
    y = np.array([0, 0, 0, 1, 1, 1])
    assert modulo.evaluar(X, y) == 1.0


def test_score_modelo():
    X = np.array([[90, 40], [40, 90]])
    y = np.array([0, 1])
    m = KNeighborsClassifier(n_neighbors=1).fit(X, y)
    assert modulo.score_modelo(m, X, y) == 1.0


_X = np.array([[90, 40], [88, 42], [86, 44], [40, 90], [42, 88], [44, 86]])
_y = np.array([0, 0, 0, 1, 1, 1])


def test_cantidad_correctas():
    assert modulo.cantidad_correctas([1, 0, 1], [1, 1, 1]) == 2


def test_cantidad_errores():
    assert modulo.cantidad_errores([1, 0, 1], [1, 1, 1]) == 1


def test_tasa_error():
    assert modulo.tasa_error([1, 0, 1], [1, 1, 1]) == 1 / 3


def test_verdaderos_positivos():
    assert modulo.verdaderos_positivos([1, 1, 0, 0], [1, 0, 1, 0]) == 1


def test_falsos_positivos():
    assert modulo.falsos_positivos([1, 1, 0, 0], [1, 0, 1, 0]) == 1


def test_falsos_negativos():
    assert modulo.falsos_negativos([1, 1, 0, 0], [1, 0, 1, 0]) == 1


def test_verdaderos_negativos():
    assert modulo.verdaderos_negativos([1, 1, 0, 0], [1, 0, 1, 0]) == 1


def test_precision_clase1():
    assert modulo.precision_clase1([1, 1, 0, 0], [1, 0, 1, 0]) == 0.5


def test_recall_clase1():
    assert modulo.recall_clase1([1, 1, 0, 0], [1, 0, 1, 0]) == 0.5


def test_es_perfecto():
    assert modulo.es_perfecto([1, 0], [1, 0]) is True
    assert modulo.es_perfecto([1, 0], [1, 1]) is False


def test_cantidad_test():
    assert modulo.cantidad_test(10, 0.2) == 2


def test_cantidad_train():
    assert modulo.cantidad_train(10, 0.2) == 8


def test_promedio():
    assert modulo.promedio([2, 4, 6]) == 4.0


def test_entrenar_knn():
    m = modulo.entrenar_knn(_X, _y, 1)
    assert m.predict([[88, 42]]).tolist() == [0]


def test_dividir_datos():
    partes = modulo.dividir_datos(_X, _y, 0.5, 0)
    assert len(partes) == 4


def test_evaluar_split():
    r = modulo.evaluar_split(_X, _y, 0)
    assert 0.0 <= r <= 1.0


def test_cantidad_clases():
    assert modulo.cantidad_clases(_y) == 2
