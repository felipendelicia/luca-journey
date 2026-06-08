"""🧪 Tests — Juntar resultados (gather)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_gather_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_combinar():
    assert modulo.combinar([("pikachu", 100), ("onix", 80)]) == {"pikachu": 100, "onix": 80}
    assert modulo.combinar([]) == {}


def test_en_orden():
    assert modulo.en_orden(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def test_todos_ok():
    assert modulo.todos_ok([1, 2, 3]) is True
    assert modulo.todos_ok([1, None, 3]) is False


def test_primer_error():
    assert modulo.primer_error([1, None, 3]) == 1
    assert modulo.primer_error([1, 2]) == -1


def test_cuantos_ok():
    assert modulo.cuantos_ok([1, None, 3]) == 2


def test_cuantos_error():
    assert modulo.cuantos_error([1, None, 3, None]) == 2


def test_solo_ok():
    assert modulo.solo_ok([1, None, 3]) == [1, 3]


def test_emparejar():
    assert modulo.emparejar(["a", "b"], [1, 2]) == {"a": 1, "b": 2}


def test_primer_ok():
    assert modulo.primer_ok([None, 5, 7]) == 5
    assert modulo.primer_ok([None, None]) is None, "Si todos fallaron, devolvé None"


def test_ultimo_ok():
    assert modulo.ultimo_ok([1, None, 7, None]) == 7
    assert modulo.ultimo_ok([None]) is None


def test_reemplazar_errores():
    assert modulo.reemplazar_errores([1, None, 3], 0) == [1, 0, 3]


def test_hay_error():
    assert modulo.hay_error([1, None]) is True
    assert modulo.hay_error([1, 2]) is False


def test_indice_primer_error():
    assert modulo.indice_primer_error([1, None, 3]) == 1
    assert modulo.indice_primer_error([1, 2]) == -1


def test_suma_ok():
    assert modulo.suma_ok([1, None, 3]) == 4


def test_promedio_ok():
    assert modulo.promedio_ok([2, None, 4]) == 3.0
    assert modulo.promedio_ok([None, None]) == 0


def test_ordenar_ok():
    assert modulo.ordenar_ok([3, None, 1, 2]) == [1, 2, 3]


def test_max_ok():
    assert modulo.max_ok([1, None, 9, 3]) == 9
    assert modulo.max_ok([None]) is None


def test_todos_fallaron():
    assert modulo.todos_fallaron([None, None]) is True
    assert modulo.todos_fallaron([None, 1]) is False


def test_con_indice():
    assert modulo.con_indice(["a", "b"]) == [(0, "a"), (1, "b")]


def test_contar_valores():
    assert modulo.contar_valores([1, 1, None, 2]) == {1: 2, 2: 1}
