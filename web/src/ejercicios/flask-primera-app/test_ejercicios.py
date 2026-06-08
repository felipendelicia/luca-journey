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


def _txt(ruta):
    return cliente.get(ruta).get_data(as_text=True)


def test_estado():
    assert _txt("/estado") == "activo"


def test_autor():
    assert _txt("/autor") == "Profesor Oak"


def test_region():
    assert _txt("/region") == "Kanto"


def test_total():
    assert _txt("/total") == "151"


def test_salud():
    assert _txt("/salud") == "OK"


def test_creador():
    assert _txt("/creador") == "Ash Ketchum"


def test_api():
    assert _txt("/api") == "Pokedex API v1"


def test_ayuda():
    assert _txt("/ayuda") == "Usa /pokemon"


def test_tipos():
    assert _txt("/tipos") == "fuego, agua, planta"


def test_destacado():
    assert _txt("/destacado") == "Pikachu"


def test_contacto():
    assert _txt("/contacto") == "oak@kanto.com"


def test_horario():
    assert _txt("/horario") == "9 a 18"


def test_reglas():
    assert _txt("/reglas") == "Atrapalos a todos"


def test_lema():
    assert _txt("/lema") == "Hazte con todos"


def test_numero():
    assert _txt("/numero") == "25"


def test_servidor():
    assert _txt("/servidor") == "online"
