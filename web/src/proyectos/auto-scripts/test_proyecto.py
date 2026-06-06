import ejercicios


def test_leer():
    assert ejercicios.leer_opcion(["--tipo", "agua"], "--tipo", "todos") == "agua"
    assert ejercicios.leer_opcion([], "--tipo", "todos") == "todos"
    assert ejercicios.leer_opcion(["--tipo"], "--tipo", "todos") == "todos"


def test_config():
    assert ejercicios.construir_config(["--cantidad", "3", "--shiny"]) == {"tipo": "todos", "cantidad": 3, "shiny": True}
    assert ejercicios.construir_config([]) == {"tipo": "todos", "cantidad": 5, "shiny": False}
    assert ejercicios.construir_config(["--tipo", "agua"]) == {"tipo": "agua", "cantidad": 5, "shiny": False}


def test_resumen():
    assert ejercicios.resumen({"tipo": "agua", "cantidad": 3, "shiny": False}) == "Buscando 3 Pokémon de tipo agua."
    assert ejercicios.resumen({"tipo": "fuego", "cantidad": 1, "shiny": True}) == "Buscando 1 Pokémon de tipo fuego shiny."


def test_ejecutar():
    assert ejercicios.ejecutar(["--tipo", "agua", "--cantidad", "2"]) == "Buscando 2 Pokémon de tipo agua."
    assert ejercicios.ejecutar(["--shiny"]) == "Buscando 5 Pokémon de tipo todos shiny."
