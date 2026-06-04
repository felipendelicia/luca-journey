"""🧪 Tests — APIs: HTTP y JSON"""
import importlib.util
import json
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"apijson_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_a_json():
    r = modulo.a_json({"nombre": "Pikachu"})
    assert isinstance(r, str)
    assert json.loads(r) == {"nombre": "Pikachu"}


def test_de_json():
    assert modulo.de_json('{"nivel": 25}') == {"nivel": 25}


def test_extraer_nombre():
    assert modulo.extraer_nombre('{"nombre": "Charizard", "nivel": 90}') == "Charizard"


def test_es_exito():
    assert modulo.es_exito(200) is True
    assert modulo.es_exito(201) is True
    assert modulo.es_exito(404) is False
    assert modulo.es_exito(500) is False


def test_armar_respuesta():
    assert modulo.armar_respuesta("Eevee", 15) == {"nombre": "Eevee", "nivel": 15}


def test_nombres():
    t = '[{"nombre": "Pikachu"}, {"nombre": "Eevee"}]'
    assert modulo.nombres(t) == ["Pikachu", "Eevee"]


def test_total_niveles():
    t = '[{"nivel": 25}, {"nivel": 90}, {"nivel": 12}]'
    assert modulo.total_niveles(t) == 127
