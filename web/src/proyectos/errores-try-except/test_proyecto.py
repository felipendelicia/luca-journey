import ejercicios


def test_dividir_seguro():
    assert ejercicios.dividir_seguro(10, 2) == 5.0
    assert ejercicios.dividir_seguro(9, 3) == 3.0
    assert ejercicios.dividir_seguro(7, 0) is None


def test_a_entero():
    assert ejercicios.a_entero("42") == 42
    assert ejercicios.a_entero("-5") == -5
    assert ejercicios.a_entero("pikachu") == 0
    assert ejercicios.a_entero("3.14") == 0


def test_buscar_pokemon():
    assert ejercicios.buscar_pokemon("surskit") == {"nivel": 10, "tipo": "agua"}
    assert ejercicios.buscar_pokemon("mewtwo") is None


def test_nivel_seguro():
    assert ejercicios.nivel_seguro("vivillon", 4) == 3.0
    assert ejercicios.nivel_seguro("mewtwo", 2) == -1
    assert ejercicios.nivel_seguro("ledyba", 0) == -1
    assert ejercicios.nivel_seguro("surskit", 2) == 5.0
