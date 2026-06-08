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


def test_solo_imagenes():
    assert modulo.solo_imagenes(["a.png", "b.txt", "c.jpg"]) == ["a.png", "c.jpg"]


def test_nombres_sin_extension():
    assert modulo.nombres_sin_extension(["a.py", "b.txt"]) == ["a", "b"]


def test_agregar_prefijo():
    assert modulo.agregar_prefijo(["a.py"], "viejo_") == ["viejo_a.py"]


def test_tamano_total():
    assert modulo.tamano_total([("a", 10), ("b", 5)]) == 15


def test_mas_chico():
    assert modulo.mas_chico([("a", 10), ("b", 99), ("c", 5)]) == "c"
    assert modulo.mas_chico([]) is None, "Con la lista vacía devolvé None"


def test_ordenar_por_tamano():
    assert modulo.ordenar_por_tamano([("a", 10), ("b", 99), ("c", 5)]) == ["b", "a", "c"]


def test_filtrar_mayores_a():
    assert modulo.filtrar_mayores_a([("a", 10), ("b", 99), ("c", 5)], 8) == ["a", "b"]


def test_extensiones_unicas():
    assert modulo.extensiones_unicas(["a.py", "b.txt", "c.py"]) == [".py", ".txt"]


def test_contar():
    assert modulo.contar(["a", "b", "c"]) == 3


def test_quitar_duplicados():
    assert modulo.quitar_duplicados(["a.py", "b.py", "a.py"]) == ["a.py", "b.py"]


def test_tienen_extension():
    assert modulo.tienen_extension(["a.py", "b.py"], ".py") is True
    assert modulo.tienen_extension(["a.py", "b.txt"], ".py") is False


def test_cambiar_todas_extensiones():
    assert modulo.cambiar_todas_extensiones(["a.txt", "b.txt"], ".md") == ["a.md", "b.md"]


def test_promedio_tamano():
    assert modulo.promedio_tamano([("a", 10), ("b", 20)]) == 15.0


def test_nombres_largos():
    assert modulo.nombres_largos(["a.py", "largote.py"], 5) == ["largote.py"]


def test_agrupar_por_extension():
    assert modulo.agrupar_por_extension(["a.py", "b.txt", "c.py"]) == {".py": ["a.py", "c.py"], ".txt": ["b.txt"]}


def test_hay_extension():
    assert modulo.hay_extension(["a.py", "b.txt"], ".txt") is True
    assert modulo.hay_extension(["a.py"], ".gif") is False
