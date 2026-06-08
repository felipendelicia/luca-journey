"""🧪 Tests — Proyecto: módulo testeado"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"proytest_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_raiz_cuadrada():
    assert modulo.raiz_cuadrada(9) == 3
    assert modulo.raiz_cuadrada(0) == 0
    with pytest.raises(ValueError):
        modulo.raiz_cuadrada(-4)


def _raiz_ok(n):
    if n < 0:
        raise ValueError()
    return n ** 0.5


def test_probar_raiz():
    modulo.probar_raiz(_raiz_ok)
    # una raíz que NO valida negativos -> el test debe detectarlo
    with pytest.raises(AssertionError):
        modulo.probar_raiz(lambda n: abs(n) ** 0.5)


def test_dividir_seguro():
    assert modulo.dividir_seguro(6, 2) == 3
    assert modulo.dividir_seguro(1, 0) is None


def test_probar_dividir_seguro():
    modulo.probar_dividir_seguro(lambda a, b: (a / b) if b else None)
    with pytest.raises(AssertionError):
        modulo.probar_dividir_seguro(lambda a, b: 0)


def test_clasificar_nivel():
    assert modulo.clasificar_nivel(10) == "bajo"
    assert modulo.clasificar_nivel(50) == "medio"
    assert modulo.clasificar_nivel(90) == "alto"


def test_probar_clasificar_nivel():
    modulo.probar_clasificar_nivel(lambda n: "bajo" if n < 30 else ("medio" if n < 70 else "alto"))
    with pytest.raises(AssertionError):
        modulo.probar_clasificar_nivel(lambda n: "bajo")


def test_iniciales():
    assert modulo.iniciales("ash ketchum") == "AK"


def test_probar_iniciales():
    modulo.probar_iniciales(lambda nom: "".join(p[0].upper() for p in nom.split()))
    with pytest.raises(AssertionError):
        modulo.probar_iniciales(lambda nom: nom[0].upper())


def test_contar_mayuscula():
    assert modulo.contar_mayuscula("PiKa") == 2


def test_probar_contar_mayuscula():
    modulo.probar_contar_mayuscula(lambda s: sum(1 for c in s if c.isupper()))
    with pytest.raises(AssertionError):
        modulo.probar_contar_mayuscula(lambda s: len(s))


def test_es_multiplo():
    assert modulo.es_multiplo(10, 5) is True
    assert modulo.es_multiplo(10, 3) is False


def test_probar_es_multiplo():
    modulo.probar_es_multiplo(lambda n, m: n % m == 0)
    with pytest.raises(AssertionError):
        modulo.probar_es_multiplo(lambda n, m: True)


def test_distancia():
    assert modulo.distancia(3, 8) == 5
    assert modulo.distancia(8, 3) == 5


def test_probar_distancia():
    modulo.probar_distancia(lambda a, b: abs(a - b))
    with pytest.raises(AssertionError):
        modulo.probar_distancia(lambda a, b: a - b)


def test_juntar():
    assert modulo.juntar(["a", "b"], "-") == "a-b"


def test_probar_juntar():
    modulo.probar_juntar(lambda l, s: s.join(l))
    with pytest.raises(AssertionError):
        modulo.probar_juntar(lambda l, s: "".join(l))


def test_limite():
    assert modulo.limite(5, 10) == 5
    assert modulo.limite(20, 10) == 10


def test_probar_limite():
    modulo.probar_limite(lambda n, m: min(n, m))
    with pytest.raises(AssertionError):
        modulo.probar_limite(lambda n, m: n)


def test_repetir_lista():
    assert modulo.repetir_lista([1, 2], 2) == [1, 2, 1, 2]


def test_probar_repetir_lista():
    modulo.probar_repetir_lista(lambda l, n: l * n)
    with pytest.raises(AssertionError):
        modulo.probar_repetir_lista(lambda l, n: l)
