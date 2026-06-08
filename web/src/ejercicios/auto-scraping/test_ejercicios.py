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


def test_extraer_emails():
    assert modulo.extraer_emails("escribi a ash@kanto.com") == ["ash@kanto.com"]


def test_extraer_precios():
    assert modulo.extraer_precios("Pocion $200, Revivir $1500") == [200, 1500]


def test_contar_etiquetas():
    assert modulo.contar_etiquetas("<li>a</li><li>b</li>", "li") == 2


def test_primer_enlace():
    assert modulo.primer_enlace('<a href="/kanto">K</a>') == "/kanto"
    assert modulo.primer_enlace("<p>sin enlaces</p>") is None, "Sin enlaces, devolvé None"


def test_tiene_etiqueta():
    assert modulo.tiene_etiqueta("<li>a</li>", "li") is True
    assert modulo.tiene_etiqueta("<p>a</p>", "li") is False


def test_contar_enlaces():
    assert modulo.contar_enlaces('<a href="/a">A</a><a href="/b">B</a>') == 2


def test_extraer_hashtags():
    assert modulo.extraer_hashtags("hoy #kanto y #pokemon") == ["kanto", "pokemon"]


def test_extraer_mayusculas():
    assert modulo.extraer_mayusculas("el TEAM ROCKET ataca") == ["TEAM", "ROCKET"]


def test_contar_palabras():
    assert modulo.contar_palabras("atrapalos a todos") == 3


def test_extraer_entre():
    assert modulo.extraer_entre("[a] y [b]", "[", "]") == ["a", "b"]


def test_primer_numero():
    assert modulo.primer_numero("nivel 30 hp 100") == 30
    assert modulo.primer_numero("sin numeros") is None


def test_suma_numeros():
    assert modulo.suma_numeros("3 pokemon y 2 pociones") == 5


def test_quitar_espacios_extra():
    assert modulo.quitar_espacios_extra("  hola   mundo  ") == "hola mundo"


def test_solo_letras():
    assert modulo.solo_letras("Pika-2!") == "Pika"


def test_ultimo_enlace():
    assert modulo.ultimo_enlace('<a href="/a">A</a><a href="/b">B</a>') == "/b"
    assert modulo.ultimo_enlace("<p>x</p>") is None


def test_reemplazar_texto():
    assert modulo.reemplazar_texto("hola hola", "hola", "chau") == "chau chau"
