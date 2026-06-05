import ejercicios
import numpy as np


def test_normalizar():
    res = ejercicios.normalizar(np.array([0, 5, 10]))
    assert np.allclose(res, [0.0, 0.5, 1.0])
    res2 = ejercicios.normalizar(np.array([10, 10, 20]))
    assert np.allclose(res2, [0.0, 0.0, 1.0])


def test_por_encima_promedio():
    res = ejercicios.por_encima_promedio(np.array([10, 20, 30, 40]))
    assert set(res.tolist()) == {30, 40}
    res2 = ejercicios.por_encima_promedio(np.array([5, 5, 10]))
    assert res2.tolist() == [10]


def test_comparar_equipos():
    ga, gb = ejercicios.comparar_equipos(np.array([10, 50, 30]), np.array([20, 40, 30]))
    assert ga == 1
    assert gb == 1
    ga2, gb2 = ejercicios.comparar_equipos(np.array([5, 5, 5]), np.array([5, 5, 5]))
    assert ga2 == 0
    assert gb2 == 0
    ga3, gb3 = ejercicios.comparar_equipos(np.array([10, 20, 30]), np.array([5, 5, 5]))
    assert ga3 == 3
    assert gb3 == 0


def test_informe_poder():
    res = ejercicios.informe_poder(np.array([0, 5, 10]))
    assert np.allclose(res["normalizadas"], [0.0, 0.5, 1.0])
    assert res["sobre_promedio"] == 1
    assert abs(res["puntuacion"] - 1.5) < 1e-6
