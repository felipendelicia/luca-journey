"""🧪 Tests — Ordenar listas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_orden_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_indice_minimo():
    assert modulo.indice_minimo([30, 10, 20]) == 1
    assert modulo.indice_minimo([5]) == 0


def test_esta_ordenada():
    assert modulo.esta_ordenada([1, 2, 2, 3]) is True
    assert modulo.esta_ordenada([3, 1]) is False


def test_ordenar_burbuja():
    assert modulo.ordenar_burbuja([3, 1, 2]) == [1, 2, 3]
    assert modulo.ordenar_burbuja([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5]


def test_ordenar_seleccion():
    assert modulo.ordenar_seleccion([3, 1, 2]) == [1, 2, 3]
    assert modulo.ordenar_seleccion([]) == []


def test_ordenar_insercion():
    assert modulo.ordenar_insercion([3, 1, 2]) == [1, 2, 3]
    assert modulo.ordenar_insercion([]) == []


def test_ordenar_desc():
    assert modulo.ordenar_desc([1, 3, 2]) == [3, 2, 1]


def test_segundo_menor():
    assert modulo.segundo_menor([5, 1, 3]) == 3
    assert modulo.segundo_menor([9, 8]) == 9


def test_mediana():
    assert modulo.mediana([3, 1, 2]) == 2
    assert modulo.mediana([1, 2, 3, 4]) == 2.5


def test_top_n():
    assert modulo.top_n([4, 1, 7, 3], 2) == [7, 4]


def test_ordenar_por_longitud():
    assert modulo.ordenar_por_longitud(["onix", "pi", "eevee"]) == ["pi", "onix", "eevee"]


def test_mezclar_ordenadas():
    assert modulo.mezclar_ordenadas([1, 4], [2, 3, 5]) == [1, 2, 3, 4, 5]
    assert modulo.mezclar_ordenadas([], [1, 2]) == [1, 2]


def test_esta_ordenada_desc():
    assert modulo.esta_ordenada_desc([5, 3, 1]) is True
    assert modulo.esta_ordenada_desc([1, 2]) is False


def test_unicos_ordenados():
    assert modulo.unicos_ordenados([3, 1, 3, 2, 1]) == [1, 2, 3]


def test_invertir():
    assert modulo.invertir([1, 2, 3]) == [3, 2, 1]
    assert modulo.invertir([]) == []


def test_kesimo_menor():
    assert modulo.kesimo_menor([7, 3, 9, 1], 2) == 3
    assert modulo.kesimo_menor([7, 3, 9, 1], 1) == 1


def test_ordenar_absoluto():
    assert modulo.ordenar_absoluto([-5, 2, -1, 3]) == [-1, 2, 3, -5]


def test_contar_swaps_burbuja():
    assert modulo.contar_swaps_burbuja([2, 1]) == 1
    assert modulo.contar_swaps_burbuja([1, 2, 3]) == 0


def test_ordenar_por_clave():
    datos = [{"n": "A", "nv": 9}, {"n": "B", "nv": 3}]
    assert modulo.ordenar_por_clave(datos, "nv") == [{"n": "B", "nv": 3}, {"n": "A", "nv": 9}]


def test_podio():
    assert modulo.podio([4, 9, 1, 7, 2]) == [9, 7, 4]
    assert modulo.podio([5]) == [5]


def test_rango():
    assert modulo.rango([3, 9, 1]) == 8
