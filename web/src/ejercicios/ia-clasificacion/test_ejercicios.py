"""🧪 Tests — ML: clasificación"""
import importlib.util
import os

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaclas_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# 0 = Fuego (mucho ataque), 1 = Agua (mucha defensa)
X = np.array([[90, 40], [85, 45], [88, 42], [40, 90], [45, 85], [42, 88]])
y = np.array([0, 0, 0, 1, 1, 1])


def test_entrenar_clasificador():
    m = modulo.entrenar_clasificador(X, y)
    assert isinstance(m, KNeighborsClassifier)
    assert m.predict([[87, 43]])[0] == 0


def test_clasificar():
    m = KNeighborsClassifier(n_neighbors=3).fit(X, y)
    assert modulo.clasificar(m, [89, 41]) == 0
    assert modulo.clasificar(m, [41, 89]) == 1
    assert isinstance(modulo.clasificar(m, [89, 41]), int)


def test_clasificar_varios():
    m = KNeighborsClassifier(n_neighbors=3).fit(X, y)
    r = modulo.clasificar_varios(m, [[89, 41], [41, 89]])
    assert r == [0, 1]
    assert all(isinstance(v, int) for v in r)
