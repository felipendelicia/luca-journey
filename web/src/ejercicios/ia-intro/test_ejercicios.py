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


def _modelo():
    m = KNeighborsClassifier(n_neighbors=1)
    m.fit(X, y)
    return m


def test_predecir_varios():
    assert modulo.predecir_varios(_modelo(), [[88, 42], [42, 88]]) == [0, 1]


def test_cantidad_clases():
    assert modulo.cantidad_clases(y) == 2


def test_precision():
    assert modulo.precision(_modelo(), X, y) == 1.0


def test_contar_por_clase():
    assert modulo.contar_por_clase(np.array([0, 0, 1])) == {0: 2, 1: 1}


def test_clase_mayoritaria():
    assert modulo.clase_mayoritaria(np.array([0, 0, 1])) == 0


def test_accuracy_manual():
    assert modulo.accuracy_manual([1, 0, 1], [1, 1, 1]) == 2 / 3


def test_etiquetas_unicas():
    assert modulo.etiquetas_unicas(np.array([1, 0, 1, 0])) == [0, 1]


def test_promedio_por_columna():
    assert np.array_equal(modulo.promedio_por_columna(np.array([[2, 4], [10, 20]])), np.array([6.0, 12.0]))


def test_escalar_0_1():
    assert np.array_equal(modulo.escalar_0_1(np.array([[0, 10], [10, 20]])), np.array([[0.0, 0.0], [1.0, 1.0]]))


def test_cantidad_features():
    assert modulo.cantidad_features(X) == 2


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(X) == 4


def test_distancia_euclidea():
    assert modulo.distancia_euclidea([0, 0], [3, 4]) == 5.0


def test_indice_mas_cercano():
    assert modulo.indice_mas_cercano([0, 0], [[10, 10], [1, 1]]) == 1


def test_cantidad_correctas():
    assert modulo.cantidad_correctas([1, 0, 1], [1, 1, 1]) == 2


def test_matriz_a_lista():
    assert modulo.matriz_a_lista(np.array([[1, 2], [3, 4]])) == [[1, 2], [3, 4]]


def test_entrenar_con_k():
    m = modulo.entrenar_con_k(X, y, 1)
    assert m.predict([[88, 42]]).tolist() == [0]
