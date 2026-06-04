"""🧪 Tests — NumPy: Cálculo numérico"""
import importlib.util
import os

import numpy as np

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"numpycalc_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_total_stats():
    assert modulo.total_stats(np.array([10, 20, 30])) == 60


def test_promedio():
    assert np.isclose(modulo.promedio(np.array([10, 20, 30])), 20.0)


def test_mas_fuerte():
    assert modulo.mas_fuerte(np.array([3, 99, 50])) == 99


def test_desviacion():
    assert np.isclose(modulo.desviacion(np.array([2, 4, 6])), np.std([2, 4, 6]))


def test_suma_por_columna():
    assert np.array_equal(modulo.suma_por_columna(np.array([[1, 2], [3, 4]])), np.array([4, 6]))


def test_suma_por_fila():
    assert np.array_equal(modulo.suma_por_fila(np.array([[1, 2], [3, 4]])), np.array([3, 7]))


def test_contar_mayores():
    r = modulo.contar_mayores(np.array([10, 50, 30, 80, 5]), 40)
    assert r == 2
    assert isinstance(r, int)


def test_normalizar():
    r = modulo.normalizar(np.array([0.0, 5.0, 10.0]))
    assert np.allclose(r, np.array([0.0, 0.5, 1.0]))


def test_sin_negativos():
    assert np.array_equal(modulo.sin_negativos(np.array([-3, 5, -1, 8])), np.array([0, 5, 0, 8]))
