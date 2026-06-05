import ejercicios


def test_calcular_dano():
    assert ejercicios.calcular_dano(50, 20) == 30
    assert ejercicios.calcular_dano(10, 30) == 0
    assert ejercicios.calcular_dano(25, 25) == 0
    raised = False
    try:
        ejercicios.calcular_dano(-5, 10)
    except ValueError:
        raised = True
    assert raised, "calcular_dano(-5, 10) debería lanzar ValueError"
    raised = False
    try:
        ejercicios.calcular_dano(10, -3)
    except ValueError:
        raised = True
    assert raised, "calcular_dano(10, -3) debería lanzar ValueError"


def test_aplicar_dano():
    assert ejercicios.aplicar_dano(100, 30) == 70
    assert ejercicios.aplicar_dano(20, 50) == 0
    assert ejercicios.aplicar_dano(0, 10) == 0
    raised = False
    try:
        ejercicios.aplicar_dano(-1, 10)
    except ValueError:
        raised = True
    assert raised, "aplicar_dano(-1, 10) debería lanzar ValueError"


def test_probar_calcular_dano():
    # la función de test no debe lanzar ninguna excepción
    ejercicios.probar_calcular_dano()


def test_simular_turno():
    assert ejercicios.simular_turno(100, 50, 20) == {"dano": 30, "hp_final": 70}
    assert ejercicios.simular_turno(20, 10, 30) == {"dano": 0, "hp_final": 20}
    assert ejercicios.simular_turno(100, -5, 20) == {"error": "valores inválidos", "hp_final": 100}
