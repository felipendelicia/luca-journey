"""🧪 Tests — Scraping: extraer datos"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_scraping_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_extraer_numeros():
    assert modulo.extraer_numeros("Pikachu nivel 30, HP 100") == [30, 100]
    assert modulo.extraer_numeros("sin numeros") == []


def test_extraer_enlaces():
    assert modulo.extraer_enlaces('<a href="/kanto">K</a><a href="/johto">J</a>') == ["/kanto", "/johto"]


def test_entre_etiqueta():
    assert modulo.entre_etiqueta("<li>Bulbasaur</li><li>Charmander</li>", "li") == ["Bulbasaur", "Charmander"]


def test_sin_etiquetas():
    assert modulo.sin_etiquetas("<b>Hola</b> mundo") == "Hola mundo"
