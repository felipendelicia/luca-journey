import ejercicios
import numpy as np


def test_crear_stats():
    arr = ejercicios.crear_stats([10, 20, 30])
    assert arr.tolist() == [10, 20, 30]
    arr2 = ejercicios.crear_stats([45, 80])
    assert arr2.tolist() == [45, 80]


def test_estadisticas():
    res = ejercicios.estadisticas(np.array([10, 20, 30]))
    assert res["total"] == 60
    assert abs(res["promedio"] - 20.0) < 1e-6
    assert res["maximo"] == 30
    assert res["minimo"] == 10
    res2 = ejercicios.estadisticas(np.array([5, 5, 5]))
    assert res2["total"] == 15
    assert abs(res2["promedio"] - 5.0) < 1e-6


def test_fuertes_y_debiles():
    fuertes, debiles = ejercicios.fuertes_y_debiles(np.array([45, 80, 65, 30]), 60)
    assert set(fuertes.tolist()) == {80, 65}
    assert set(debiles.tolist()) == {45, 30}
    fuertes2, debiles2 = ejercicios.fuertes_y_debiles(np.array([10, 50, 90]), 50)
    assert set(fuertes2.tolist()) == {50, 90}
    assert set(debiles2.tolist()) == {10}


def test_resumen_equipo():
    res = ejercicios.resumen_equipo(["Pidgey", "Hoothoot"], np.array([45, 60]))
    assert res[0] == "Pidgey: 45 pts"
    assert res[1] == "Hoothoot: 60 pts"
    assert res[2] == "Promedio: 52.5 pts"
    assert len(res) == 3
