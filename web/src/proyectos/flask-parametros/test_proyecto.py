import ejercicios


def test_ruta_saludo():
    c = ejercicios.crear_app().test_client()
    r = c.get("/saludo/Ash")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "Hola, Ash!"
    r2 = c.get("/saludo/Misty")
    assert r2.get_data(as_text=True) == "Hola, Misty!"


def test_ruta_pokemon_id():
    c = ejercicios.crear_app().test_client()
    r = c.get("/pokemon/25")
    assert r.status_code == 200
    assert r.get_json() == {"nombre": "Pikachu", "tipo": "eléctrico"}
    r404 = c.get("/pokemon/999")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no encontrado"}


def test_ruta_buscar_tipo():
    c = ejercicios.crear_app().test_client()
    r = c.get("/buscar?tipo=fuego")
    assert r.status_code == 200
    nombres = r.get_json()
    assert sorted(nombres) == ["Charmander", "Torchic"]
    r2 = c.get("/buscar?tipo=planta")
    assert r2.get_json() == ["Bulbasaur"]
    r3 = c.get("/buscar?tipo=fantasma")
    assert r3.get_json() == []


def test_ruta_nivel():
    c = ejercicios.crear_app().test_client()
    r = c.get("/nivel/10/5")
    assert r.status_code == 200
    assert r.get_json() == {"nivel_final": 15}
    r2 = c.get("/nivel/50/20")
    assert r2.get_json() == {"nivel_final": 70}
