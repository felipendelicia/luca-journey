import ejercicios


def test_clase_pokemon():
    p = ejercicios.Pokemon("Pikachu", "eléctrico", 10)
    assert p.nombre == "Pikachu"
    assert p.tipo == "eléctrico"
    assert p.nivel == 10
    p2 = ejercicios.Pokemon("Charizard", "fuego", 36)
    assert p2.nombre == "Charizard"
    assert p2.nivel == 36


def test_metodo_presentar():
    assert ejercicios.Pokemon("Pikachu", "eléctrico", 10).presentar() == "Soy Pikachu, de tipo eléctrico. Nivel: 10."
    assert ejercicios.Pokemon("Charizard", "fuego", 36).presentar() == "Soy Charizard, de tipo fuego. Nivel: 36."


def test_metodo_subir_nivel():
    p = ejercicios.Pokemon("Bulbasaur", "planta", 5)
    p.subir_nivel(3)
    assert p.nivel == 8
    p.subir_nivel(10)
    assert p.nivel == 18


def test_desde_dict():
    DATA = [
        {"nombre": "Abra",    "tipo": "psíquico", "nivel": 10},
        {"nombre": "Kadabra", "tipo": "psíquico", "nivel": 30},
        {"nombre": "Gengar",  "tipo": "fantasma", "nivel": 25},
    ]
    pokemons = ejercicios.desde_dict(DATA)
    assert len(pokemons) == 3
    assert pokemons[0].nombre == "Abra"
    assert pokemons[0].tipo == "psíquico"
    assert [p.nivel for p in pokemons] == [10, 30, 25]
