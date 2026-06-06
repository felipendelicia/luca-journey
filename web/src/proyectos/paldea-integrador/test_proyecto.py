import ejercicios


def test_cargar():
    assert ejercicios.cargar(["Pikachu,electrico,30"]) == [{"nombre": "Pikachu", "tipo": "electrico", "nivel": 30}]


def test_de_tipo():
    pokes = [{"nombre": "a", "tipo": "agua"}, {"nombre": "b", "tipo": "fuego"}]
    assert ejercicios.de_tipo(pokes, "agua") == [{"nombre": "a", "tipo": "agua"}]


def test_ordenar():
    assert ejercicios.ordenar([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}]) == [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]


def test_ejecutar():
    lineas = ["Squirtle,agua,16", "Charmander,fuego,9", "Gyarados,agua,30"]
    assert ejercicios.ejecutar(lineas, "agua") == "2 Pokémon de tipo agua, el mejor: Gyarados."
    assert ejercicios.ejecutar(lineas, "planta") == "0 Pokémon de tipo planta, el mejor: -."
