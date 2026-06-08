"""🧪 Tests — Corrutinas (async def)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_corrutinas_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


async def descargar():
    return 1


async def subir():
    return 2


def sumar():
    return 3


def test_es_corrutina():
    assert modulo.es_corrutina(descargar) is True
    assert modulo.es_corrutina(sumar) is False


def test_contar_corrutinas():
    assert modulo.contar_corrutinas([descargar, sumar, subir]) == 2
    assert modulo.contar_corrutinas([sumar]) == 0


def test_nombres_corrutinas():
    assert modulo.nombres_corrutinas([descargar, sumar, subir]) == ["descargar", "subir"]


def test_firma():
    assert modulo.firma("descargar", True) == "async def descargar():"
    assert modulo.firma("sumar", False) == "def sumar():"


async def _af():
    pass


async def _descargar():
    pass


def _nf():
    pass


def _sumar():
    pass


def test_tipo_de():
    assert modulo.tipo_de(_af) == "async"
    assert modulo.tipo_de(_nf) == "normal"


def test_primera_corrutina():
    assert modulo.primera_corrutina([_nf, _descargar, _af]) == "_descargar"
    assert modulo.primera_corrutina([_nf, _sumar]) is None, "Si no hay corrutinas, devolvé None"


def test_nombres_normales():
    assert modulo.nombres_normales([_af, _nf, _sumar]) == ["_nf", "_sumar"]


def test_solo_corrutinas():
    r = modulo.solo_corrutinas([_af, _nf, _descargar])
    assert [f.__name__ for f in r] == ["_af", "_descargar"]


def test_firma_con_args():
    assert modulo.firma_con_args("bajar", ["url", "destino"], True) == "async def bajar(url, destino):"
    assert modulo.firma_con_args("sumar", ["a", "b"], False) == "def sumar(a, b):"


def test_agregar_async():
    assert modulo.agregar_async("def f():") == "async def f():"
    assert modulo.agregar_async("async def f():") == "async def f():"


def test_quitar_async():
    assert modulo.quitar_async("async def f():") == "def f():"
    assert modulo.quitar_async("def f():") == "def f():"


def test_es_definicion_async():
    assert modulo.es_definicion_async("async def f():") is True
    assert modulo.es_definicion_async("def f():") is False


def test_nombre_de_firma():
    assert modulo.nombre_de_firma("async def descargar():") == "descargar"
    assert modulo.nombre_de_firma("def sumar():") == "sumar"


def test_cuenta_awaits():
    assert modulo.cuenta_awaits("await a()\nawait b()") == 2
    assert modulo.cuenta_awaits("x = 1") == 0


def test_tiene_await():
    assert modulo.tiene_await("await f()") is True
    assert modulo.tiene_await("x = 1") is False


def test_clasificar_todas():
    assert modulo.clasificar_todas([_af, _nf]) == {"_af": "async", "_nf": "normal"}


def test_hay_alguna_async():
    assert modulo.hay_alguna_async([_nf, _af]) is True
    assert modulo.hay_alguna_async([_nf, _sumar]) is False


def test_todas_async():
    assert modulo.todas_async([_af, _descargar]) is True
    assert modulo.todas_async([_af, _nf]) is False


def test_proporcion_async():
    assert modulo.proporcion_async([_af, _nf, _sumar, _descargar]) == 0.5


def test_firma_lista():
    assert modulo.firma_lista(["a", "b"], True) == ["async def a():", "async def b():"]
