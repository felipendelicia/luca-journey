import ejercicios


def test_validar_nivel():
    assert ejercicios.validar_nivel(50) == 50
    assert ejercicios.validar_nivel(1) == 1
    assert ejercicios.validar_nivel(100) == 100
    raised = False
    try:
        ejercicios.validar_nivel(0)
    except ValueError:
        raised = True
    assert raised, "validar_nivel(0) debería lanzar ValueError"
    raised = False
    try:
        ejercicios.validar_nivel(101)
    except ValueError:
        raised = True
    assert raised, "validar_nivel(101) debería lanzar ValueError"


def test_validar_nombre():
    assert ejercicios.validar_nombre("Pikachu") == "pikachu"
    assert ejercicios.validar_nombre("SURSKIT") == "surskit"
    raised = False
    try:
        ejercicios.validar_nombre("")
    except ValueError:
        raised = True
    assert raised, "validar_nombre('') debería lanzar ValueError"
    raised = False
    try:
        ejercicios.validar_nombre(42)
    except ValueError:
        raised = True
    assert raised, "validar_nombre(42) debería lanzar ValueError"


def test_validar_tipo():
    assert ejercicios.validar_tipo("fuego") == "fuego"
    assert ejercicios.validar_tipo("roca") == "roca"
    raised = False
    try:
        ejercicios.validar_tipo("dragón")
    except ValueError:
        raised = True
    assert raised, "validar_tipo('dragón') debería lanzar ValueError"
    raised = False
    try:
        ejercicios.validar_tipo("")
    except ValueError:
        raised = True
    assert raised, "validar_tipo('') debería lanzar ValueError"


def test_registrar_pokemon():
    assert ejercicios.registrar_pokemon("Pikachu", "fuego", 25) == {"nombre": "pikachu", "tipo": "fuego", "nivel": 25}
    raised = False
    try:
        ejercicios.registrar_pokemon("", "fuego", 25)
    except ValueError:
        raised = True
    assert raised, "nombre vacío debería lanzar ValueError"
    raised = False
    try:
        ejercicios.registrar_pokemon("Raichu", "dragón", 50)
    except ValueError:
        raised = True
    assert raised, "tipo inválido debería lanzar ValueError"
    raised = False
    try:
        ejercicios.registrar_pokemon("Surskit", "bug", 200)
    except ValueError:
        raised = True
    assert raised, "nivel inválido debería lanzar ValueError"
