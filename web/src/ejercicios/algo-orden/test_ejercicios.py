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
