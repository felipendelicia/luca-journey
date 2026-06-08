"""🧪 Tests — Pila (stack)"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_pila_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_apilar():
    assert modulo.apilar([1, 2], 3) == [1, 2, 3]


def test_desapilar():
    pila = [1, 2, 3]
    assert modulo.desapilar(pila) == 3
    assert pila == [1, 2]
    assert modulo.desapilar([]) is None


def test_tope():
    assert modulo.tope([1, 2, 3]) == 3
    assert modulo.tope([]) is None


def test_balanceado():
    assert modulo.balanceado("(a(b)c)") is True
    assert modulo.balanceado("(a(b)") is False
    assert modulo.balanceado(")(") is False


def test_esta_vacia():
    assert modulo.esta_vacia([]) is True
    assert modulo.esta_vacia([1]) is False


def test_tamano():
    assert modulo.tamano([1, 2, 3]) == 3
    assert modulo.tamano([]) == 0


def test_tope_seguro():
    assert modulo.tope_seguro([1, 2, 3]) == 3
    assert modulo.tope_seguro([]) is None, "Con la pila vacía hay que devolver None"


def test_apilar_varios():
    assert modulo.apilar_varios([1], [2, 3]) == [1, 2, 3]


def test_vaciar():
    assert modulo.vaciar([1, 2, 3]) == [3, 2, 1]


def test_invertir_pila():
    assert modulo.invertir([1, 2, 3]) == [3, 2, 1]


def test_balanceado_todo():
    assert modulo.balanceado_todo("([]{})") is True
    assert modulo.balanceado_todo("([)]") is False
    assert modulo.balanceado_todo("(") is False


def test_profundidad_maxima():
    assert modulo.profundidad_maxima("((()))") == 3
    assert modulo.profundidad_maxima("()()") == 1


def test_evaluar_postfija():
    assert modulo.evaluar_postfija(["3", "4", "+", "2", "*"]) == 14
    assert modulo.evaluar_postfija(["5"]) == 5


def test_decimal_a_binario():
    assert modulo.decimal_a_binario(6) == "110"
    assert modulo.decimal_a_binario(0) == "0"


def test_quitar_adyacentes():
    assert modulo.quitar_adyacentes("abbac") == "c"
    assert modulo.quitar_adyacentes("abc") == "abc"


def test_es_palindromo_pila():
    assert modulo.es_palindromo_pila("ana") is True
    assert modulo.es_palindromo_pila("pikachu") is False


def test_simular_pila():
    assert modulo.simular_pila(["push 3", "pop", "push 5"]) == [5]
    assert modulo.simular_pila(["pop"]) == []


def test_invertir_texto():
    assert modulo.invertir_texto("pika") == "akip"


def test_pares_completos():
    assert modulo.pares_completos("(())") == 2
    assert modulo.pares_completos("(()") == 1


def test_sin_cerrar():
    assert modulo.sin_cerrar("(()") == 1
    assert modulo.sin_cerrar("()") == 0
