"""🧪 Tests — Errores: try / except"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"tryexc_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_dividir_seguro():
    assert modulo.dividir_seguro(10, 2) == 5
    assert modulo.dividir_seguro(5, 0) is None


def test_a_entero():
    assert modulo.a_entero("42") == 42
    assert modulo.a_entero("pikachu") == 0


def test_elemento():
    assert modulo.elemento([10, 20, 30], 1) == 20
    assert modulo.elemento([10], 5) is None


def test_valor():
    assert modulo.valor({"nivel": 25}, "nivel") == 25
    assert modulo.valor({"nivel": 25}, "tipo") == "no encontrado"


def test_raiz_segura():
    assert modulo.raiz_segura(9) == 3.0
    assert modulo.raiz_segura(-4) is None, "Un número negativo no tiene raíz real: devolvé None"


def test_promedio_seguro():
    assert modulo.promedio_seguro([2, 4]) == 3.0
    assert modulo.promedio_seguro([]) == 0


def test_primer_elemento():
    assert modulo.primer_elemento([10, 20]) == 10
    assert modulo.primer_elemento([]) is None, "Con la lista vacía devolvé None"


def test_a_float_seguro():
    assert modulo.a_float_seguro("3.5") == 3.5
    assert modulo.a_float_seguro("pika") is None, "Si no se puede convertir, devolvé None"


def test_dividir_lista():
    assert modulo.dividir_lista([10, 20], 2) == [5.0, 10.0]
    assert modulo.dividir_lista([10], 0) is None, "Dividir por cero: devolvé None"


def test_buscar_indice():
    assert modulo.buscar_indice(["a", "b"], "b") == 1
    assert modulo.buscar_indice(["a"], "z") == -1


def test_convertir_todos():
    assert modulo.convertir_todos(["1", "x", "3"]) == [1, 0, 3]


def test_acceso_anidado():
    assert modulo.acceso_anidado({"a": {"b": 9}}, ["a", "b"]) == 9
    assert modulo.acceso_anidado({"a": {"b": 9}}, ["a", "z"]) is None, "Si falta una clave, devolvé None"


def test_dividir_o_mensaje():
    assert modulo.dividir_o_mensaje(6, 2) == 3.0
    assert modulo.dividir_o_mensaje(6, 0) == "no se puede dividir por cero"


def test_sumar_validos():
    assert modulo.sumar_validos(["10", "x", "5"]) == 15


def test_max_seguro():
    assert modulo.max_seguro([3, 9, 1]) == 9
    assert modulo.max_seguro([]) is None, "Con la lista vacía devolvé None"


def test_leer_o_cero():
    assert modulo.leer_o_cero({"hp": 35}, "hp") == 35
    assert modulo.leer_o_cero({}, "hp") == 0


def test_ejecutar_seguro():
    assert modulo.ejecutar_seguro(int, "42") == 42
    assert modulo.ejecutar_seguro(int, "pika") is None, "Si func tira error, devolvé None"


def test_cuantos_validos():
    assert modulo.cuantos_validos(["1", "x", "3", "y"]) == 2


def test_ultimo_elemento():
    assert modulo.ultimo_elemento([1, 2, 3]) == 3
    assert modulo.ultimo_elemento([]) is None


def test_a_entero_o():
    assert modulo.a_entero_o("42", 0) == 42
    assert modulo.a_entero_o("pika", -1) == -1
