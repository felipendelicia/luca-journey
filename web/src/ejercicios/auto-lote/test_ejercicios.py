"""🧪 Tests — Procesar carpetas en lote"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_lote_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_solo_extension():
    assert modulo.solo_extension(["a.py", "b.txt", "c.py"], ".py") == ["a.py", "c.py"]
    assert modulo.solo_extension(["a.txt"], ".py") == []


def test_contar_por_extension():
    assert modulo.contar_por_extension(["a.py", "b.txt", "c.py"]) == {".py": 2, ".txt": 1}
    assert modulo.contar_por_extension([]) == {}


def test_renombrar_lote():
    assert modulo.renombrar_lote(["IMG_1.png", "IMG_2.png"], "IMG", "foto") == ["foto_1.png", "foto_2.png"]


def test_mas_grande():
    assert modulo.mas_grande([("a.txt", 10), ("b.txt", 99), ("c.txt", 5)]) == "b.txt"
    assert modulo.mas_grande([]) is None
