import ejercicios


def test_categoria():
    assert ejercicios.categoria(3) == "principiante"
    assert ejercicios.categoria(9) == "principiante"
    assert ejercicios.categoria(10) == "intermedio"
    assert ejercicios.categoria(15) == "intermedio"
    assert ejercicios.categoria(29) == "intermedio"
    assert ejercicios.categoria(30) == "experto"
    assert ejercicios.categoria(36) == "experto"


def test_puede_combatir():
    assert ejercicios.puede_combatir({"nombre": "Starmie", "tipo": "agua", "nivel": 21, "estado": "normal"}) is True
    assert ejercicios.puede_combatir({"nombre": "Horsea",  "tipo": "agua", "nivel": 8,  "estado": "dormido"}) is False
    assert ejercicios.puede_combatir({"nombre": "Geodude", "tipo": "roca", "nivel": 4,  "estado": "normal"}) is False
    assert ejercicios.puede_combatir({"nombre": "Magikarp","tipo": "agua", "nivel": 3,  "estado": "paralizado"}) is False
    assert ejercicios.puede_combatir({"nombre": "Psyduck", "tipo": "agua", "nivel": 15, "estado": "normal"}) is True


def test_filtrar_tipo():
    EQUIPO = [
        {"nombre": "Starmie",  "tipo": "agua", "nivel": 21, "estado": "normal"},
        {"nombre": "Horsea",   "tipo": "agua", "nivel": 8,  "estado": "dormido"},
        {"nombre": "Geodude",  "tipo": "roca", "nivel": 5,  "estado": "normal"},
        {"nombre": "Magikarp", "tipo": "agua", "nivel": 3,  "estado": "paralizado"},
        {"nombre": "Psyduck",  "tipo": "agua", "nivel": 15, "estado": "normal"},
    ]
    agua = ejercicios.filtrar_tipo(EQUIPO, "agua")
    assert len(agua) == 4
    assert all(p["tipo"] == "agua" for p in agua)
    roca = ejercicios.filtrar_tipo(EQUIPO, "roca")
    assert len(roca) == 1
    assert roca[0]["nombre"] == "Geodude"
    fuego = ejercicios.filtrar_tipo(EQUIPO, "fuego")
    assert fuego == []


def test_resumen_equipo():
    EQUIPO = [
        {"nombre": "Starmie",  "tipo": "agua", "nivel": 21, "estado": "normal"},
        {"nombre": "Horsea",   "tipo": "agua", "nivel": 8,  "estado": "dormido"},
        {"nombre": "Geodude",  "tipo": "roca", "nivel": 5,  "estado": "normal"},
        {"nombre": "Magikarp", "tipo": "agua", "nivel": 3,  "estado": "paralizado"},
        {"nombre": "Psyduck",  "tipo": "agua", "nivel": 15, "estado": "normal"},
    ]
    res = ejercicios.resumen_equipo(EQUIPO)
    assert res == [
        "Starmie: intermedio | listo",
        "Horsea: principiante | no disponible",
        "Geodude: principiante | listo",
        "Magikarp: principiante | no disponible",
        "Psyduck: intermedio | listo",
    ]
