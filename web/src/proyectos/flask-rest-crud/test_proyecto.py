import ejercicios
import json


def test_listar_y_obtener():
    c = ejercicios.crear_app().test_client()
    r = c.get("/pokemon")
    assert r.status_code == 200
    assert r.get_json() == []
    r404 = c.get("/pokemon/1")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no existe"}


def test_crear():
    c = ejercicios.crear_app().test_client()
    r = c.post("/pokemon", data=json.dumps({"id": 1, "nombre": "Swablu"}), content_type="application/json")
    assert r.status_code == 201
    assert r.get_json() == {"id": 1, "nombre": "Swablu"}
    r2 = c.get("/pokemon")
    assert r2.get_json() == [{"id": 1, "nombre": "Swablu"}]
    r3 = c.get("/pokemon/1")
    assert r3.status_code == 200
    assert r3.get_json() == {"id": 1, "nombre": "Swablu"}


def test_borrar():
    c = ejercicios.crear_app().test_client()
    c.post("/pokemon", data=json.dumps({"id": 1, "nombre": "Swablu"}), content_type="application/json")
    r = c.delete("/pokemon/1")
    assert r.status_code == 200
    assert r.get_json() == {"borrado": 1}
    r2 = c.get("/pokemon")
    assert r2.get_json() == []
    r404 = c.delete("/pokemon/99")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no existe"}


def test_actualizar():
    c = ejercicios.crear_app().test_client()
    c.post("/pokemon", data=json.dumps({"id": 1, "nombre": "Swablu"}), content_type="application/json")
    r = c.put("/pokemon/1", data=json.dumps({"id": 1, "nombre": "Altaria"}), content_type="application/json")
    assert r.status_code == 200
    assert r.get_json() == {"id": 1, "nombre": "Altaria"}
    r404 = c.put("/pokemon/99", data=json.dumps({"id": 99}), content_type="application/json")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no existe"}
