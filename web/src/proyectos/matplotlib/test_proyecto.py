import ejercicios
import pandas as pd


EQUIPO = pd.DataFrame({
    "nombre":  ["Seel",   "Dewgong", "Jynx",  "Piloswine", "Sneasel", "Lapras"],
    "nivel":   [20,       30,        28,      35,          22,        32],
    "hp":      [65,       90,        65,      100,         55,        130],
    "tipo":    ["Agua",   "Agua",    "Hielo", "Tierra",    "Hielo",   "Agua"],
})


def test_datos_barras():
    nombres, niveles = ejercicios.datos_barras(EQUIPO)
    assert nombres == ["Seel", "Dewgong", "Jynx", "Piloswine", "Sneasel", "Lapras"]
    assert niveles == [20, 30, 28, 35, 22, 32]


def test_datos_dispersion():
    niveles, hp = ejercicios.datos_dispersion(EQUIPO)
    assert niveles == [20, 30, 28, 35, 22, 32]
    assert hp == [65, 90, 65, 100, 55, 130]


def test_datos_histograma():
    hp = ejercicios.datos_histograma(EQUIPO, "hp")
    assert hp == [65, 90, 65, 100, 55, 130]
    niveles = ejercicios.datos_histograma(EQUIPO, "nivel")
    assert niveles == [20, 30, 28, 35, 22, 32]


def test_graficar_equipo():
    nombres, niveles = ejercicios.graficar_equipo(EQUIPO)
    assert nombres == ["Seel", "Dewgong", "Jynx", "Piloswine", "Sneasel", "Lapras"]
    assert niveles == [20, 30, 28, 35, 22, 32]
