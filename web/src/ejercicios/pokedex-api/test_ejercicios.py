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


def _ej(ruta):
    return cliente.get(ruta).get_json()


def test_equipo_listar():
    assert len(_ej("/equipo")) == 4


def test_equipo_cantidad():
    assert _ej("/equipo-cantidad") == {"cantidad": 4}


def test_equipo_nombres():
    assert _ej("/equipo-nombres") == {"nombres": ["Pikachu", "Onix", "Staryu", "Gengar"]}


def test_equipo_tipos():
    assert _ej("/equipo-tipos") == {"tipos": ["Agua", "Electrico", "Fantasma", "Roca"]}


def test_equipo_de_tipo():
    assert _ej("/equipo-de-tipo/Agua") == [{"id": 3, "nombre": "Staryu", "tipo": "Agua"}]


def test_equipo_obtener():
    assert _ej("/equipo-id/2") == {"id": 2, "nombre": "Onix", "tipo": "Roca"}
    assert cliente.get("/equipo-id/99").status_code == 404


def test_equipo_contar_tipo():
    assert _ej("/equipo-contar-tipo/Agua") == {"cantidad": 1}


def test_equipo_primero():
    assert _ej("/equipo-primero") == {"id": 1, "nombre": "Pikachu", "tipo": "Electrico"}


def test_equipo_ultimo():
    assert _ej("/equipo-ultimo") == {"id": 4, "nombre": "Gengar", "tipo": "Fantasma"}


def test_equipo_existe():
    assert _ej("/equipo-existe/Onix") == {"existe": True}
    assert _ej("/equipo-existe/Mew") == {"existe": False}


def test_equipo_ordenado():
    assert _ej("/equipo-ordenado") == ["Gengar", "Onix", "Pikachu", "Staryu"]


def test_equipo_filtrar():
    assert cliente.post("/equipo-filtrar", json={"tipo": "Roca"}).get_json() == [{"id": 2, "nombre": "Onix", "tipo": "Roca"}]


def test_equipo_resumen():
    assert _ej("/equipo-resumen") == {"total": 4, "tipos": 4}


def test_equipo_ids():
    assert _ej("/equipo-ids") == {"ids": [1, 2, 3, 4]}


def test_equipo_buscar():
    assert _ej("/equipo-buscar/Staryu") == {"id": 3, "nombre": "Staryu", "tipo": "Agua"}
    assert cliente.get("/equipo-buscar/Xyz").status_code == 404


def test_equipo_tiene_tipo():
    assert _ej("/equipo-tiene-tipo/Roca") == {"hay": True}
    assert _ej("/equipo-tiene-tipo/Dragon") == {"hay": False}
