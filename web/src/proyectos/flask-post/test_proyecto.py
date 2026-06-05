import ejercicios
import json


def test_ruta_eco():
    c = ejercicios.crear_app().test_client()
    payload = {"saludo": "Hola"}
    r = c.post("/eco", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 200
    assert r.get_json() == payload


def test_ruta_registrar():
    c = ejercicios.crear_app().test_client()
    r = c.post("/registrar", data=json.dumps({"nombre": "Vigoroth", "nivel": 28}), content_type="application/json")
    assert r.status_code == 201
    assert r.get_json() == {"registrado": "Vigoroth", "nivel": 28}


def test_ruta_sumar_niveles():
    c = ejercicios.crear_app().test_client()
    r = c.post("/sumar-niveles", data=json.dumps({"niveles": [10, 20, 30]}), content_type="application/json")
    assert r.status_code == 200
    assert r.get_json() == {"total": 60}
    r2 = c.post("/sumar-niveles", data=json.dumps({"niveles": [5]}), content_type="application/json")
    assert r2.get_json() == {"total": 5}


def test_ruta_tipo_fuerte():
    c = ejercicios.crear_app().test_client()
    payload = {"equipo": [{"nombre": "Slaking", "nivel": 36}, {"nombre": "Vigoroth", "nivel": 28}]}
    r = c.post("/tipo-fuerte", data=json.dumps(payload), content_type="application/json")
    assert r.status_code == 200
    assert r.get_json() == {"mas_fuerte": "Slaking"}
