"""🧪 Tests — Flask: parámetros"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"flaskparam_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_pokemon():
    r = cliente.get("/pokemon/25")
    assert r.get_json() == {"id": 25}


def test_saludo():
    r = cliente.get("/saludo/Ash")
    assert r.get_data(as_text=True) == "Hola, Ash"


def test_buscar():
    r = cliente.get("/buscar?tipo=Fuego")
    assert r.get_json() == {"tipo": "Fuego"}


def test_doble():
    r = cliente.get("/doble/21")
    assert r.get_json() == {"resultado": 42}
