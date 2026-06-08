"""🧪 Tests — Grafos"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_grafo_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

G = {"a": ["b", "c"], "b": ["a"], "c": ["a"]}


def test_vecinos():
    assert modulo.vecinos(G, "a") == ["b", "c"]
    assert modulo.vecinos(G, "z") == []


def test_grado():
    assert modulo.grado(G, "a") == 2
    assert modulo.grado(G, "b") == 1


def test_hay_arista():
    assert modulo.hay_arista(G, "a", "b") is True
    assert modulo.hay_arista(G, "b", "c") is False


def test_nodos():
    assert modulo.nodos({"c": [], "a": [], "b": []}) == ["a", "b", "c"]


_G = {"a": ["b", "c"], "b": ["a", "d"], "c": ["a"], "d": ["b"]}


def test_cantidad_nodos():
    assert modulo.cantidad_nodos(_G) == 4


def test_nodos_aislados():
    assert modulo.nodos_aislados({"a": [], "b": ["c"], "c": ["b"]}) == ["a"]


def test_grado_maximo():
    assert modulo.grado_maximo(_G) == 2


def test_nodo_mas_conectado():
    assert modulo.nodo_mas_conectado(_G) == "a"


def test_grados():
    assert modulo.grados({"a": ["b"], "b": ["a", "c"], "c": ["b"]}) == {"a": 1, "b": 2, "c": 1}


def test_vecinos_comunes():
    assert modulo.vecinos_comunes({"a": ["x", "y"], "b": ["y", "z"]}, "a", "b") == ["y"]


def test_agregar_arista():
    assert modulo.agregar_arista({"a": []}, "a", "b") == {"a": ["b"], "b": ["a"]}


def test_quitar_nodo():
    assert modulo.quitar_nodo({"a": ["b"], "b": ["a"]}, "a") == {"b": []}


def test_recorrido_bfs():
    assert modulo.recorrido_bfs(_G, "a") == ["a", "b", "c", "d"]


def test_recorrido_dfs():
    assert modulo.recorrido_dfs(_G, "a") == ["a", "b", "d", "c"]


def test_hay_camino():
    assert modulo.hay_camino(_G, "a", "d") is True
    assert modulo.hay_camino({"a": [], "z": []}, "a", "z") is False


def test_distancia():
    assert modulo.distancia(_G, "a", "d") == 2
    assert modulo.distancia(_G, "a", "a") == 0
    assert modulo.distancia({"a": [], "z": []}, "a", "z") == -1


def test_componente():
    assert modulo.componente({"a": ["b"], "b": ["a"], "c": []}, "a") == ["a", "b"]


def test_alcanzables_en():
    assert modulo.alcanzables_en({"a": ["b"], "b": ["a", "c"], "c": ["b"]}, "a", 1) == ["a", "b"]


def test_es_hoja():
    assert modulo.es_hoja({"a": ["b"], "b": ["a", "c"]}, "a") is True
    assert modulo.es_hoja(_G, "a") is False


def test_cantidad_conexiones():
    assert modulo.cantidad_conexiones({"a": ["b"], "b": ["a"]}) == 2
