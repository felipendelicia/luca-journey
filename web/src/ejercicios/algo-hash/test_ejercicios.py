"""🧪 Tests — Diccionarios y sets"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_hash_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_frecuencias():
    assert modulo.frecuencias(["a", "b", "a", "c", "a"]) == {"a": 3, "b": 1, "c": 1}
    assert modulo.frecuencias([]) == {}


def test_sin_duplicados():
    assert modulo.sin_duplicados([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_mas_comun():
    assert modulo.mas_comun(["a", "b", "a", "c"]) == "a"


def test_interseccion():
    assert modulo.interseccion([1, 2, 3, 4], [2, 4, 6]) == [2, 4]
    assert modulo.interseccion([1], [2]) == []


def test_union():
    assert modulo.union([1, 2], [2, 3]) == [1, 2, 3]


def test_diferencia():
    assert modulo.diferencia([1, 2, 3], [2]) == [1, 3]


def test_mismos_elementos():
    assert modulo.mismos_elementos([1, 2, 2], [2, 1]) is True
    assert modulo.mismos_elementos([1, 2], [1, 3]) is False


def test_unicos():
    assert modulo.unicos([3, 1, 3, 2, 1]) == [3, 1, 2]


def test_contar_distintos():
    assert modulo.contar_distintos([1, 1, 2, 3, 3]) == 3


def test_agrupar_por_inicial():
    assert modulo.agrupar_por_inicial(["pikachu", "onix", "pidgey"]) == {"p": ["pikachu", "pidgey"], "o": ["onix"]}


def test_invertir_dict():
    assert modulo.invertir_dict({"a": 1, "b": 2}) == {1: "a", 2: "b"}


def test_claves_con_valor():
    assert modulo.claves_con_valor({"a": 1, "b": 2, "c": 1}, 1) == ["a", "c"]


def test_suma_valores():
    assert modulo.suma_valores({"a": 10, "b": 5}) == 15


def test_clave_mayor_valor():
    assert modulo.clave_mayor_valor({"pikachu": 5, "onix": 12}) == "onix"


def test_combinar_conteos():
    assert modulo.combinar_conteos({"x": 1}, {"x": 2, "y": 5}) == {"x": 3, "y": 5}


def test_son_anagramas():
    assert modulo.son_anagramas("roma", "amor") is True
    assert modulo.son_anagramas("ash", "gary") is False


def test_faltantes():
    assert modulo.faltantes([1, 2, 3, 4], [2, 4]) == [1, 3]


def test_aparece_una_vez():
    assert modulo.aparece_una_vez([1, 2, 2, 3, 1, 4]) == [3, 4]


def test_tiene_todas():
    assert modulo.tiene_todas({"a": 1, "b": 2}, ["a", "b"]) is True
    assert modulo.tiene_todas({"a": 1}, ["a", "z"]) is False


def test_dos_mas_comunes():
    assert modulo.dos_mas_comunes([1, 1, 2, 2, 2, 3]) == [2, 1]
