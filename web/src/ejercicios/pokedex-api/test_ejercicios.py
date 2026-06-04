"""🧪 Tests — Proyecto: Pokédex API"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"pokeapi_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_listar():
    r = cliente.get("/pokedex")
    assert r.status_code == 200
    assert len(r.get_json()) >= 4


def test_obtener():
    r = cliente.get("/pokedex/2")
    assert r.get_json()["nombre"] == "Charmander"


def test_obtener_404():
    r = cliente.get("/pokedex/999")
    assert r.status_code == 404


def test_buscar():
    r = cliente.get("/buscar?tipo=Fuego")
    nombres = [p["nombre"] for p in r.get_json()]
    assert nombres == ["Charmander", "Vulpix"]


def test_agregar():
    r = cliente.post("/pokedex", json={"id": 5, "nombre": "Pikachu", "tipo": "Electrico"})
    assert r.status_code == 201
    assert r.get_json()["nombre"] == "Pikachu"
