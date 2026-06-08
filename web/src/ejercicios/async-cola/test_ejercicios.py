"""🧪 Tests — Cola productor/consumidor"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_cola_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_encolar():
    assert modulo.encolar([1, 2], 3) == [1, 2, 3]
    assert modulo.encolar([], "a") == ["a"]


def test_desencolar():
    cola = [1, 2, 3]
    assert modulo.desencolar(cola) == 1
    assert cola == [2, 3]
    assert modulo.desencolar([]) is None


def test_siguiente():
    assert modulo.siguiente([1, 2, 3]) == 1
    assert modulo.siguiente([]) is None


def test_vaciar():
    cola = [1, 2, 3]
    assert modulo.vaciar(cola) == [1, 2, 3]
    assert cola == []


def test_tamano():
    assert modulo.tamano(["a", "b"]) == 2


def test_esta_vacia():
    assert modulo.esta_vacia([]) is True
    assert modulo.esta_vacia(["a"]) is False


def test_espacio_libre():
    assert modulo.espacio_libre(["a"], 3) == 2


def test_cabe():
    assert modulo.cabe(["a"], 3) is True
    assert modulo.cabe(["a", "b", "c"], 3) is False


def test_esta_llena():
    assert modulo.esta_llena(["a", "b", "c"], 3) is True
    assert modulo.esta_llena(["a"], 3) is False


def test_encolar_varios():
    assert modulo.encolar_varios(["a"], ["b", "c"]) == ["a", "b", "c"]


def test_desencolar_varios():
    assert modulo.desencolar_varios(["a", "b", "c"], 2) == ["a", "b"]
    assert modulo.desencolar_varios(["a"], 5) == ["a"]


def test_proximos():
    assert modulo.proximos(["a", "b", "c"], 2) == ["a", "b"]


def test_hay():
    assert modulo.hay(["a", "b"], "b") is True
    assert modulo.hay(["a"], "z") is False


def test_posicion():
    assert modulo.posicion(["a", "b", "c"], "c") == 3
    assert modulo.posicion(["a"], "z") == -1


def test_contar():
    assert modulo.contar(["a", "b", "a"], "a") == 2


def test_rotar():
    assert modulo.rotar(["a", "b", "c", "d"], 2) == ["c", "d", "a", "b"]


def test_dividir_en_lotes():
    assert modulo.dividir_en_lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]


def test_procesar_todos():
    assert modulo.procesar_todos([1, 2, 3], lambda x: x * 2) == [2, 4, 6]


def test_invertir_cola():
    assert modulo.invertir_cola(["a", "b", "c"]) == ["c", "b", "a"]


def test_mover_al_final():
    assert modulo.mover_al_final(["a", "b", "c"], "a") == ["b", "c", "a"]
