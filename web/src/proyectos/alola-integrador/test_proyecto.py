import ejercicios


def test_config():
    assert ejercicios.parsear_config("# bot\nMINIMO=20\nMODO=diario") == {"MINIMO": "20", "MODO": "diario"}
    assert ejercicios.parsear_config("") == {}


def test_cargar():
    assert ejercicios.cargar_pokes(["Pikachu,30", "Onix,12"]) == [{"nombre": "Pikachu", "nivel": 30}, {"nombre": "Onix", "nivel": 12}]


def test_seleccionar():
    pokes = [{"nombre": "a", "nivel": 10}, {"nombre": "b", "nivel": 40}, {"nombre": "c", "nivel": 25}]
    assert ejercicios.seleccionar(pokes, 20) == [{"nombre": "b", "nivel": 40}, {"nombre": "c", "nivel": 25}]


def test_ejecutar():
    assert ejercicios.ejecutar("MINIMO=20", ["Pikachu,30", "Onix,12", "Snorlax,25"]) == "2 Pokémon listos (nivel >= 20)."
    assert ejercicios.ejecutar("", ["Pikachu,5"]) == "1 Pokémon listos (nivel >= 1)."
