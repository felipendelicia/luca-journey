import ejercicios
import json


def _post_json(c, url, data):
    return c.post(url, data=json.dumps(data), content_type="application/json")


def test_registrar_y_listar():
    c = ejercicios.crear_app().test_client()
    r = _post_json(c, "/entrenadores", {"id": 1, "nombre": "Ash", "region": "kanto"})
    assert r.status_code == 201
    body = r.get_json()
    assert body["nombre"] == "Ash"
    assert body["region"] == "kanto"
    r2 = c.get("/entrenadores")
    assert r2.status_code == 200
    lista = r2.get_json()
    assert len(lista) == 1
    assert lista[0]["nombre"] == "Ash"


def test_obtener_y_borrar():
    c = ejercicios.crear_app().test_client()
    _post_json(c, "/entrenadores", {"id": 1, "nombre": "Ash", "region": "kanto"})
    r = c.get("/entrenadores/1")
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Ash"
    r404 = c.get("/entrenadores/99")
    assert r404.status_code == 404
    assert r404.get_json() == {"error": "no existe"}
    rd = c.delete("/entrenadores/1")
    assert rd.status_code == 200
    assert rd.get_json() == {"borrado": 1}
    assert c.get("/entrenadores").get_json() == []
    rd2 = c.delete("/entrenadores/99")
    assert rd2.status_code == 404


def test_buscar_por_region():
    c = ejercicios.crear_app().test_client()
    _post_json(c, "/entrenadores", {"id": 1, "nombre": "Ash", "region": "kanto"})
    _post_json(c, "/entrenadores", {"id": 2, "nombre": "May", "region": "hoenn"})
    r = c.get("/entrenadores/region/kanto")
    assert r.status_code == 200
    lista = r.get_json()
    assert len(lista) == 1
    assert lista[0]["nombre"] == "Ash"
    r2 = c.get("/entrenadores/region/johto")
    assert r2.get_json() == []


def test_equipo_y_stats():
    c = ejercicios.crear_app().test_client()
    _post_json(c, "/entrenadores", {"id": 1, "nombre": "Ash", "region": "kanto"})
    rp = _post_json(c, "/entrenadores/1/pokemon", {"nombre": "Pikachu", "nivel": 25})
    assert rp.status_code == 201
    assert rp.get_json() == {"nombre": "Pikachu", "nivel": 25}
    _post_json(c, "/entrenadores/1/pokemon", {"nombre": "Charizard", "nivel": 36})
    re = c.get("/entrenadores/1/pokemon")
    assert re.status_code == 200
    equipo = re.get_json()
    assert len(equipo) == 2
    rn = c.get("/entrenadores/1/nivel-total")
    assert rn.status_code == 200
    assert rn.get_json() == {"nivel_total": 61}
    r404 = c.get("/entrenadores/99/pokemon")
    assert r404.status_code == 404
