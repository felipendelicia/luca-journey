import ejercicios
import pandas as pd
import numpy as np


CENSO = pd.DataFrame({
    "nombre": ["Primeape", "Poliwrath", "Hitmonlee", "Poliwrath", "Hitmonchan", "Machoke"],
    "tipo":   ["Pelea",   "Agua",     "Pelea",    "Agua",      None,        "Pelea"],
    "nivel":  ["30",      "35",       "28",        "35",        "28",        None],
    "hp":     [65,        90,         50,          90,          50,          np.nan],
})


def test_contar_nulos():
    assert ejercicios.contar_nulos(CENSO) == 3


def test_limpiar_tipos():
    res = ejercicios.limpiar_tipos(CENSO)
    # tipo: None → "Desconocido"
    assert res.loc[res["nombre"] == "Hitmonchan", "tipo"].iloc[0] == "Desconocido"
    # nivel: None → 0 como int
    machoke_nivel = res.loc[res["nombre"] == "Machoke", "nivel"].iloc[0]
    assert machoke_nivel == 0
    assert isinstance(machoke_nivel, (int, np.integer))
    # otros niveles también int
    assert res.loc[res["nombre"] == "Primeape", "nivel"].iloc[0] == 30


def test_sin_duplicados():
    res = ejercicios.sin_duplicados(CENSO)
    # Poliwrath duplicado → ahora solo 1
    assert len(res[res["nombre"] == "Poliwrath"]) == 1
    assert len(res) == 5


def test_censo_limpio():
    res = ejercicios.censo_limpio(CENSO)
    # sin Machoke (hp NaN) y sin Poliwrath duplicado
    assert "Machoke" not in list(res["nombre"])
    assert len(res[res["nombre"] == "Poliwrath"]) == 1
    assert len(res) == 4
    # tipo sin None
    assert res["tipo"].isna().sum() == 0
    # nivel como int
    assert res["nivel"].dtype in [int, np.int64, np.int32]
