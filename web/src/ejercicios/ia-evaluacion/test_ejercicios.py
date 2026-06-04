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
