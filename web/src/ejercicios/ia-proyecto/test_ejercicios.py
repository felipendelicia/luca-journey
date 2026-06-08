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


def _knn():
    return KNeighborsClassifier(n_neighbors=3).fit(X, y)


def test_cantidad_de_tipo():
    assert modulo.cantidad_de_tipo(y, 0) == 6


def test_ataque_promedio():
    assert modulo.ataque_promedio(X) == 65.0


def test_defensa_promedio():
    assert modulo.defensa_promedio(X) == 65.0


def test_promedio_por_tipo():
    assert np.allclose(modulo.promedio_por_tipo(X, y, 0), [532 / 6, 248 / 6])


def test_clasificar_por_regla():
    assert modulo.clasificar_por_regla([90, 40]) == 0
    assert modulo.clasificar_por_regla([40, 90]) == 1


def test_cantidad_features():
    assert modulo.cantidad_features(X) == 2


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(X) == 12


def test_entrenar_con_k():
    m = modulo.entrenar_con_k(X, y, 3)
    assert m.predict([[89, 41]]).tolist() == [0]


def test_predecir_varios():
    assert modulo.predecir_varios(_knn(), [[85, 45], [45, 85]]) == [0, 1]


def test_precision():
    assert modulo.precision(_knn(), X, y) == 1.0


def test_distancia_euclidea():
    assert modulo.distancia_euclidea([0, 0], [3, 4]) == 5.0


def test_indice_mas_parecido():
    assert modulo.indice_mas_parecido([90, 40], X) == 0


def test_contar_tipos():
    assert modulo.contar_tipos(y) == {0: 6, 1: 6}


def test_ataque_maximo():
    assert modulo.ataque_maximo(X) == 92.0


def test_indice_mas_fuerte():
    assert modulo.indice_mas_fuerte(X) == 3


def test_normalizar_min_max():
    assert np.array_equal(modulo.normalizar_min_max(np.array([[0.0, 10.0], [10.0, 20.0]])), np.array([[0.0, 0.0], [1.0, 1.0]]))
