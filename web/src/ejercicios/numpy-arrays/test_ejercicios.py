"""🧪 Tests — NumPy: Arrays"""
import importlib.util
import os

import numpy as np

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"numpyarrays_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_crear_equipo():
    r = modulo.crear_equipo([5, 12, 30])
    assert isinstance(r, np.ndarray), "Tiene que ser un np.array"
    assert np.array_equal(r, np.array([5, 12, 30]))


def test_rango_niveles():
    assert np.array_equal(modulo.rango_niveles(5), np.array([1, 2, 3, 4, 5]))
    assert np.array_equal(modulo.rango_niveles(1), np.array([1]))


def test_tanque_vacio():
    r = modulo.tanque_vacio(3)
    assert np.array_equal(r, np.zeros(3))
    assert len(r) == 3


def test_doblar_ataque():
    r = modulo.doblar_ataque(np.array([1, 5, 10]))
    assert np.array_equal(r, np.array([2, 10, 20]))


def test_sumar_stats():
    r = modulo.sumar_stats(np.array([10, 20, 30]), np.array([1, 2, 3]))
    assert np.array_equal(r, np.array([11, 22, 33]))


def test_primeros_tres():
    assert np.array_equal(modulo.primeros_tres(np.array([9, 8, 7, 6, 5])), np.array([9, 8, 7]))


def test_superan_umbral():
    r = modulo.superan_umbral(np.array([10, 50, 30, 80, 5]), 40)
    assert np.array_equal(r, np.array([50, 80]))


def test_forma():
    assert modulo.forma(np.array([[1, 2, 3], [4, 5, 6]])) == (2, 3)


def test_aplanar():
    r = modulo.aplanar(np.array([[1, 2], [3, 4]]))
    assert np.array_equal(r, np.array([1, 2, 3, 4]))
    assert r.ndim == 1
