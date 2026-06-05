import ejercicios
import pandas as pd


RANKING = pd.DataFrame({
    "nombre":    ["Steelix",  "Magnemite", "Magneton",  "Onix",  "Scizor", "Forretress", "Skarmory"],
    "tipo":      ["Acero",    "Eléctrico", "Eléctrico", "Roca",  "Acero",  "Acero",      "Acero"],
    "nivel":     [35,         20,          28,          15,      32,       25,            30],
    "hp":        [75,         25,          50,          35,      65,       58,            65],
    "victorias": [10,         3,           7,           2,       9,        6,             8],
})


def test_contar_por_tipo():
    res = ejercicios.contar_por_tipo(RANKING)
    assert res["Acero"] == 4
    assert res["Eléctrico"] == 2
    assert res["Roca"] == 1


def test_nivel_promedio_por_tipo():
    res = ejercicios.nivel_promedio_por_tipo(RANKING)
    assert abs(res["Acero"] - 30.5) < 1e-6
    assert abs(res["Eléctrico"] - 24.0) < 1e-6
    assert abs(res["Roca"] - 15.0) < 1e-6


def test_tipo_mas_victorias():
    res = ejercicios.tipo_mas_victorias(RANKING)
    assert res == "Acero"


def test_resumen_por_tipo():
    res = ejercicios.resumen_por_tipo(RANKING)
    assert len(res) == 3
    assert res[0] == "Acero: 4 Pokémon | Nivel promedio: 30.5 | Victorias: 33"
    assert res[1] == "Eléctrico: 2 Pokémon | Nivel promedio: 24.0 | Victorias: 10"
    assert res[2] == "Roca: 1 Pokémon | Nivel promedio: 15.0 | Victorias: 2"
