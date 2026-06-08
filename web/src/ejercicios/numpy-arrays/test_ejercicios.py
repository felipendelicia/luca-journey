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


def test_sumar_arrays():
    assert np.array_equal(modulo.sumar_arrays(np.array([1, 2]), np.array([10, 20])), np.array([11, 22]))


def test_mayores_a():
    assert np.array_equal(modulo.mayores_a(np.array([5, 20, 12, 30]), 15), np.array([20, 30]))


def test_contar_mayores():
    assert modulo.contar_mayores(np.array([5, 20, 30]), 15) == 2


def test_array_de():
    assert np.array_equal(modulo.array_de(7, 3), np.array([7, 7, 7]))


def test_invertir_array():
    assert np.array_equal(modulo.invertir_array(np.array([1, 2, 3])), np.array([3, 2, 1]))


def test_primeros_n():
    assert np.array_equal(modulo.primeros_n(np.array([1, 2, 3, 4]), 2), np.array([1, 2]))


def test_ultimos_n():
    assert np.array_equal(modulo.ultimos_n(np.array([1, 2, 3, 4]), 2), np.array([3, 4]))


def test_multiplicar_por():
    assert np.array_equal(modulo.multiplicar_por(np.array([1, 2, 3]), 10), np.array([10, 20, 30]))


def test_reemplazar_negativos():
    assert np.array_equal(modulo.reemplazar_negativos(np.array([-3, 5, -1, 2])), np.array([0, 5, 0, 2]))


def test_indices_donde():
    assert np.array_equal(modulo.indices_donde(np.array([5, 9, 5, 1]), 5), np.array([0, 2]))


def test_concatenar():
    assert np.array_equal(modulo.concatenar(np.array([1, 2]), np.array([3, 4])), np.array([1, 2, 3, 4]))
