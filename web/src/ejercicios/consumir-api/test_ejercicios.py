"""🧪 Tests — Consumir una API"""
import importlib.util
import json
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"consumir_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_extraer_tipos():
    t = '{"name": "charizard", "tipos": ["fuego", "volador"]}'
    assert modulo.extraer_tipos(t) == ["fuego", "volador"]


def test_nombre_y_nivel():
    assert modulo.nombre_y_nivel('{"nombre": "Eevee", "nivel": 15}') == ("Eevee", 15)


def test_filtrar_por_tipo():
    t = '[{"nombre": "Charmander", "tipo": "Fuego"}, {"nombre": "Squirtle", "tipo": "Agua"}, {"nombre": "Vulpix", "tipo": "Fuego"}]'
    assert modulo.filtrar_por_tipo(t, "Fuego") == ["Charmander", "Vulpix"]


def test_manejar_respuesta():
    assert modulo.manejar_respuesta(200, '{"ok": 1}') == {"ok": 1}
    assert modulo.manejar_respuesta(404, '{"ok": 1}') is None


def test_contar_resultados():
    assert modulo.contar_resultados('{"results": [1, 2, 3, 4]}') == 4


def test_primer_resultado():
    t = '{"results": [{"name": "bulbasaur"}, {"name": "ivysaur"}]}'
    assert modulo.primer_resultado(t) == "bulbasaur"
