"""🧪 Tests — Cola (queue)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_cola_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_encolar():
    assert modulo.encolar([1, 2], 3) == [1, 2, 3]


def test_atender():
    cola = [1, 2, 3]
    assert modulo.atender(cola) == 1
    assert cola == [2, 3]
    assert modulo.atender([]) is None


def test_en_espera():
    assert modulo.en_espera([1, 2, 3]) == 3
    assert modulo.en_espera([]) == 0


def test_orden_de_atencion():
    cola = [1, 2, 3]
    assert modulo.orden_de_atencion(cola) == [1, 2, 3]
    assert cola == [1, 2, 3]


def test_esta_vacia():
    assert modulo.esta_vacia([]) is True
    assert modulo.esta_vacia(["A"]) is False


def test_tamano():
    assert modulo.tamano(["A", "B"]) == 2


def test_proximo():
    assert modulo.proximo(["Ash", "Misty"]) == "Ash"
    assert modulo.proximo([]) is None, "Con la cola vacía devolvé None"


def test_encolar_varios():
    assert modulo.encolar_varios(["A"], ["B", "C"]) == ["A", "B", "C"]


def test_atender_a_todos():
    assert modulo.atender_a_todos(["A", "B", "C"]) == ["A", "B", "C"]


def test_atender_n():
    assert modulo.atender_n(["A", "B", "C"], 2) == ["A", "B"]
    assert modulo.atender_n(["A"], 5) == ["A"]


def test_simular_cola():
    assert modulo.simular_cola(["enqueue 1", "enqueue 2", "dequeue"]) == [2]


def test_josephus():
    assert modulo.josephus(["A", "B", "C", "D"], 2) == "A"
    assert modulo.josephus(["solo"], 3) == "solo"


def test_invertir_cola():
    assert modulo.invertir_cola(["A", "B", "C"]) == ["C", "B", "A"]


def test_intercalar():
    assert modulo.intercalar(["A", "C"], ["B", "D", "E"]) == ["A", "B", "C", "D", "E"]


def test_posicion_en_fila():
    assert modulo.posicion_en_fila(["A", "B", "C"], "C") == 3
    assert modulo.posicion_en_fila(["A"], "Z") == -1


def test_mover_al_final():
    assert modulo.mover_al_final(["A", "B", "C"], "A") == ["B", "C", "A"]


def test_hay_en_cola():
    assert modulo.hay_en_cola(["A", "B"], "B") is True
    assert modulo.hay_en_cola(["A"], "Z") is False


def test_duplicar_cada():
    assert modulo.duplicar_cada(["A", "B"]) == ["A", "A", "B", "B"]


def test_atender_hasta():
    assert modulo.atender_hasta(["A", "B", "C"], "B") == ["A", "B"]


def test_rotar():
    assert modulo.rotar(["A", "B", "C", "D"], 2) == ["C", "D", "A", "B"]
