import ejercicios


def test_agregar_pokemon():
    equipo = [{"nombre": "Bulbasaur", "tipo": "planta", "nivel": 5, "ps": 45}]
    resultado = ejercicios.agregar_pokemon(equipo, "Oddish", "planta", 12, 55)
    assert len(resultado) == 2
    assert resultado[-1] == {"nombre": "Oddish", "tipo": "planta", "nivel": 12, "ps": 55}


def test_filtrar_nivel_minimo():
    EQUIPO = [
        {"nombre": "Vileplume",  "tipo": "planta", "nivel": 29, "ps": 75},
        {"nombre": "Weepinbell", "tipo": "planta", "nivel": 24, "ps": 65},
        {"nombre": "Tangela",    "tipo": "planta", "nivel": 22, "ps": 70},
    ]
    res25 = ejercicios.filtrar_nivel_minimo(EQUIPO, 25)
    assert len(res25) == 1
    assert res25[0]["nombre"] == "Vileplume"

    res22 = ejercicios.filtrar_nivel_minimo(EQUIPO, 22)
    assert len(res22) == 3

    res30 = ejercicios.filtrar_nivel_minimo(EQUIPO, 30)
    assert res30 == []


def test_ordenar_por_ps():
    EQUIPO = [
        {"nombre": "Vileplume",  "tipo": "planta", "nivel": 29, "ps": 75},
        {"nombre": "Weepinbell", "tipo": "planta", "nivel": 24, "ps": 65},
        {"nombre": "Tangela",    "tipo": "planta", "nivel": 22, "ps": 70},
    ]
    ordenado = ejercicios.ordenar_por_ps(EQUIPO)
    assert [p["nombre"] for p in ordenado] == ["Vileplume", "Tangela", "Weepinbell"]
    assert [p["ps"] for p in ordenado] == [75, 70, 65]
    # original no modificado
    assert EQUIPO[0]["nombre"] == "Vileplume"
    assert EQUIPO[1]["nombre"] == "Weepinbell"


def test_resumen_equipo():
    EQUIPO = [
        {"nombre": "Vileplume",  "tipo": "planta", "nivel": 29, "ps": 75},
        {"nombre": "Weepinbell", "tipo": "planta", "nivel": 24, "ps": 65},
        {"nombre": "Tangela",    "tipo": "planta", "nivel": 22, "ps": 70},
    ]
    res = ejercicios.resumen_equipo(EQUIPO)
    assert res["cantidad"] == 3
    assert res["ps_total"] == 210
    assert res["nivel_promedio"] == 25.0
    assert res["mas_fuerte"] == "Vileplume"
