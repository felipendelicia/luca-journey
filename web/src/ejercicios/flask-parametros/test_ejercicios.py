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


def _gj(ruta):
    return cliente.get(ruta).get_json()


def _gt(ruta):
    return cliente.get(ruta).get_data(as_text=True)


def test_triple():
    assert _gj("/triple/7") == {"resultado": 21}


def test_cuadrado():
    assert _gj("/cuadrado/5") == {"resultado": 25}


def test_eco():
    assert _gj("/eco/pikachu") == {"texto": "pikachu"}


def test_mayuscula():
    assert _gt("/mayuscula/pika") == "PIKA"


def test_largo():
    assert _gj("/largo/pikachu") == {"largo": 7}


def test_suma():
    assert _gj("/suma/3/4") == {"suma": 7}


def test_resta():
    assert _gj("/resta/10/4") == {"resta": 6}


def test_es_par():
    assert _gj("/es-par/4") == {"par": True}
    assert _gj("/es-par/5") == {"par": False}


def test_saludar():
    assert _gj("/saludar?nombre=Ash") == {"saludo": "Hola Ash"}


def test_nivel():
    assert _gj("/nivel?valor=25") == {"nivel": 25}


def test_repetir():
    assert _gj("/repetir/ab/3") == {"resultado": "ababab"}


def test_invertir():
    assert _gt("/invertir/pika") == "akip"


def test_rango():
    assert _gj("/rango/4") == {"numeros": [1, 2, 3, 4]}


def test_multiplicar():
    assert _gj("/multiplicar/6/7") == {"resultado": 42}


def test_inicial():
    assert _gt("/inicial/pikachu") == "p"


def test_negativo():
    assert _gj("/negativo/5") == {"resultado": -5}
