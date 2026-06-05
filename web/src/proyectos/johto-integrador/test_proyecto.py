import ejercicios
import numpy as np
import pandas as pd


LIGA = pd.DataFrame({
    "nombre":    ["Pikachu",   "Raichu",    "Gengar",   "Alakazam", "Machamp", "Steelix", "Gyarados", "Dragonite", "Espeon",    "Umbreon"],
    "tipo":      ["Eléctrico", "Eléctrico", "Fantasma", "Psíquico", "Pelea",   "Acero",   "Agua",     "Dragón",    "Psíquico",  "Siniestro"],
    "nivel":     [25,          40,          38,         45,         42,        35,        45,         55,          38,          32],
    "hp":        [35,          60,          60,         55,         90,        75,        95,         91,          65,          65],
    "ataque":    [55,          90,          65,         50,         130,       85,        125,        134,         65,          65],
    "victorias": [5,           12,          10,         15,         11,        8,         16,         20,          9,           7],
})


def test_preparar_stats():
    mat = ejercicios.preparar_stats(LIGA)
    assert mat.shape == (10, 2)
    assert mat[0].tolist() == [35, 55]
    assert mat[-1].tolist() == [65, 65]


def test_normalizar_columna():
    norm = ejercicios.normalizar_columna(LIGA, "nivel")
    assert len(norm) == 10
    assert abs(norm[0] - 0.0) < 1e-6   # Pikachu nivel 25 = min
    assert abs(norm[7] - 1.0) < 1e-6   # Dragonite nivel 55 = max
    assert all(0.0 <= v <= 1.0 for v in norm)


def test_ranking_por_tipo():
    res = ejercicios.ranking_por_tipo(LIGA)
    assert list(res.columns) == ["tipo", "cantidad", "nivel_max", "victorias_totales"]
    primer = res.iloc[0]
    assert primer["tipo"] == "Psíquico"   # 24 victorias (Alakazam 15 + Espeon 9)
    assert primer["victorias_totales"] == 24
    # verificar que está ordenado descendente
    vics = list(res["victorias_totales"])
    assert vics == sorted(vics, reverse=True)


def test_informe_liga():
    info = ejercicios.informe_liga(LIGA)
    assert info["total_pokemon"] == 10
    assert abs(info["nivel_promedio"] - 39.5) < 1e-6
    assert info["mvp"] == "Dragonite"
    assert info["tipo_dominante"] == "Psíquico"
    assert abs(info["stats_normalizadas"][0] - 0.0) < 1e-6
    assert abs(info["stats_normalizadas"][7] - 1.0) < 1e-6


def test_reporte_texto():
    texto = ejercicios.reporte_texto(LIGA)
    assert "Liga de Johto — Informe" in texto
    assert "Total: 10 Pokémon" in texto
    assert "Nivel promedio: 39.5" in texto
    assert "MVP: Dragonite" in texto
    assert "Tipo dominante: Psíquico" in texto
