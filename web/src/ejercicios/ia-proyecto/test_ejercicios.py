"""🧪 Tests — Proyecto: clasificador Pokédex"""
import importlib.util
import os

import numpy as np
from sklearn.neighbors import KNeighborsClassifier

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iaproy_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

# stats [ataque, defensa] + tipo (0 Fuego / 1 Agua) en la última columna
DATOS = np.array([
    [90, 40, 0], [88, 42, 0], [86, 44, 0], [92, 38, 0], [89, 41, 0], [87, 43, 0],
    [40, 90, 1], [42, 88, 1], [44, 86, 1], [38, 92, 1], [41, 89, 1], [43, 87, 1],
])
X = DATOS[:, :-1]
y = DATOS[:, -1]


def test_preparar():
    Xs, ys = modulo.preparar(DATOS)
    assert Xs.shape == (12, 2)
    assert list(ys) == [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]


def test_entrenar():
    m = modulo.entrenar(X, y)
    assert isinstance(m, KNeighborsClassifier)
    assert m.predict([[89, 41]])[0] == 0


def test_evaluar():
    # datos bien separados -> el modelo debería acertar (casi) todo
    assert modulo.evaluar(X, y) >= 0.8


def test_predecir_tipo():
    m = KNeighborsClassifier(n_neighbors=3).fit(X, y)
    assert modulo.predecir_tipo(m, [85, 45]) == 0
    assert modulo.predecir_tipo(m, [45, 85]) == 1
    assert isinstance(modulo.predecir_tipo(m, [85, 45]), int)
