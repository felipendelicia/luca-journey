"""🧪 Tests — Flask: API REST (CRUD)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"flaskcrud_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_listar():
    r = cliente.get("/pokedex")
    assert r.status_code == 200
    datos = r.get_json()
    assert isinstance(datos, list) and len(datos) >= 3
    assert datos[0]["nombre"] == "Bulbasaur"


def test_obtener():
    r = cliente.get("/pokedex/2")
    assert r.status_code == 200
    assert r.get_json()["nombre"] == "Charmander"


def test_obtener_no_existe():
    r = cliente.get("/pokedex/999")
    assert r.status_code == 404
    assert r.get_json() == {"error": "no existe"}


def test_agregar():
    r = cliente.post("/pokedex", json={"id": 4, "nombre": "Pikachu"})
    assert r.status_code == 201
    assert r.get_json() == {"id": 4, "nombre": "Pikachu"}


def test_borrar():
    r = cliente.delete("/pokedex/1")
    assert r.status_code == 200
    assert r.get_json() == {"borrado": 1}


def test_borrar_no_existe():
    r = cliente.delete("/pokedex/999")
    assert r.status_code == 404
