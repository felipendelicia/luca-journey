import ejercicios

POKEMON = [
    {"nombre": "Meowth",  "tipo": "normal", "nivel": 14, "hp": 45},
    {"nombre": "Arbok",   "tipo": "veneno", "nivel": 20, "hp": 60},
    {"nombre": "Weezing", "tipo": "veneno", "nivel": 22, "hp": 65},
    {"nombre": "Rhydon",  "tipo": "roca",   "nivel": 38, "hp": 105},
    {"nombre": "Persian", "tipo": "normal", "nivel": 30, "hp": 65},
]


def test_filtrar_y_ordenar():
    veneno = ejercicios.filtrar_tipo(POKEMON, "veneno")
    assert len(veneno) == 2
    assert all(p["tipo"] == "veneno" for p in veneno)
    assert ejercicios.filtrar_tipo(POKEMON, "agua") == []

    ordenados = ejercicios.ordenar_por(POKEMON, "nivel")
    assert ordenados[0]["nombre"] == "Meowth"
    assert ordenados[-1]["nombre"] == "Rhydon"

    por_hp = ejercicios.ordenar_por(POKEMON, "hp")
    assert por_hp[0]["nombre"] == "Meowth"
    assert por_hp[-1]["nombre"] == "Rhydon"


def test_estadisticas():
    stats = ejercicios.estadisticas(POKEMON, "nivel")
    assert stats["minimo"] == 14
    assert stats["maximo"] == 38
    assert abs(stats["promedio"] - 24.8) < 0.01

    stats_hp = ejercicios.estadisticas(POKEMON, "hp")
    assert stats_hp["minimo"] == 45
    assert stats_hp["maximo"] == 105
    assert abs(stats_hp["promedio"] - 68.0) < 0.01


def test_buscar_nombre():
    # "ok" aparece en "Arbok"
    res = ejercicios.buscar_nombre(POKEMON, "ok")
    nombres = [p["nombre"] for p in res]
    assert "Arbok" in nombres
    assert len(res) == 1

    # "ing" aparece en "Weezing"
    res2 = ejercicios.buscar_nombre(POKEMON, "ing")
    assert len(res2) == 1
    assert res2[0]["nombre"] == "Weezing"

    res3 = ejercicios.buscar_nombre(POKEMON, "xyz")
    assert res3 == []

    # case-insensitive: "ME" encuentra "Meowth"
    res4 = ejercicios.buscar_nombre(POKEMON, "ME")
    assert any(p["nombre"] == "Meowth" for p in res4)


def test_reporte():
    r = ejercicios.reporte(POKEMON, "veneno")
    assert [p["nombre"] for p in r["equipo"]] == ["Arbok", "Weezing"]
    assert r["stats_nivel"]["minimo"] == 20
    assert r["stats_nivel"]["maximo"] == 22
    assert abs(r["stats_hp"]["promedio"] - 62.5) < 0.01
