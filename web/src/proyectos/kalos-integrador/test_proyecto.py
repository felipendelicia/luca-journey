import ejercicios


def test_excepciones_y_validacion():
    assert ejercicios.crear_pokemon("Pikachu", 25, 100) == {"nombre": "pikachu", "nivel": 25, "hp": 100}
    raised = False
    try:
        ejercicios.crear_pokemon("", 25, 100)
    except ejercicios.ErrorBatalla:
        raised = True
    assert raised, "nombre vacío debería lanzar ErrorBatalla"
    raised = False
    try:
        ejercicios.crear_pokemon("Raichu", 0, 100)
    except ejercicios.ErrorBatalla:
        raised = True
    assert raised, "nivel 0 debería lanzar ErrorBatalla"
    raised = False
    try:
        ejercicios.crear_pokemon("Surskit", 10, 0)
    except ejercicios.ErrorBatalla:
        raised = True
    assert raised, "hp 0 debería lanzar ErrorBatalla"


def test_combate_robusto():
    atacante = {"nombre": "pikachu", "nivel": 25, "hp": 100}
    defensor = {"nombre": "surskit", "nivel": 10, "hp": 50}
    resultado = ejercicios.atacar(atacante, defensor, 4)
    assert resultado == {"nombre": "surskit", "nivel": 10, "hp": 42}
    assert ejercicios.atacar(None, defensor, 4) is None
    raised = False
    try:
        ejercicios.atacar(atacante, defensor, 0)
    except ejercicios.ErrorBatalla:
        raised = True
    assert raised, "poder 0 debería lanzar ErrorBatalla"


def test_casos_limite_equipo():
    assert ejercicios.hp_total([{"hp": 50}, {"hp": 30}]) == 80
    assert ejercicios.hp_total([{"hp": 0}, {"nombre": "raro"}]) == 0
    assert ejercicios.hp_total([]) == 0
    assert ejercicios.hp_total(None) == 0
    assert ejercicios.equipo_vivo([{"hp": 50}, {"hp": 0}]) is True
    assert ejercicios.equipo_vivo([{"hp": 0}, {"hp": 0}]) is False
    assert ejercicios.equipo_vivo([]) is False


def test_ronda_completa():
    a = [{"nombre": "pikachu", "nivel": 25, "hp": 100}]
    b = [{"nombre": "surskit", "nivel": 10, "hp": 50}]
    assert ejercicios.ronda(a, b, 4) == {"atacante": "pikachu", "defensor": "surskit", "dano": 8, "hp_defensor": 42}
    assert ejercicios.ronda(None, b, 4) == {"error": "equipo inválido"}
    assert ejercicios.ronda(a, b, 0) == {"error": "poder inválido"}


def test_verificar_sistema():
    ejercicios.verificar_sistema()
