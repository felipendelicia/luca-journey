import ejercicios
import pandas as pd


DATA = {
    "nombre": ["Clefairy", "Miltank", "Snubbull", "Jigglypuff", "Wigglytuff"],
    "tipo":   ["Normal",   "Normal",  "Normal",   "Normal",     "Normal"],
    "nivel":  [18,          23,         15,          12,           20],
    "hp":     [40,          95,         60,          45,           70],
}


def test_crear_pokedex():
    df = ejercicios.crear_pokedex(DATA)
    assert list(df.columns) == ["nombre", "tipo", "nivel", "hp"]
    assert len(df) == 5
    assert df.iloc[0]["nombre"] == "Clefairy"


def test_consultar_columna():
    df = pd.DataFrame(DATA)
    nombres = ejercicios.consultar_columna(df, "nombre")
    assert nombres == ["Clefairy", "Miltank", "Snubbull", "Jigglypuff", "Wigglytuff"]
    niveles = ejercicios.consultar_columna(df, "nivel")
    assert niveles == [18, 23, 15, 12, 20]


def test_resumen_numerico():
    df = pd.DataFrame(DATA)
    res = ejercicios.resumen_numerico(df, "nivel")
    assert res["minimo"] == 12
    assert res["maximo"] == 23
    assert abs(res["promedio"] - 17.6) < 1e-6
    res2 = ejercicios.resumen_numerico(df, "hp")
    assert res2["minimo"] == 40
    assert res2["maximo"] == 95
    assert abs(res2["promedio"] - 62.0) < 1e-6


def test_ficha_pokemon():
    df = pd.DataFrame(DATA)
    assert ejercicios.ficha_pokemon(df, "Miltank") == "Miltank | Tipo: Normal | Nivel: 23 | HP: 95"
    assert ejercicios.ficha_pokemon(df, "Clefairy") == "Clefairy | Tipo: Normal | Nivel: 18 | HP: 40"
    assert ejercicios.ficha_pokemon(df, "Marill") == "No encontrado."
