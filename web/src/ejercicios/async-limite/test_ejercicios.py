"""🧪 Tests — Límite de concurrencia"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_limite_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_por_lotes():
    assert modulo.por_lotes([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert modulo.por_lotes([], 2) == []


def test_cantidad_lotes():
    assert modulo.cantidad_lotes(5, 2) == 3
    assert modulo.cantidad_lotes(4, 2) == 2


def test_cabe():
    assert modulo.cabe(2, 3) is True
    assert modulo.cabe(3, 3) is False


def test_limitar():
    assert modulo.limitar([1, 2, 3, 4], 2) == [1, 2]
    assert modulo.limitar([1], 5) == [1]


def test_lugares_libres():
    assert modulo.lugares_libres(["a"], 3) == 2


def test_esta_al_limite():
    assert modulo.esta_al_limite(["a", "b", "c"], 3) is True
    assert modulo.esta_al_limite(["a"], 3) is False


def test_hay_lugar():
    assert modulo.hay_lugar(["a"], 3) is True
    assert modulo.hay_lugar(["a", "b", "c"], 3) is False


def test_agregar_si_cabe():
    assert modulo.agregar_si_cabe(["a"], "b", 3) == ["a", "b"]
    assert modulo.agregar_si_cabe(["a", "b", "c"], "d", 3) == ["a", "b", "c"]


def test_liberar():
    assert modulo.liberar(["a", "b"], "a") == ["b"]


def test_tomar_hasta():
    assert modulo.tomar_hasta(["a", "b", "c"], 2) == ["a", "b"]


def test_resto_despues_de():
    assert modulo.resto_despues_de(["a", "b", "c"], 2) == ["c"]


def test_cantidad_ultimo_lote():
    assert modulo.cantidad_ultimo_lote(10, 3) == 1
    assert modulo.cantidad_ultimo_lote(9, 3) == 3


def test_procesar_en_lotes():
    assert modulo.procesar_en_lotes([1, 2, 3], 2, lambda x: x * 10) == [10, 20, 30]


def test_rondas_necesarias():
    assert modulo.rondas_necesarias(10, 3) == 4
    assert modulo.rondas_necesarias(9, 3) == 3


def test_cabe_todo():
    assert modulo.cabe_todo(2, 3) is True
    assert modulo.cabe_todo(5, 3) is False


def test_ocupacion():
    assert modulo.ocupacion(["a", "b"], 4) == 0.5


def test_limitar_lista():
    assert modulo.limitar_lista([1, 2, 3, 4], 2) == [1, 2]


def test_sobran():
    assert modulo.sobran([1, 2, 3, 4], 2) == [3, 4]


def test_puede_agregar_n():
    assert modulo.puede_agregar_n(["a"], 2, 3) is True
    assert modulo.puede_agregar_n(["a"], 3, 3) is False


def test_cuantos_esperan():
    assert modulo.cuantos_esperan(10, 3) == 7
    assert modulo.cuantos_esperan(2, 3) == 0
