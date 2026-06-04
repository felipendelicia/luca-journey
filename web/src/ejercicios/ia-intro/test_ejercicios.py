"""🧪 Tests — ML: tu primer modelo"""
import importlib.util
import os

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaintro_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# stats [ataque, defensa] -> tipo: 0 = Fuego (mucho ataque), 1 = Agua (mucha defensa)
X = np.array([[90, 40], [85, 45], [40, 90], [45, 85]])
y = np.array([0, 0, 1, 1])


def test_crear_modelo():
    m = modulo.crear_modelo()
    assert isinstance(m, KNeighborsClassifier)
    assert m.n_neighbors == 1


def test_entrenar():
    m = modulo.entrenar(modulo.crear_modelo(), X, y)
    assert m.predict([[88, 42]])[0] == 0


def test_predecir():
    m = KNeighborsClassifier(n_neighbors=1).fit(X, y)
    assert modulo.predecir(m, [88, 42]) == 0
    assert modulo.predecir(m, [42, 88]) == 1
    assert isinstance(modulo.predecir(m, [88, 42]), int)


def test_entrenar_y_predecir():
    assert modulo.entrenar_y_predecir(X, y, [95, 35]) == 0
    assert modulo.entrenar_y_predecir(X, y, [35, 95]) == 1
