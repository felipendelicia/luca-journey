from ejercicios import buscar, mostrar, responder, pokedex  # CURSO_MODULO=ejercicios

def test_buscar():
    assert buscar("Pikachu") == {"tipo": "eléctrico", "nivel": 10}
    assert buscar("CHARIZARD") == {"tipo": "fuego", "nivel": 36}
    assert buscar("nada") is None

def test_mostrar():
    assert mostrar({"tipo": "fuego", "nivel": 36}) == "Tipo: fuego · Nivel: 36"
    assert mostrar(None) == "No encontrado."

def test_responder():
    assert responder("charizard") == "Tipo: fuego · Nivel: 36"
    assert responder("xxx") == "No encontrado."

def test_pokedex():
    assert pokedex(["pikachu", "xxx"]) == ["Tipo: eléctrico · Nivel: 10", "No encontrado."]
