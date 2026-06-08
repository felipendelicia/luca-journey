"""🧪 Tests — Algoritmos sobre la Pokédex"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_proyecto_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_contar_tipos():
    assert modulo.contar_tipos([{"nombre": "a", "tipo": "agua"}, {"nombre": "b", "tipo": "agua"}]) == {"agua": 2}


def test_ordenar_por_nivel():
    r = modulo.ordenar_por_nivel([{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}])
    assert r == [{"nombre": "b", "nivel": 20}, {"nombre": "a", "nivel": 5}]


def test_buscar():
    assert modulo.buscar([{"nombre": "Pikachu"}], "Pikachu") == {"nombre": "Pikachu"}
    assert modulo.buscar([{"nombre": "Pikachu"}], "Onix") is None


def test_top_n():
    pokes = [{"nombre": "a", "nivel": 5}, {"nombre": "b", "nivel": 20}, {"nombre": "c", "nivel": 12}]
    assert modulo.top_n(pokes, 2) == ["b", "c"]


_P = [
    {"nombre": "pikachu", "tipo": "electrico", "nivel": 20},
    {"nombre": "onix", "tipo": "roca", "nivel": 12},
    {"nombre": "staryu", "tipo": "agua", "nivel": 18},
    {"nombre": "gyarados", "tipo": "agua", "nivel": 30},
]


def test_promedio_nivel():
    assert modulo.promedio_nivel(_P) == 20.0


def test_nivel_maximo():
    assert modulo.nivel_maximo(_P) == 30


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(_P)["nombre"] == "gyarados"


def test_filtrar_por_tipo():
    assert modulo.filtrar_por_tipo(_P, "agua") == [_P[2], _P[3]]


def test_nombres():
    assert modulo.nombres(_P) == ["pikachu", "onix", "staryu", "gyarados"]


def test_tipos_unicos():
    assert modulo.tipos_unicos(_P) == ["agua", "electrico", "roca"]


def test_existe():
    assert modulo.existe(_P, "onix") is True
    assert modulo.existe(_P, "mew") is False


def test_nivel_de():
    assert modulo.nivel_de(_P, "onix") == 12
    assert modulo.nivel_de(_P, "mew") is None, "Si no está, devolvé None"


def test_subir_nivel_todos():
    r = modulo.subir_nivel_todos([{"nombre": "a", "tipo": "x", "nivel": 5}], 3)
    assert r == [{"nombre": "a", "tipo": "x", "nivel": 8}]


def test_mas_de_nivel():
    assert modulo.mas_de_nivel(_P, 19) == [_P[0], _P[3]]


def test_agrupar_por_tipo():
    assert modulo.agrupar_por_tipo(_P) == {"electrico": ["pikachu"], "roca": ["onix"], "agua": ["staryu", "gyarados"]}


def test_ordenar_por_nombre():
    assert modulo.ordenar_por_nombre(_P) == ["gyarados", "onix", "pikachu", "staryu"]


def test_tipo_mas_comun():
    assert modulo.tipo_mas_comun(_P) == "agua"


def test_nivel_total():
    assert modulo.nivel_total(_P) == 80


def test_equipo_balanceado():
    assert modulo.equipo_balanceado(_P) is False
    assert modulo.equipo_balanceado(_P[:3]) is True


def test_contar():
    assert modulo.contar(_P) == 4
