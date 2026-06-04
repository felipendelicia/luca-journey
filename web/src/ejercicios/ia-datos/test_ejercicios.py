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
