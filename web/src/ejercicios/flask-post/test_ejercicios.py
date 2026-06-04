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
