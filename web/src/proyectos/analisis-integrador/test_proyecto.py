import ejercicios
import pandas as pd


DRAGONES = pd.DataFrame({
    "nombre":    ["Dratini",  "Dragonair", "Dragonite", "Kingdra", "Seadra", "Horsea", "Gyarados"],
    "tipo":      ["Dragón",   "Dragón",    "Dragón",    "Agua",    "Agua",   "Agua",   "Agua"],
    "nivel":     [20,         35,          55,          40,        28,       15,       45],
    "hp":        [41,         61,          91,          75,        55,       30,       95],
    "victorias": [3,          8,           20,          14,        6,        1,        18],
})


def test_filtrar_elite():
    res = ejercicios.filtrar_elite(DRAGONES, 35)
    nombres = list(res["nombre"])
    assert nombres == ["Dragonite", "Gyarados", "Kingdra", "Dragonair"]


def test_resumen_por_tipo():
    res = ejercicios.resumen_por_tipo(DRAGONES)
    assert res["Dragón"]["cantidad"] == 3
    assert abs(res["Dragón"]["nivel_promedio"] - 36.7) < 0.05
    assert res["Dragón"]["victorias_totales"] == 31
    assert res["Agua"]["cantidad"] == 4
    assert abs(res["Agua"]["nivel_promedio"] - 32.0) < 0.05
    assert res["Agua"]["victorias_totales"] == 39


def test_mvp():
    assert ejercicios.mvp(DRAGONES) == "Dragonite"


def test_reporte_final():
    res = ejercicios.reporte_final(DRAGONES)
    assert res["elite"] == ["Dragonite", "Gyarados", "Kingdra", "Dragonair"]
    assert res["mvp"] == "Dragonite"
    assert res["tipo_dominante"] == "Agua"
    assert abs(res["victoria_rate"] - 10.0) < 1e-6
