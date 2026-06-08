"""🧪 Tests — ML: preparar los datos"""
import importlib.util
import os

import numpy as np

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"iadatos_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_separar_columnas():
    m = np.array([[90, 40, 0], [40, 90, 1]])
    X, y = modulo.separar_columnas(m)
    assert np.array_equal(X, np.array([[90, 40], [40, 90]]))
    assert np.array_equal(y, np.array([0, 1]))


def test_dividir():
    X = np.arange(16).reshape(8, 2)
    y = np.array([0, 1, 0, 1, 0, 1, 0, 1])
    X_tr, X_te, y_tr, y_te = modulo.dividir(X, y)
    assert len(X_tr) == 6 and len(X_te) == 2
    assert len(y_tr) == 6 and len(y_te) == 2


def test_escalar():
    X = np.array([[0.0, 10.0], [10.0, 20.0], [20.0, 30.0]])
    r = modulo.escalar(X)
    assert np.allclose(r.mean(axis=0), 0, atol=1e-9)
    assert np.allclose(r.std(axis=0), 1, atol=1e-9)


def test_cantidad_features():
    assert modulo.cantidad_features(np.zeros((5, 3))) == 3


def test_cantidad_muestras():
    assert modulo.cantidad_muestras(np.arange(16).reshape(8, 2)) == 8


def test_promedio_features():
    assert np.array_equal(modulo.promedio_features(np.array([[2, 4], [10, 20]])), np.array([6.0, 12.0]))


def test_desviacion_features():
    assert np.array_equal(modulo.desviacion_features(np.array([[0, 0], [2, 2]])), np.array([1.0, 1.0]))


def test_minimo_features():
    assert np.array_equal(modulo.minimo_features(np.array([[1, 5], [3, 2]])), np.array([1, 2]))


def test_maximo_features():
    assert np.array_equal(modulo.maximo_features(np.array([[1, 5], [3, 2]])), np.array([3, 5]))


def test_normalizar_min_max():
    assert np.array_equal(modulo.normalizar_min_max(np.array([[0.0, 10.0], [10.0, 20.0]])), np.array([[0.0, 0.0], [1.0, 1.0]]))


def test_agregar_columna():
    assert np.array_equal(modulo.agregar_columna(np.array([[1], [2]]), np.array([3, 4])), np.array([[1, 3], [2, 4]]))


def test_quitar_columna():
    assert np.array_equal(modulo.quitar_columna(np.array([[1, 2, 3], [4, 5, 6]]), 1), np.array([[1, 3], [4, 6]]))


def test_primera_columna():
    assert np.array_equal(modulo.primera_columna(np.array([[1, 2], [3, 4]])), np.array([1, 3]))


def test_etiquetas():
    assert np.array_equal(modulo.etiquetas(np.array([[1, 2, 0], [3, 4, 1]])), np.array([0, 1]))


def test_features():
    assert np.array_equal(modulo.features(np.array([[1, 2, 0], [3, 4, 1]])), np.array([[1, 2], [3, 4]]))


def test_balanceado():
    assert modulo.balanceado(np.array([0, 0, 1, 1])) is True
    assert modulo.balanceado(np.array([0, 0, 0, 1])) is False


def test_dividir_manual():
    a, b = modulo.dividir_manual(np.arange(8).reshape(4, 2), 0.5)
    assert np.array_equal(a, np.array([[0, 1], [2, 3]]))
    assert np.array_equal(b, np.array([[4, 5], [6, 7]]))


def test_contar_clases():
    assert modulo.contar_clases(np.array([0, 0, 1])) == {0: 2, 1: 1}


def test_proporcion_clase():
    assert modulo.proporcion_clase(np.array([0, 0, 1, 1]), 1) == 0.5


def test_mezclar_indices():
    r = modulo.mezclar_indices(5, 42)
    assert sorted(r) == [0, 1, 2, 3, 4]
    assert modulo.mezclar_indices(5, 42) == r, "Con la misma seed tiene que dar lo mismo"
