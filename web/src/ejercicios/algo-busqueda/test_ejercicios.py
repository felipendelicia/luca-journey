"""🧪 Tests — Búsqueda lineal y binaria"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_busqueda_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_busqueda_lineal():
    assert modulo.busqueda_lineal([10, 20, 30], 20) == 1
    assert modulo.busqueda_lineal([10], 99) == -1


def test_contiene():
    assert modulo.contiene([1, 2, 3], 2) is True
    assert modulo.contiene([1, 2, 3], 9) is False


def test_busqueda_binaria():
    assert modulo.busqueda_binaria([1, 3, 5, 7, 9], 7) == 3
    assert modulo.busqueda_binaria([1, 3, 5], 4) == -1
    assert modulo.busqueda_binaria([], 1) == -1


def test_primero_mayor():
    assert modulo.primero_mayor([1, 3, 5, 7], 4) == 5
    assert modulo.primero_mayor([1, 2], 9) is None


def test_cuenta_apariciones():
    assert modulo.cuenta_apariciones([1, 2, 2, 3, 2], 2) == 3
    assert modulo.cuenta_apariciones([1, 2, 3], 9) == 0


def test_indice_minimo():
    assert modulo.indice_minimo([30, 10, 20]) == 1
    assert modulo.indice_minimo([5]) == 0


def test_indice_maximo():
    assert modulo.indice_maximo([30, 10, 20]) == 0
    assert modulo.indice_maximo([1, 9, 9, 2]) == 1


def test_ultimo_indice():
    assert modulo.ultimo_indice([1, 2, 1, 3], 1) == 2
    assert modulo.ultimo_indice([1, 2, 3], 9) == -1


def test_todos_los_indices():
    assert modulo.todos_los_indices([5, 1, 5, 5], 5) == [0, 2, 3]
    assert modulo.todos_los_indices([1, 2], 9) == []


def test_primer_par():
    assert modulo.primer_par([3, 7, 4, 9]) == 4
    assert modulo.primer_par([1, 3, 5]) is None, "Si no hay pares, devolvé None"


def test_hay_repetidos():
    assert modulo.hay_repetidos([1, 2, 3, 2]) is True
    assert modulo.hay_repetidos([1, 2, 3]) is False


def test_primer_repetido():
    assert modulo.primer_repetido([1, 2, 3, 2, 1]) == 2
    assert modulo.primer_repetido([1, 2, 3]) is None, "Sin repetidos, devolvé None"


def test_dos_que_suman():
    assert modulo.dos_que_suman([2, 7, 4], 11) is True
    assert modulo.dos_que_suman([2, 7, 4], 100) is False


def test_mas_cercano():
    assert modulo.mas_cercano([1, 5, 9], 6) == 5
    assert modulo.mas_cercano([10, 20, 30], 21) == 20


def test_esta_ordenada():
    assert modulo.esta_ordenada([1, 2, 2, 5]) is True
    assert modulo.esta_ordenada([1, 3, 2]) is False


def test_cuantos_menores():
    assert modulo.cuantos_menores([1, 3, 5, 7], 5) == 2
    assert modulo.cuantos_menores([1, 2, 3], 0) == 0


def test_buscar_texto():
    assert modulo.buscar_texto("pikachu", "ka") == 2
    assert modulo.buscar_texto("pikachu", "zzz") == -1


def test_contar_en_rango():
    assert modulo.contar_en_rango([1, 5, 8, 10], 5, 9) == 2
    assert modulo.contar_en_rango([1, 2, 3], 10, 20) == 0


def test_interseccion():
    assert modulo.interseccion([1, 2, 3, 2], [2, 3, 9]) == [2, 3]
    assert modulo.interseccion([1, 2], [9]) == []


def test_posicion_para_insertar():
    assert modulo.posicion_para_insertar([1, 3, 5], 4) == 2
    assert modulo.posicion_para_insertar([1, 3, 5], 0) == 0
    assert modulo.posicion_para_insertar([1, 3, 5], 9) == 3
