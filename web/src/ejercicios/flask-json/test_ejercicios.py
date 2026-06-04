"""🧪 Tests — Flask: respuestas JSON"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"flaskjson_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_pokemon():
    r = cliente.get("/pokemon")
    assert r.status_code == 200
    assert r.get_json() == {"nombre": "Pikachu", "nivel": 25}


def test_equipo():
    r = cliente.get("/equipo")
    assert r.get_json() == ["Pikachu", "Charizard", "Snorlax"]


def test_stats():
    r = cliente.get("/stats")
    assert r.get_json() == {"ataque": 55, "defensa": 40, "velocidad": 90}


def test_cantidad():
    r = cliente.get("/cantidad")
    assert r.get_json() == {"total": 151}
