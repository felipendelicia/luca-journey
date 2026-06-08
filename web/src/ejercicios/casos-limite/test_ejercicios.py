"""🧪 Tests — Casos límite y errores"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"casoslim_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_probar_largo():
    modulo.probar_largo(lambda t: len(t))
    # función que olvida el caso vacío (devuelve 1 para "")
    with pytest.raises(AssertionError):
        modulo.probar_largo(lambda t: len(t) if t else 1)


def test_probar_suma_lista():
    modulo.probar_suma_lista(lambda nums: sum(nums))
    with pytest.raises(AssertionError):
        modulo.probar_suma_lista(lambda nums: 99)


def test_probar_dividir():
    modulo.probar_dividir(lambda a, b: a / b)
    # una división que NO lanza con 0 (devuelve 0) -> el test debe detectarlo
    with pytest.raises(AssertionError):
        modulo.probar_dividir(lambda a, b: 0)


def test_probar_division_segura():
    modulo.probar_division_segura(lambda a, b: a / b if b != 0 else None)
    with pytest.raises(AssertionError):
        modulo.probar_division_segura(lambda a, b: a / b if b != 0 else 0)


def test_probar_primero_seguro():
    modulo.probar_primero_seguro(lambda l: l[0] if l else None)
    with pytest.raises(AssertionError):
        modulo.probar_primero_seguro(lambda l: l[0] if l else 0)


def test_probar_ultimo_seguro():
    modulo.probar_ultimo_seguro(lambda l: l[-1] if l else None)
    with pytest.raises(AssertionError):
        modulo.probar_ultimo_seguro(lambda l: l[-1] if l else 0)


def test_probar_promedio_seguro():
    modulo.probar_promedio_seguro(lambda l: sum(l) / len(l) if l else 0)
    with pytest.raises(AssertionError):
        modulo.probar_promedio_seguro(lambda l: sum(l) / len(l) if l else -1)


def test_probar_maximo_seguro():
    modulo.probar_maximo_seguro(lambda l: max(l) if l else None)
    with pytest.raises(AssertionError):
        modulo.probar_maximo_seguro(lambda l: max(l) if l else 0)


def test_probar_es_vacio():
    modulo.probar_es_vacio(lambda l: len(l) == 0)
    with pytest.raises(AssertionError):
        modulo.probar_es_vacio(lambda l: False)


def test_probar_clamp():
    modulo.probar_clamp(lambda n, lo, hi: lo if n < lo else (hi if n > hi else n))
    with pytest.raises(AssertionError):
        modulo.probar_clamp(lambda n, lo, hi: min(n, hi))


def test_probar_signo():
    modulo.probar_signo(lambda n: 0 if n == 0 else (1 if n > 0 else -1))
    with pytest.raises(AssertionError):
        modulo.probar_signo(lambda n: 1 if n > 0 else -1)


def test_probar_porcentaje():
    modulo.probar_porcentaje(lambda p, t: p / t * 100 if t != 0 else 0)
    with pytest.raises(AssertionError):
        modulo.probar_porcentaje(lambda p, t: p / t * 100 if t != 0 else 100)


def test_probar_indice_seguro():
    modulo.probar_indice_seguro(lambda l, i: l[i] if 0 <= i < len(l) else None)
    with pytest.raises(AssertionError):
        modulo.probar_indice_seguro(lambda l, i: l[i] if i < len(l) else 0)


def test_probar_contar_vocales():
    modulo.probar_contar_vocales(lambda s: sum(1 for c in s if c in "aeiou"))
    with pytest.raises(AssertionError):
        modulo.probar_contar_vocales(lambda s: len(s))


def test_probar_recortar():
    modulo.probar_recortar(lambda s, n: s[:n])
    with pytest.raises(AssertionError):
        modulo.probar_recortar(lambda s, n: s[:n] if n < len(s) else "")


def test_probar_quitar_negativos():
    modulo.probar_quitar_negativos(lambda l: [x for x in l if x >= 0])
    with pytest.raises(AssertionError):
        modulo.probar_quitar_negativos(lambda l: [x for x in l if x > 0])


def test_probar_primera_palabra():
    modulo.probar_primera_palabra(lambda s: s.split()[0] if s.split() else "")
    with pytest.raises(AssertionError):
        modulo.probar_primera_palabra(lambda s: s[0] if s else "")


def test_probar_minimo_seguro():
    modulo.probar_minimo_seguro(lambda l: min(l) if l else None)
    with pytest.raises(AssertionError):
        modulo.probar_minimo_seguro(lambda l: min(l) if l else 0)


def test_probar_dividir_lista():
    modulo.probar_dividir_lista(lambda l, d: [x / d for x in l] if d != 0 else None)
    with pytest.raises(AssertionError):
        modulo.probar_dividir_lista(lambda l, d: [x / d for x in l] if d != 0 else [])


def test_probar_es_positivo():
    modulo.probar_es_positivo(lambda n: n > 0)
    with pytest.raises(AssertionError):
        modulo.probar_es_positivo(lambda n: n >= 0)
