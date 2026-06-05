import ejercicios

ENTRENADORES = [
    {"nombre": "Ash",    "insignias": 8, "pokemones": [{"nombre": "Pikachu",   "nivel": 55}, {"nombre": "Charizard",  "nivel": 60}]},
    {"nombre": "Gary",   "insignias": 8, "pokemones": [{"nombre": "Blastoise", "nivel": 58}, {"nombre": "Nidoking",   "nivel": 52}]},
    {"nombre": "Misty",  "insignias": 5, "pokemones": [{"nombre": "Starmie",   "nivel": 42}, {"nombre": "Psyduck",    "nivel": 28}]},
    {"nombre": "Brock",  "insignias": 4, "pokemones": [{"nombre": "Onix",      "nivel": 35}, {"nombre": "Geodude",    "nivel": 18}]},
    {"nombre": "Jessie", "insignias": 2, "pokemones": [{"nombre": "Arbok",     "nivel": 24}, {"nombre": "Wobbuffet",  "nivel": 22}]},
]


def test_clasificados():
    c5 = ejercicios.clasificados(ENTRENADORES, 5)
    assert [e["nombre"] for e in c5] == ["Ash", "Gary", "Misty"]
    c8 = ejercicios.clasificados(ENTRENADORES, 8)
    assert len(c8) == 2
    assert all(e["insignias"] == 8 for e in c8)
    c10 = ejercicios.clasificados(ENTRENADORES, 10)
    assert c10 == []


def test_nivel_equipo():
    ash = ENTRENADORES[0]
    assert abs(ejercicios.nivel_promedio(ash) - 57.5) < 0.01
    assert ejercicios.nivel_maximo(ash) == 60

    brock = ENTRENADORES[3]
    assert abs(ejercicios.nivel_promedio(brock) - 26.5) < 0.01
    assert ejercicios.nivel_maximo(brock) == 35


def test_clase_entrenador():
    e = ejercicios.Entrenador(ENTRENADORES[0])  # Ash, 8 insignias
    assert e.nombre == "Ash"
    assert e.insignias == 8
    assert e.es_finalista() is True
    assert str(e) == "Ash [8 insignias]"

    e2 = ejercicios.Entrenador(ENTRENADORES[2])  # Misty, 5 insignias
    assert e2.es_finalista() is False
    assert str(e2) == "Misty [5 insignias]"


def test_ranking():
    rank = ejercicios.ranking(ENTRENADORES)
    assert len(rank) == 2
    assert all(isinstance(e, ejercicios.Entrenador) for e in rank)
    assert rank[0].nombre == "Ash"   # Charizard nv.60 > Blastoise nv.58
    assert rank[1].nombre == "Gary"


def test_campeon():
    assert ejercicios.campeon(ENTRENADORES) == "Ash"
    solo_jessie = [{"nombre": "Jessie", "insignias": 2, "pokemones": [{"nombre": "Arbok", "nivel": 24}]}]
    assert ejercicios.campeon(solo_jessie) is None
