"""🧪 Tests — Repartir tareas"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_tareas_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_repartir():
    assert modulo.repartir([1, 2, 3, 4, 5], 2) == [[1, 3, 5], [2, 4]]
    assert modulo.repartir([1, 2, 3], 3) == [[1], [2], [3]]


def test_carga_de():
    assert modulo.carga_de([[1, 3, 5], [2, 4]]) == [3, 2]


def test_worker_libre():
    assert modulo.worker_libre([3, 1, 2]) == 1
    assert modulo.worker_libre([2, 2, 2]) == 0


def test_equilibrado():
    assert modulo.equilibrado([[1, 3], [2, 4]]) is True
    assert modulo.equilibrado([[1, 2, 3], [4]]) is False


def test_total_tareas():
    assert modulo.total_tareas([["a"], ["b", "c"]]) == 3


def test_cargas():
    assert modulo.cargas([["a"], ["b", "c"]]) == [1, 2]


def test_mas_cargado():
    assert modulo.mas_cargado([["a"], ["b", "c"]]) == 1


def test_menos_cargado():
    assert modulo.menos_cargado([["a", "x"], ["b"]]) == 1


def test_promedio_carga():
    assert modulo.promedio_carga([["a"], ["b", "c"]]) == 1.5


def test_diferencia_carga():
    assert modulo.diferencia_carga([["a"], ["b", "c", "d"]]) == 2


def test_repartir_round_robin():
    assert modulo.repartir_round_robin(["a", "b", "c"], 2) == [["a", "c"], ["b"]]


def test_agregar_a_menos_cargado():
    assert modulo.agregar_a_menos_cargado([["a", "b"], ["c"]], "z") == [["a", "b"], ["c", "z"]]


def test_todas_las_tareas():
    assert modulo.todas_las_tareas([["a"], ["b", "c"]]) == ["a", "b", "c"]


def test_quien_tiene():
    assert modulo.quien_tiene([["a"], ["b", "c"]], "c") == 1
    assert modulo.quien_tiene([["a"]], "z") == -1


def test_tareas_de():
    assert modulo.tareas_de([["a"], ["b", "c"]], 1) == ["b", "c"]


def test_cantidad_workers():
    assert modulo.cantidad_workers([["a"], ["b"], []]) == 3


def test_hay_vacio():
    assert modulo.hay_vacio([["a"], []]) is True
    assert modulo.hay_vacio([["a"], ["b"]]) is False


def test_mover_una():
    assert modulo.mover_una([["a", "b"], ["c"]], 0, 1) == [["b"], ["c", "a"]]


def test_estan_equilibrados():
    assert modulo.estan_equilibrados([["a"], ["b"]]) is True
    assert modulo.estan_equilibrados([["a"], ["b", "c", "d"]]) is False


def test_worker_mas_grande():
    assert modulo.worker_mas_grande([["a"], ["b", "c"]]) == ["b", "c"]
