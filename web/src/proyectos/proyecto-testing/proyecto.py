# Líder Wulfric — Función blindada (solución de referencia).

def calcular_dano(ataque, defensa):
    if ataque < 0 or defensa < 0:
        raise ValueError("Los valores deben ser positivos")
    return max(0, ataque - defensa)

def aplicar_dano(hp, dano):
    if hp < 0 or dano < 0:
        raise ValueError("Los valores deben ser positivos")
    return max(0, hp - dano)

def probar_calcular_dano():
    assert calcular_dano(50, 20) == 30
    assert calcular_dano(10, 30) == 0
    assert calcular_dano(25, 25) == 0
    raised = False
    try:
        calcular_dano(-5, 10)
    except ValueError:
        raised = True
    assert raised
    raised = False
    try:
        calcular_dano(10, -3)
    except ValueError:
        raised = True
    assert raised

def simular_turno(hp_rival, ataque_propio, defensa_rival):
    try:
        dano = calcular_dano(ataque_propio, defensa_rival)
        hp_final = aplicar_dano(hp_rival, dano)
    except ValueError:
        return {"error": "valores inválidos", "hp_final": hp_rival}
    return {"dano": dano, "hp_final": hp_final}
