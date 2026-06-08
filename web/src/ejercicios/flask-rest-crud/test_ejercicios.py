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


def _cj(ruta):
    return cliente.get(ruta).get_json()


def test_cat_listar():
    assert _cj("/catalogo") == [{"id": 10, "nombre": "Mew"}, {"id": 11, "nombre": "Mewtwo"}, {"id": 12, "nombre": "Ditto"}]


def test_cat_cantidad():
    assert _cj("/catalogo-cantidad") == {"cantidad": 3}


def test_cat_nombres():
    assert _cj("/catalogo-nombres") == {"nombres": ["Mew", "Mewtwo", "Ditto"]}


def test_cat_ids():
    assert _cj("/catalogo-ids") == {"ids": [10, 11, 12]}


def test_cat_obtener():
    assert _cj("/catalogo-id/11") == {"id": 11, "nombre": "Mewtwo"}
    assert cliente.get("/catalogo-id/99").status_code == 404


def test_cat_existe():
    assert _cj("/catalogo-existe/10") == {"existe": True}
    assert _cj("/catalogo-existe/99") == {"existe": False}


def test_cat_primero():
    assert _cj("/catalogo-primero") == {"id": 10, "nombre": "Mew"}


def test_cat_ultimo():
    assert _cj("/catalogo-ultimo") == {"id": 12, "nombre": "Ditto"}


def test_cat_buscar():
    assert _cj("/catalogo-buscar/Ditto") == {"id": 12, "nombre": "Ditto"}
    assert cliente.get("/catalogo-buscar/Xyz").status_code == 404


def test_cat_ordenado():
    assert _cj("/catalogo-ordenado") == ["Ditto", "Mew", "Mewtwo"]


def test_cat_maxid():
    assert _cj("/catalogo-maxid") == {"max": 12}


def test_cat_minid():
    assert _cj("/catalogo-minid") == {"min": 10}


def test_cat_contar():
    assert cliente.post("/catalogo-contar", json={"ids": [1, 2, 3]}).get_json() == {"cantidad": 3}


def test_cat_filtrar():
    assert _cj("/catalogo-filtrar/11") == {"ids": [11, 12]}


def test_cat_resumen():
    assert _cj("/catalogo-resumen") == {"total": 3, "primero": "Mew"}


def test_cat_vacio():
    assert _cj("/catalogo-vacio") == {"vacio": False}
