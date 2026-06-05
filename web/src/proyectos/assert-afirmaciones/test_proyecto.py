import ejercicios


def test_verificar_positivo():
    assert ejercicios.verificar_positivo(5) == 5
    assert ejercicios.verificar_positivo(1) == 1
    raised = False
    try:
        ejercicios.verificar_positivo(0)
    except AssertionError:
        raised = True
    assert raised, "verificar_positivo(0) debería lanzar AssertionError"
    raised = False
    try:
        ejercicios.verificar_positivo(-3)
    except AssertionError:
        raised = True
    assert raised, "verificar_positivo(-3) debería lanzar AssertionError"


def test_verificar_lista():
    assert ejercicios.verificar_lista([10, 20, 30]) == 10
    assert ejercicios.verificar_lista(["pikachu"]) == "pikachu"
    raised = False
    try:
        ejercicios.verificar_lista([])
    except AssertionError:
        raised = True
    assert raised, "verificar_lista([]) debería lanzar AssertionError"


def test_calcular_promedio():
    assert ejercicios.calcular_promedio([10, 20, 30]) == 20.0
    assert ejercicios.calcular_promedio([5, 5]) == 5.0
    raised = False
    try:
        ejercicios.calcular_promedio([])
    except AssertionError:
        raised = True
    assert raised, "calcular_promedio([]) debería lanzar AssertionError"


def test_resumen_equipo():
    assert ejercicios.resumen_equipo([10, 20, 30]) == {"cantidad": 3, "promedio": 20.0, "max": 30, "min": 10}
    raised = False
    try:
        ejercicios.resumen_equipo([])
    except AssertionError:
        raised = True
    assert raised, "resumen_equipo([]) debería lanzar AssertionError"
    raised = False
    try:
        ejercicios.resumen_equipo([5, -1, 10])
    except AssertionError:
        raised = True
    assert raised, "resumen_equipo con nivel negativo debería lanzar AssertionError"
