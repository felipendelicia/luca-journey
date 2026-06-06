"""🧪 Tests — Descargador async"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"async_bot_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_preparar():
    assert modulo.preparar(["a", "b"]) == [{"url": "a", "ok": False}, {"url": "b", "ok": False}]
    assert modulo.preparar([]) == []


def test_en_lotes():
    assert modulo.en_lotes([1, 2, 3], 2) == [[1, 2], [3]]


def test_marcar_ok():
    assert modulo.marcar_ok([{"url": "a", "ok": False}]) == [{"url": "a", "ok": True}]


def test_resumen():
    assert modulo.resumen([{"ok": True}, {"ok": False}]) == "2 descargas, 1 ok."
    assert modulo.resumen([{"ok": True}, {"ok": True}]) == "2 descargas, 2 ok."
