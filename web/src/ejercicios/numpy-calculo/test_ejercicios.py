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


def test_minimo():
    assert modulo.minimo(np.array([3, 1, 2])) == 1


def test_maximo():
    assert modulo.maximo(np.array([3, 9, 2])) == 9


def test_rango():
    assert modulo.rango(np.array([3, 9, 1])) == 8


def test_producto():
    assert modulo.producto(np.array([2, 3, 4])) == 24


def test_raiz():
    assert np.array_equal(modulo.raiz(np.array([4, 9, 16])), np.array([2.0, 3.0, 4.0]))


def test_acumulado():
    assert np.array_equal(modulo.acumulado(np.array([1, 2, 3, 4])), np.array([1, 3, 6, 10]))


def test_media_por_fila():
    assert np.array_equal(modulo.media_por_fila(np.array([[2, 4], [10, 20]])), np.array([3.0, 15.0]))


def test_maximo_por_columna():
    assert np.array_equal(modulo.maximo_por_columna(np.array([[1, 9], [7, 2]])), np.array([7, 9]))


def test_clip_valores():
    assert np.array_equal(modulo.clip_valores(np.array([-5, 50, 200]), 0, 100), np.array([0, 50, 100]))


def test_proporcion_mayores():
    assert modulo.proporcion_mayores(np.array([1, 2, 3, 4]), 2) == 0.5


def test_donde_mayor():
    assert np.array_equal(modulo.donde_mayor(np.array([1, 5, 2, 9]), 3), np.array([0, 5, 0, 9]))
