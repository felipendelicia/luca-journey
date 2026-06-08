"""🧪 Tests — Flask: métodos y POST"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"flaskpost_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_eco():
    r = cliente.post("/eco", json={"x": 1, "y": 2})
    assert r.get_json() == {"x": 1, "y": 2}


def test_sumar():
    r = cliente.post("/sumar", json={"a": 2, "b": 3})
    assert r.get_json() == {"suma": 5}


def test_crear():
    r = cliente.post("/crear", json={"nombre": "Mew"})
    assert r.status_code == 201
    assert r.get_json() == {"creado": "Mew"}


def _p(ruta, datos):
    return cliente.post(ruta, json=datos).get_json()


def test_multiplicar():
    assert _p("/multiplicar", {"a": 6, "b": 7}) == {"producto": 42}


def test_restar():
    assert _p("/restar", {"a": 10, "b": 4}) == {"resta": 6}


def test_saludar():
    assert _p("/saludar", {"nombre": "Ash"}) == {"mensaje": "Hola Ash"}


def test_mayuscula():
    assert _p("/mayuscula", {"texto": "pika"}) == {"texto": "PIKA"}


def test_largo():
    assert _p("/largo", {"texto": "pikachu"}) == {"largo": 7}


def test_promedio():
    assert _p("/promedio", {"numeros": [2, 4, 6]}) == {"promedio": 4.0}


def test_maximo():
    assert _p("/maximo", {"numeros": [3, 9, 1]}) == {"maximo": 9}


def test_contar():
    assert _p("/contar", {"items": [1, 2, 3]}) == {"cantidad": 3}


def test_invertir():
    assert _p("/invertir", {"texto": "pika"}) == {"resultado": "akip"}


def test_sumar_lista():
    assert _p("/sumar-lista", {"numeros": [1, 2, 3]}) == {"suma": 6}


def test_validar():
    assert _p("/validar", {"nivel": 50}) == {"valido": True}
    assert _p("/validar", {"nivel": 200}) == {"valido": False}


def test_crear_pokemon():
    r = cliente.post("/crear-pokemon", json={"nombre": "Mew", "tipo": "psiquico"})
    assert r.status_code == 201
    assert r.get_json() == {"pokemon": {"nombre": "Mew", "tipo": "psiquico"}}


def test_duplicar():
    assert _p("/duplicar", {"valor": 21}) == {"resultado": 42}


def test_concatenar():
    assert _p("/concatenar", {"a": "pika", "b": "chu"}) == {"resultado": "pikachu"}


def test_es_mayor():
    assert _p("/es-mayor", {"a": 9, "b": 3}) == {"mayor": True}
    assert _p("/es-mayor", {"a": 3, "b": 9}) == {"mayor": False}


def test_borrar():
    assert _p("/borrar", {"id": 25}) == {"borrado": 25}


def test_tipos_unicos():
    assert _p("/tipos-unicos", {"tipos": ["agua", "fuego", "agua"]}) == {"tipos": ["agua", "fuego"]}
