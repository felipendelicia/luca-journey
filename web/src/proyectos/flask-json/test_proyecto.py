import ejercicios


def test_ruta_pokemon():
    c = ejercicios.crear_app().test_client()
    r = c.get("/pokemon")
    assert r.status_code == 200
    assert r.get_json() == {"nombre": "Voltorb", "tipo": "eléctrico", "nivel": 20}


def test_ruta_equipo():
    c = ejercicios.crear_app().test_client()
    r = c.get("/equipo")
    assert r.get_json() == ["Voltorb", "Electrode", "Magneton"]


def test_ruta_stats():
    c = ejercicios.crear_app().test_client()
    r = c.get("/stats")
    assert r.get_json() == {"ataque": 55, "defensa": 40, "velocidad": 90}


def test_ruta_info():
    c = ejercicios.crear_app().test_client()
    r = c.get("/info")
    assert r.get_json() == {"region": "Hoenn", "gimnasio": 3, "tipo": "eléctrico"}
