# Integrador de Kalos — Sistema de batalla (solución de referencia).

class ErrorBatalla(Exception):
    pass

def crear_pokemon(nombre, nivel, hp):
    if not isinstance(nombre, str) or nombre == "":
        raise ErrorBatalla("Nombre inválido")
    if not (1 <= nivel <= 100):
        raise ErrorBatalla("Nivel fuera de rango")
    if hp <= 0:
        raise ErrorBatalla("HP inválido")
    return {"nombre": nombre.lower(), "nivel": nivel, "hp": hp}

def atacar(atacante, defensor, poder):
    if atacante is None or defensor is None:
        return None
    if poder <= 0:
        raise ErrorBatalla("Poder inválido")
    dano = max(0, atacante["nivel"] * poder // 10 - defensor["nivel"] // 5)
    nuevo_hp = max(0, defensor["hp"] - dano)
    return {"nombre": defensor["nombre"], "nivel": defensor["nivel"], "hp": nuevo_hp}

def hp_total(equipo):
    if equipo is None:
        return 0
    return sum(p["hp"] for p in equipo if "hp" in p)

def equipo_vivo(equipo):
    if not equipo:
        return False
    return any(p.get("hp", 0) > 0 for p in equipo)

def ronda(equipo_a, equipo_b, poder):
    if not equipo_a or not equipo_b:
        return {"error": "equipo inválido"}
    atacante = next((p for p in equipo_a if p.get("hp", 0) > 0), None)
    defensor = next((p for p in equipo_b if p.get("hp", 0) > 0), None)
    if atacante is None or defensor is None:
        return {"resultado": "sin combatientes"}
    try:
        hp_antes = defensor["hp"]
        nuevo_defensor = atacar(atacante, defensor, poder)
        return {
            "atacante": atacante["nombre"],
            "defensor": defensor["nombre"],
            "dano": hp_antes - nuevo_defensor["hp"],
            "hp_defensor": nuevo_defensor["hp"],
        }
    except ErrorBatalla:
        return {"error": "poder inválido"}

def verificar_sistema():
    poke = crear_pokemon("Pikachu", 25, 100)
    assert poke == {"nombre": "pikachu", "nivel": 25, "hp": 100}
    raised = False
    try:
        crear_pokemon("", 25, 100)
    except ErrorBatalla:
        raised = True
    assert raised
    assert atacar(None, poke, 4) is None
    assert hp_total([]) == 0
    assert equipo_vivo([]) is False
