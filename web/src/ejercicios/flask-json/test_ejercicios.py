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


def _json(ruta):
    return cliente.get(ruta).get_json()


def test_tipos_json():
    assert _json("/tipos-json") == ["fuego", "agua", "planta"]


def test_info():
    assert _json("/info") == {"region": "Kanto", "total": 151}


def test_pikachu_info():
    assert _json("/pikachu") == {"nombre": "Pikachu", "tipo": "electrico", "nivel": 25}


def test_numeros():
    assert _json("/numeros") == [1, 2, 3, 4, 5]


def test_vacio():
    assert _json("/vacio") == {}


def test_lista_vacia():
    assert _json("/lista-vacia") == []


def test_booleano():
    assert _json("/booleano") == {"activo": True}


def test_anidado():
    assert _json("/anidado") == {"pokemon": {"nombre": "Pikachu", "stats": {"hp": 35}}}


def test_entrenador():
    assert _json("/entrenador") == {"nombre": "Ash", "medallas": 8}


def test_tipos_conteo():
    assert _json("/tipos-conteo") == {"agua": 32, "fuego": 12}


def test_version_json():
    assert _json("/version-json") == {"version": "1.0", "estable": True}


def test_coordenadas():
    assert _json("/coordenadas") == [10, 20]


def test_mensaje():
    assert _json("/mensaje") == {"mensaje": "Hola"}


def test_precios():
    assert _json("/precios") == {"pocion": 200, "revivir": 1500}


def test_equipo_completo():
    assert _json("/equipo-completo") == [{"nombre": "Pikachu"}, {"nombre": "Onix"}]


def test_estado_json():
    assert _json("/estado-json") == {"status": "ok", "codigo": 200}
