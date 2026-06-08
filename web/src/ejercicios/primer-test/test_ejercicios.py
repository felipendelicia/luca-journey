"""🧪 Tests — Tu primer test"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"primertest_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_probar_doble():
    # con una función correcta NO debe lanzar
    modulo.probar_doble(lambda x: x * 2)
    # con una función ROTA debe detectar el bug (AssertionError)
    with pytest.raises(AssertionError):
        modulo.probar_doble(lambda x: x + 2)


def test_probar_es_par():
    modulo.probar_es_par(lambda x: x % 2 == 0)
    with pytest.raises(AssertionError):
        modulo.probar_es_par(lambda x: True)


def test_probar_mayor():
    modulo.probar_mayor(lambda a, b: a if a >= b else b)
    with pytest.raises(AssertionError):
        modulo.probar_mayor(lambda a, b: a)


def test_probar_triple():
    modulo.probar_triple(lambda x: x * 3)
    with pytest.raises(AssertionError):
        modulo.probar_triple(lambda x: x + 3)


def test_probar_resta():
    modulo.probar_resta(lambda a, b: a - b)
    with pytest.raises(AssertionError):
        modulo.probar_resta(lambda a, b: b - a)


def test_probar_es_impar():
    modulo.probar_es_impar(lambda x: x % 2 == 1)
    with pytest.raises(AssertionError):
        modulo.probar_es_impar(lambda x: x % 2 == 0)


def test_probar_maximo():
    modulo.probar_maximo(lambda a, b: a if a >= b else b)
    with pytest.raises(AssertionError):
        modulo.probar_maximo(lambda a, b: a)


def test_probar_minimo():
    modulo.probar_minimo(lambda a, b: a if a <= b else b)
    with pytest.raises(AssertionError):
        modulo.probar_minimo(lambda a, b: a)


def test_probar_absoluto():
    modulo.probar_absoluto(abs)
    with pytest.raises(AssertionError):
        modulo.probar_absoluto(lambda x: x)


def test_probar_largo():
    modulo.probar_largo(len)
    with pytest.raises(AssertionError):
        modulo.probar_largo(lambda l: 0)


def test_probar_primero():
    modulo.probar_primero(lambda l: l[0])
    with pytest.raises(AssertionError):
        modulo.probar_primero(lambda l: l[-1])


def test_probar_ultimo():
    modulo.probar_ultimo(lambda l: l[-1])
    with pytest.raises(AssertionError):
        modulo.probar_ultimo(lambda l: l[0])


def test_probar_suma_lista():
    modulo.probar_suma_lista(sum)
    with pytest.raises(AssertionError):
        modulo.probar_suma_lista(lambda l: 0)


def test_probar_contiene():
    modulo.probar_contiene(lambda l, x: x in l)
    with pytest.raises(AssertionError):
        modulo.probar_contiene(lambda l, x: True)


def test_probar_invertir():
    modulo.probar_invertir(lambda l: l[::-1])
    with pytest.raises(AssertionError):
        modulo.probar_invertir(lambda l: l)


def test_probar_mayusculas():
    modulo.probar_mayusculas(lambda s: s.upper())
    with pytest.raises(AssertionError):
        modulo.probar_mayusculas(lambda s: s)


def test_probar_repetir():
    modulo.probar_repetir(lambda s, n: s * n)
    with pytest.raises(AssertionError):
        modulo.probar_repetir(lambda s, n: s)


def test_probar_promedio():
    modulo.probar_promedio(lambda l: sum(l) / len(l))
    with pytest.raises(AssertionError):
        modulo.probar_promedio(lambda l: sum(l))


def test_probar_cuadrado():
    modulo.probar_cuadrado(lambda x: x ** 2)
    with pytest.raises(AssertionError):
        modulo.probar_cuadrado(lambda x: x * 2)


def test_probar_es_vocal():
    modulo.probar_es_vocal(lambda c: c in "aeiou")
    with pytest.raises(AssertionError):
        modulo.probar_es_vocal(lambda c: True)
