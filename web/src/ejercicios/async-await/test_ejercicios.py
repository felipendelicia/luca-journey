"""🧪 Tests — await: dónde esperar"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_await_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_necesita_await():
    assert modulo.necesita_await({"nombre": "bajar", "espera": True}) is True
    assert modulo.necesita_await({"nombre": "sumar", "espera": False}) is False


def test_pasos_con_await():
    pasos = [{"nombre": "bajar", "espera": True}, {"nombre": "sumar", "espera": False}, {"nombre": "leer", "espera": True}]
    assert modulo.pasos_con_await(pasos) == ["bajar", "leer"]


def test_agregar_await():
    assert modulo.agregar_await("bajar(url)") == "await bajar(url)"
    assert modulo.agregar_await("await bajar(url)") == "await bajar(url)"


def test_contar_awaits():
    assert modulo.contar_awaits("a = await f()\nb = await g()") == 2
    assert modulo.contar_awaits("x = 1") == 0


def test_quitar_await():
    assert modulo.quitar_await("await bajar()") == "bajar()"
    assert modulo.quitar_await("sumar()") == "sumar()"


def test_tiene_await_linea():
    assert modulo.tiene_await_linea("await f()") is True
    assert modulo.tiene_await_linea("f()") is False


def test_lineas_con_await():
    assert modulo.lineas_con_await(["x=1", "await a()", "await b()"]) == ["await a()", "await b()"]


def test_lineas_sin_await():
    assert modulo.lineas_sin_await(["x=1", "await a()"]) == ["x=1"]


def test_indices_con_await():
    assert modulo.indices_con_await(["x=1", "await a()", "await b()"]) == [1, 2]


def test_cuantas_con_await():
    assert modulo.cuantas_con_await(["await a()", "x=1", "await b()"]) == 2


def test_todas_con_await():
    assert modulo.todas_con_await(["await a()", "await b()"]) is True
    assert modulo.todas_con_await(["await a()", "x=1"]) is False


def test_ninguna_con_await():
    assert modulo.ninguna_con_await(["x=1", "y=2"]) is True
    assert modulo.ninguna_con_await(["await a()"]) is False


def test_agregar_await_a_todas():
    assert modulo.agregar_await_a_todas(["a()", "await b()"]) == ["await a()", "await b()"]


def test_quitar_await_de_todas():
    assert modulo.quitar_await_de_todas(["await a()", "b()"]) == ["a()", "b()"]


def test_primer_indice_await():
    assert modulo.primer_indice_await(["x=1", "await a()"]) == 1
    assert modulo.primer_indice_await(["x=1"]) == -1


def test_proporcion_con_await():
    assert modulo.proporcion_con_await(["await a()", "x=1", "y=2", "await b()"]) == 0.5


def test_normalizar_await():
    assert modulo.normalizar_await("await await f()") == "await f()"
    assert modulo.normalizar_await("f()") == "await f()"


def test_contar_await_total():
    assert modulo.contar_await_total("await a()\nawait b()") == 2


def test_mas_corta_con_await():
    assert modulo.mas_corta_con_await(["await bajar()", "await ir()"]) == "await ir()"
    assert modulo.mas_corta_con_await(["x=1"]) is None, "Si no hay líneas con await, devolvé None"


def test_juntar_lineas():
    assert modulo.juntar_lineas(["a", "b", "c"]) == "a\nb\nc"
