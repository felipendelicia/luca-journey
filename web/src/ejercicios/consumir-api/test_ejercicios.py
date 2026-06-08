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


_J = '[{"nombre": "pikachu", "tipo": "electrico", "nivel": 25}, {"nombre": "onix", "tipo": "roca", "nivel": 12}, {"nombre": "staryu", "tipo": "agua", "nivel": 30}]'


def test_ultimo_resultado():
    assert modulo.ultimo_resultado(_J)["nombre"] == "staryu"
    assert modulo.ultimo_resultado("[]") is None


def test_nombres_de():
    assert modulo.nombres_de(_J) == ["pikachu", "onix", "staryu"]


def test_ordenar_por_nivel():
    assert modulo.ordenar_por_nivel(_J) == ["staryu", "pikachu", "onix"]


def test_promedio_nivel():
    assert modulo.promedio_nivel(_J) == (25 + 12 + 30) / 3


def test_mas_fuerte():
    assert modulo.mas_fuerte(_J) == "staryu"


def test_existe():
    assert modulo.existe(_J, "onix") is True
    assert modulo.existe(_J, "mew") is False


def test_buscar():
    assert modulo.buscar(_J, "onix")["nivel"] == 12
    assert modulo.buscar(_J, "mew") is None


def test_tipos_unicos():
    assert modulo.tipos_unicos(_J) == ["agua", "electrico", "roca"]


def test_contar_por_tipo():
    assert modulo.contar_por_tipo(_J) == {"electrico": 1, "roca": 1, "agua": 1}


def test_filtrar_nivel_minimo():
    assert modulo.filtrar_nivel_minimo(_J, 20) == ["pikachu", "staryu"]


def test_hay_resultados():
    assert modulo.hay_resultados(_J) is True
    assert modulo.hay_resultados("[]") is False


def test_nombres_de_tipo():
    assert modulo.nombres_de_tipo(_J, "agua") == ["staryu"]


def test_nivel_de():
    assert modulo.nivel_de(_J, "pikachu") == 25
    assert modulo.nivel_de(_J, "mew") is None


def test_resumen():
    assert modulo.resumen(_J) == {"total": 3, "tipos": 3}
