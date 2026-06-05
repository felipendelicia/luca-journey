import ejercicios


def test_extraer_nombre_nivel():
    assert ejercicios.extraer_nombre_nivel({"nombre": "Solrock", "nivel": 26}) == ("Solrock", 26)
    assert ejercicios.extraer_nombre_nivel({"nombre": "Lunatone", "nivel": 26}) == ("Lunatone", 26)


def test_filtrar_por_tipo():
    lista = [
        {"nombre": "Solrock", "tipo": "roca"},
        {"nombre": "Lunatone", "tipo": "roca"},
        {"nombre": "Ralts", "tipo": "psíquico"},
    ]
    assert ejercicios.filtrar_por_tipo(lista, "roca") == ["Solrock", "Lunatone"]
    assert ejercicios.filtrar_por_tipo(lista, "psíquico") == ["Ralts"]
    assert ejercicios.filtrar_por_tipo(lista, "agua") == []


def test_manejar_respuesta():
    assert ejercicios.manejar_respuesta(200, {"nombre": "Ralts"}) == {"nombre": "Ralts"}
    assert ejercicios.manejar_respuesta(404, {"error": "nope"}) is None
    assert ejercicios.manejar_respuesta(500, {}) is None


def test_resumen_equipo():
    lista = [
        {"nombre": "Solrock", "tipo": "roca", "nivel": 26},
        {"nombre": "Lunatone", "tipo": "roca", "nivel": 26},
    ]
    assert ejercicios.resumen_equipo(lista) == [
        "Solrock (tipo: roca, nivel: 26)",
        "Lunatone (tipo: roca, nivel: 26)",
    ]
