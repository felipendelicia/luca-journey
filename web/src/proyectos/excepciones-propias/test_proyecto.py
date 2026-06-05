import ejercicios


def test_error_propio():
    assert ejercicios.verificar_vivo(50) == 50
    assert ejercicios.verificar_vivo(1) == 1
    raised = False
    try:
        ejercicios.verificar_vivo(0)
    except ejercicios.ErrorPokemon:
        raised = True
    assert raised, "verificar_vivo(0) debería lanzar ErrorPokemon"
    raised = False
    try:
        ejercicios.verificar_vivo(-5)
    except ejercicios.ErrorPokemon:
        raised = True
    assert raised, "verificar_vivo(-5) debería lanzar ErrorPokemon"


def test_error_nivel():
    assert ejercicios.subir_nivel(50, 10) == 60
    raised = False
    try:
        ejercicios.subir_nivel(95, 10)
    except ejercicios.ErrorNivel:
        raised = True
    assert raised, "subir_nivel(95, 10) debería lanzar ErrorNivel"
    raised = False
    try:
        ejercicios.subir_nivel(30, -5)
    except ejercicios.ErrorNivel:
        raised = True
    assert raised, "subir_nivel(30, -5) debería lanzar ErrorNivel"


def test_atrapar_propio():
    assert ejercicios.intentar_subir(50, 10) == 60
    assert ejercicios.intentar_subir(95, 10) == 95
    assert ejercicios.intentar_subir(30, -5) == 30


def test_combate_seguro():
    assert ejercicios.combate_seguro(30, 10, 5) == {"resultado": "victoria", "nivel": 15}
    assert ejercicios.combate_seguro(0, 10, 5) == {"resultado": "derrota", "nivel": 10}
    assert ejercicios.combate_seguro(30, 98, 10) == {"resultado": "victoria", "nivel": 98}
