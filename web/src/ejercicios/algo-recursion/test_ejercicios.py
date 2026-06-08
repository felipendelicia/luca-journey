"""🧪 Tests — Recursión"""
import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"algo_recursion_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_factorial():
    assert modulo.factorial(5) == 120
    assert modulo.factorial(0) == 1


def test_suma_hasta():
    assert modulo.suma_hasta(4) == 10
    assert modulo.suma_hasta(0) == 0


def test_fibonacci():
    assert modulo.fibonacci(6) == 8
    assert modulo.fibonacci(0) == 0
    assert modulo.fibonacci(1) == 1


def test_potencia():
    assert modulo.potencia(2, 5) == 32
    assert modulo.potencia(7, 0) == 1


def test_cuenta_regresiva():
    assert modulo.cuenta_regresiva(3) == "3,2,1,Ya!"
    assert modulo.cuenta_regresiva(0) == "Ya!"


def test_suma_lista():
    assert modulo.suma_lista([1, 2, 3]) == 6
    assert modulo.suma_lista([]) == 0


def test_largo():
    assert modulo.largo([10, 20, 30]) == 3
    assert modulo.largo([]) == 0


def test_maximo():
    assert modulo.maximo([3, 9, 1]) == 9
    assert modulo.maximo([5]) == 5


def test_invertir_texto():
    assert modulo.invertir_texto("pika") == "akip"
    assert modulo.invertir_texto("") == ""


def test_es_palindromo():
    assert modulo.es_palindromo("ana") is True
    assert modulo.es_palindromo("pika") is False


def test_contar_apariciones():
    assert modulo.contar_apariciones([1, 2, 1, 1], 1) == 3


def test_multiplicar():
    assert modulo.multiplicar(4, 3) == 12
    assert modulo.multiplicar(7, 0) == 0


def test_mcd():
    assert modulo.mcd(12, 8) == 4
    assert modulo.mcd(7, 0) == 7


def test_suma_digitos():
    assert modulo.suma_digitos(253) == 10


def test_aplanar():
    assert modulo.aplanar([1, [2, [3, 4]], 5]) == [1, 2, 3, 4, 5]


def test_binomial():
    assert modulo.binomial(5, 2) == 10
    assert modulo.binomial(4, 0) == 1


def test_hanoi_movimientos():
    assert modulo.hanoi_movimientos(3) == 7
    assert modulo.hanoi_movimientos(0) == 0


def test_busqueda_binaria_rec():
    assert modulo.busqueda_binaria_rec([1, 3, 5, 7, 9], 7) == 3
    assert modulo.busqueda_binaria_rec([1, 3, 5], 4) == -1


def test_contar_pares():
    assert modulo.contar_pares([1, 2, 4, 7, 8]) == 3


def test_cantidad_digitos():
    assert modulo.cantidad_digitos(2025) == 4
    assert modulo.cantidad_digitos(7) == 1
