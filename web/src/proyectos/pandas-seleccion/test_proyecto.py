import ejercicios
import pandas as pd


REGISTRO = pd.DataFrame({
    "nombre": ["Gastly",   "Haunter",  "Gengar",   "Misdreavus", "Murkrow",   "Umbreon"],
    "tipo":   ["Fantasma", "Fantasma", "Fantasma", "Fantasma",   "Siniestro", "Siniestro"],
    "nivel":  [15,         25,         38,         20,           18,          30],
    "hp":     [30,         45,         60,         45,           40,          65],
})


def test_filtrar_nivel_minimo():
    res = ejercicios.filtrar_nivel_minimo(REGISTRO, 25)
    nombres = list(res["nombre"])
    assert set(nombres) == {"Haunter", "Gengar", "Umbreon"}
    res2 = ejercicios.filtrar_nivel_minimo(REGISTRO, 38)
    assert list(res2["nombre"]) == ["Gengar"]
    res3 = ejercicios.filtrar_nivel_minimo(REGISTRO, 40)
    assert len(res3) == 0


def test_de_tipo():
    res = ejercicios.de_tipo(REGISTRO, "Fantasma")
    assert set(res["nombre"]) == {"Gastly", "Haunter", "Gengar", "Misdreavus"}
    res2 = ejercicios.de_tipo(REGISTRO, "Siniestro")
    assert set(res2["nombre"]) == {"Murkrow", "Umbreon"}
    res3 = ejercicios.de_tipo(REGISTRO, "Fuego")
    assert len(res3) == 0


def test_top_n():
    res = ejercicios.top_n(REGISTRO, 1)
    assert res == ["Gengar"]
    res2 = ejercicios.top_n(REGISTRO, 3)
    assert res2[0] == "Gengar"
    assert set(res2) == {"Gengar", "Umbreon", "Haunter"}


def test_buscar_y_mostrar():
    res = ejercicios.buscar_y_mostrar(REGISTRO, "Fantasma", 20)
    assert res == ["Gengar (Lv.38)", "Haunter (Lv.25)", "Misdreavus (Lv.20)"]
    res2 = ejercicios.buscar_y_mostrar(REGISTRO, "Fuego", 10)
    assert res2 == []
    res3 = ejercicios.buscar_y_mostrar(REGISTRO, "Siniestro", 25)
    assert res3 == ["Umbreon (Lv.30)"]
