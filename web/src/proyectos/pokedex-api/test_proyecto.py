import ejercicios


def test_listar_y_buscar():
    c = ejercicios.crear_app().test_client()
    r = c.get("/pokemon")
    assert r.status_code == 200
    lista = r.get_json()
    assert len(lista) == 6
    r2 = c.get("/pokemon/25")
    assert r2.status_code == 200
    assert r2.get_json() == {"id": 25, "nombre": "Pikachu", "tipo": "eléctrico", "nivel": 12}
    r404 = c.get("/pokemon/99")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no encontrado"}


def test_buscar_por_tipo():
    c = ejercicios.crear_app().test_client()
    r = c.get("/pokemon/tipo/agua")
    assert r.status_code == 200
    agua = r.get_json()
    assert len(agua) == 3
    nombres = [p["nombre"] for p in agua]
    assert "Squirtle" in nombres
    assert "Psyduck" in nombres
    assert "Magikarp" in nombres
    r2 = c.get("/pokemon/tipo/fantasma")
    assert r2.get_json() == []


def test_buscar_por_nombre():
    c = ejercicios.crear_app().test_client()
    r = c.get("/buscar?nombre=char")
    assert r.status_code == 200
    assert len(r.get_json()) == 1
    assert r.get_json()[0]["nombre"] == "Charmander"
    r2 = c.get("/buscar?nombre=zzz")
    assert r2.get_json() == []


def test_stats():
    c = ejercicios.crear_app().test_client()
    r = c.get("/stats")
    assert r.status_code == 200
    data = r.get_json()
    assert data["total"] == 6
    assert abs(data["nivel_promedio"] - (5 + 8 + 7 + 12 + 15 + 3) / 6) < 0.01
    assert "planta" in data["tipos"]
    assert "fuego" in data["tipos"]
    assert "agua" in data["tipos"]
    assert "eléctrico" in data["tipos"]
    assert len(data["tipos"]) == 4
