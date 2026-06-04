"""🧪 Tests — Flask: tu primera app"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"flaskapp_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))
cliente = modulo.app.test_client()


def test_inicio():
    r = cliente.get("/")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "¡Bienvenido a la Pokédex API!"


def test_ping():
    r = cliente.get("/ping")
    assert r.status_code == 200
    assert r.get_data(as_text=True) == "pong"


def test_hola():
    r = cliente.get("/hola")
    assert r.get_data(as_text=True) == "Hola, Entrenador"


def test_version():
    r = cliente.get("/version")
    assert r.get_data(as_text=True) == "1.0"
