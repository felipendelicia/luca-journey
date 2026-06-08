"""🧪 Tests — Dividir trabajo (hilos)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_hilos_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_dividir():
    assert modulo.dividir([1, 2, 3, 4, 5, 6], 3) == [[1, 2], [3, 4], [5, 6]]
    assert modulo.dividir([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]


def test_tamano_chunk():
    assert modulo.tamano_chunk(10, 3) == 4
    assert modulo.tamano_chunk(9, 3) == 3


def test_cuantos_hilos():
    assert modulo.cuantos_hilos(10, 4) == 3
    assert modulo.cuantos_hilos(8, 4) == 2


def test_aplanar():
    assert modulo.aplanar([[1, 2], [3, 4], [5]]) == [1, 2, 3, 4, 5]


def test_cuantos_chunks():
    assert modulo.cuantos_chunks([1, 2, 3, 4, 5], 2) == 3
    assert modulo.cuantos_chunks([1, 2], 2) == 1


def test_chunk_n():
    assert modulo.chunk_n([1, 2, 3, 4, 5], 2, 1) == [3, 4]


def test_tamanos_chunks():
    assert modulo.tamanos_chunks([1, 2, 3, 4, 5], 2) == [2, 2, 1]


def test_ultimo_chunk():
    assert modulo.ultimo_chunk([1, 2, 3, 4, 5], 2) == [5]
    assert modulo.ultimo_chunk([], 2) == []


def test_tamano_por_hilo():
    assert modulo.tamano_por_hilo(10, 3) == 4
    assert modulo.tamano_por_hilo(9, 3) == 3


def test_chunk_mas_grande():
    assert modulo.chunk_mas_grande([[1], [2, 3, 4], [5, 6]]) == [2, 3, 4]


def test_total_items():
    assert modulo.total_items([[1], [2, 3]]) == 3


def test_balanceado():
    assert modulo.balanceado([[1, 2], [3, 4], [5]]) is True
    assert modulo.balanceado([[1], [2, 3, 4]]) is False


def test_dividir_en_n():
    assert modulo.dividir_en_n([1, 2, 3, 4, 5], 2) == [[1, 2, 3], [4, 5]]


def test_promedio_tamano():
    assert modulo.promedio_tamano([[1, 2], [3, 4]]) == 2.0


def test_chunks_no_vacios():
    assert modulo.chunks_no_vacios([[1], [], [2, 3]]) == [[1], [2, 3]]


def test_indice_de_chunk():
    assert modulo.indice_de_chunk([1, 2, 3, 4, 5], 2, 3) == 1
    assert modulo.indice_de_chunk([1, 2, 3, 4, 5], 2, 0) == 0


def test_cabe_en_chunks():
    assert modulo.cabe_en_chunks(10, 2, 5) is True
    assert modulo.cabe_en_chunks(10, 2, 3) is False


def test_asignar_round_robin():
    assert modulo.asignar_round_robin(["a", "b", "c"], 2) == {0: ["a", "c"], 1: ["b"]}


def test_primer_chunk():
    assert modulo.primer_chunk([1, 2, 3, 4], 2) == [1, 2]


def test_chunk_mas_chico():
    assert modulo.chunk_mas_chico([[1, 2], [3], [4, 5, 6]]) == [3]
