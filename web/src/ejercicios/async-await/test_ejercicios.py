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
