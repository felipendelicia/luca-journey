import ejercicios


def test_efectividad():
    assert ejercicios.efectividad("agua", "fuego") == 2.0
    assert ejercicios.efectividad("fuego", "agua") == 0.5
    assert ejercicios.efectividad("electrico", "agua") == 2.0
    assert ejercicios.efectividad("normal", "normal") == 1.0
    assert ejercicios.efectividad("planta", "roca") == 1.0


def test_danio_base():
    assert ejercicios.danio_base(50, 40, 80) == 100
    assert ejercicios.danio_base(30, 60, 50) == 25
    assert ejercicios.danio_base(100, 50, 40) == 80


def test_danio_total():
    assert ejercicios.danio_total(50, 40, 80, "agua", "fuego") == 200
    assert ejercicios.danio_total(50, 40, 80, "fuego", "agua") == 50
    assert ejercicios.danio_total(50, 40, 80, "normal", "normal") == 100


def test_resultado_combate():
    atacante = {"nombre": "Pikachu",  "tipo": "electrico", "ataque": 55, "poder": 90, "hp": 100}
    defensor  = {"nombre": "Gyarados", "tipo": "agua",      "defensa": 79, "hp": 100}
    resultado = ejercicios.resultado_combate(atacante, defensor)
    assert resultado == "Pikachu derrota a Gyarados en 1 golpe(s)."

    atacante2 = {"nombre": "Charmander", "tipo": "fuego",   "ataque": 40, "poder": 60, "hp": 80}
    defensor2  = {"nombre": "Blastoise",  "tipo": "agua",   "defensa": 65, "hp": 200}
    resultado2 = ejercicios.resultado_combate(atacante2, defensor2)
    assert resultado2 == "Charmander derrota a Blastoise en 12 golpe(s)."
