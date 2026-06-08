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


def _m():
    m = KNeighborsClassifier(n_neighbors=1)
    m.fit(X, y)
    return m


def test_precision():
    assert modulo.precision(_m(), X, y) == 1.0


def test_cantidad_clases():
    assert modulo.cantidad_clases(y) == 2


def test_contar_por_clase():
    assert modulo.contar_por_clase(y) == {0: 3, 1: 3}


def test_clase_mayoritaria():
    assert modulo.clase_mayoritaria(np.array([0, 0, 1])) == 0


def test_etiquetas_unicas():
    assert modulo.etiquetas_unicas(y) == [0, 1]


def test_accuracy():
    assert modulo.accuracy([1, 0, 1], [1, 1, 1]) == 2 / 3


def test_cantidad_aciertos():
    assert modulo.cantidad_aciertos([1, 0, 1], [1, 1, 1]) == 2


def test_cantidad_errores():
    assert modulo.cantidad_errores([1, 0, 1], [1, 1, 1]) == 1


def test_tasa_error():
    assert modulo.tasa_error([1, 0, 1], [1, 1, 1]) == 1 / 3


def test_todas_correctas():
    assert modulo.todas_correctas([1, 1], [1, 1]) is True
    assert modulo.todas_correctas([1, 0], [1, 1]) is False


def test_indices_incorrectos():
    assert modulo.indices_incorrectos([1, 0, 1], [1, 1, 1]) == [1]


def test_es_correcta():
    assert modulo.es_correcta([1, 0], [1, 1], 0) is True
    assert modulo.es_correcta([1, 0], [1, 1], 1) is False


def test_entrenar_con_vecinos():
    m = modulo.entrenar_con_vecinos(X, y, 1)
    assert m.predict([[88, 42]]).tolist() == [0]


def test_predecir_y_contar():
    assert modulo.predecir_y_contar(_m(), X) == {0: 3, 1: 3}


def test_mayoria_predicha():
    assert modulo.mayoria_predicha(_m(), np.array([[90, 40], [85, 45], [40, 90]])) == 0


def test_cantidad_de_clase():
    assert modulo.cantidad_de_clase(y, 0) == 3


def test_hay_clase():
    assert modulo.hay_clase(y, 1) is True
    assert modulo.hay_clase(y, 5) is False
