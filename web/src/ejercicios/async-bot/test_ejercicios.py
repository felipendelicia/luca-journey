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


def _items():
    return [
        {"url": "https://a.com", "ok": True},
        {"url": "https://b.com", "ok": False},
        {"url": "https://c.com", "ok": True},
    ]


def test_cantidad():
    assert modulo.cantidad(["a", "b"]) == 2


def test_quitar_duplicados():
    assert modulo.quitar_duplicados(["a", "b", "a", "c"]) == ["a", "b", "c"]


def test_solo_https():
    assert modulo.solo_https(["https://a", "http://b", "https://c"]) == ["https://a", "https://c"]


def test_agregar_protocolo():
    assert modulo.agregar_protocolo("pokeapi.co") == "https://pokeapi.co"
    assert modulo.agregar_protocolo("http://x.com") == "http://x.com"


def test_contar_ok():
    assert modulo.contar_ok(_items()) == 2


def test_contar_fallidos():
    assert modulo.contar_fallidos(_items()) == 1


def test_urls_fallidas():
    assert modulo.urls_fallidas(_items()) == ["https://b.com"]


def test_tasa_exito():
    assert modulo.tasa_exito(_items()) == 2 / 3


def test_todos_ok():
    assert modulo.todos_ok(_items()) is False
    assert modulo.todos_ok([{"url": "x", "ok": True}]) is True


def test_primer_fallo():
    assert modulo.primer_fallo(_items())["url"] == "https://b.com"
    assert modulo.primer_fallo([{"url": "x", "ok": True}]) is None, "Si no hay fallos, devolvé None"


def test_marcar_todos_ok():
    r = modulo.marcar_todos_ok(_items())
    assert all(it["ok"] for it in r)


def test_resumen_estado():
    assert modulo.resumen_estado(_items()) == {"ok": 2, "error": 1}


def test_marcar_error():
    r = modulo.marcar_error(_items(), "https://a.com")
    assert r[0]["ok"] is False


def test_ordenar_por_url():
    items = [{"url": "z", "ok": True}, {"url": "a", "ok": True}]
    assert modulo.ordenar_por_url(items) == [{"url": "a", "ok": True}, {"url": "z", "ok": True}]


def test_agregar_si_nueva():
    assert modulo.agregar_si_nueva(["a"], "b") == ["a", "b"]
    assert modulo.agregar_si_nueva(["a"], "a") == ["a"]


def test_con_indice():
    assert modulo.con_indice(["a", "b"]) == [(0, "a"), (1, "b")]
