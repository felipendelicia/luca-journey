"""🧪 Tests — Automatizador (bot)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_bot_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_normalizar():
    assert modulo.normalizar("  Pikachu ") == "pikachu"


def test_filtrar_nivel():
    pokes = [{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}]
    assert modulo.filtrar_nivel(pokes, 10) == [{"nombre": "b", "nivel": 20}]
    assert modulo.filtrar_nivel(pokes, 100) == []


def test_agrupar_por_tipo():
    pokes = [{"nombre": "Squirtle", "tipo": "agua"}, {"nombre": "Charmander", "tipo": "fuego"}, {"nombre": "Psyduck", "tipo": "agua"}]
    assert modulo.agrupar_por_tipo(pokes) == {"agua": ["Squirtle", "Psyduck"], "fuego": ["Charmander"]}


def test_contar():
    assert modulo.contar([{"nombre": "a"}, {"nombre": "b"}]) == 2
    assert modulo.contar([]) == 0


_PB = [
    {"nombre": "Pikachu", "tipo": "electrico", "nivel": 20},
    {"nombre": "Squirtle", "tipo": "agua", "nivel": 12},
    {"nombre": "Psyduck", "tipo": "agua", "nivel": 30},
]


def test_normalizar_lista():
    assert modulo.normalizar_lista(["  Pikachu", "ONIX "]) == ["pikachu", "onix"]


def test_quitar_duplicados():
    assert modulo.quitar_duplicados(["a", "b", "a"]) == ["a", "b"]


def test_solo_nombres():
    assert modulo.solo_nombres(_PB) == ["Pikachu", "Squirtle", "Psyduck"]


def test_ordenar_por_nivel():
    assert modulo.ordenar_por_nivel(_PB)[0]["nombre"] == "Psyduck"


def test_el_de_mayor_nivel():
    assert modulo.el_de_mayor_nivel(_PB)["nombre"] == "Psyduck"


def test_nivel_promedio():
    assert modulo.nivel_promedio([{"nivel": 10}, {"nivel": 20}]) == 15.0


def test_tipos_unicos():
    assert modulo.tipos_unicos(_PB) == ["agua", "electrico"]


def test_filtrar_tipo():
    assert modulo.filtrar_tipo(_PB, "agua") == [_PB[1], _PB[2]]


def test_subir_nivel():
    r = modulo.subir_nivel([{"nombre": "a", "tipo": "x", "nivel": 5}], 3)
    assert r == [{"nombre": "a", "tipo": "x", "nivel": 8}]


def test_contar_por_tipo():
    assert modulo.contar_por_tipo(_PB) == {"electrico": 1, "agua": 2}


def test_nombres_filtrados():
    assert modulo.nombres_filtrados(_PB, 15) == ["Pikachu", "Psyduck"]


def test_existe():
    assert modulo.existe(_PB, "  pikachu ") is True
    assert modulo.existe(_PB, "mew") is False


def test_buscar():
    assert modulo.buscar(_PB, "PSYDUCK")["nivel"] == 30
    assert modulo.buscar(_PB, "mew") is None, "Si no está, devolvé None"


def test_nivel_total():
    assert modulo.nivel_total(_PB) == 62


def test_mapear_nombres():
    assert modulo.mapear_nombres([{"nombre": "abc"}], str.upper) == ["ABC"]


def test_agregar_slug():
    r = modulo.agregar_slug([{"nombre": "  Pikachu "}])
    assert r[0]["slug"] == "pikachu"
