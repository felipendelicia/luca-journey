"""🧪 Tests — assert: afirmaciones"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"assert_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_verificar_positivo():
    assert modulo.verificar_positivo(5) == 5
    with pytest.raises(AssertionError):
        modulo.verificar_positivo(-2)


def test_verificar_nivel():
    assert modulo.verificar_nivel(50) == 50
    with pytest.raises(AssertionError):
        modulo.verificar_nivel(0)


def test_promedio():
    assert modulo.promedio([10, 20, 30]) == 20
    with pytest.raises(AssertionError):
        modulo.promedio([])


def test_afirmar_no_negativo():
    assert modulo.afirmar_no_negativo(5) == 5
    with pytest.raises(AssertionError):
        modulo.afirmar_no_negativo(-1)


def test_afirmar_en_rango():
    assert modulo.afirmar_en_rango(5, 1, 10) == 5
    with pytest.raises(AssertionError):
        modulo.afirmar_en_rango(20, 1, 10)


def test_afirmar_no_vacio():
    assert modulo.afirmar_no_vacio("Ash") == "Ash"
    with pytest.raises(AssertionError):
        modulo.afirmar_no_vacio("")


def test_afirmar_par():
    assert modulo.afirmar_par(4) == 4
    with pytest.raises(AssertionError):
        modulo.afirmar_par(3)


def test_afirmar_tipo_valido():
    assert modulo.afirmar_tipo_valido("Agua") == "Agua"
    with pytest.raises(AssertionError):
        modulo.afirmar_tipo_valido("Cosmico")


def test_afirmar_suma():
    assert modulo.afirmar_suma(2, 3, 5) == 5
    with pytest.raises(AssertionError):
        modulo.afirmar_suma(2, 3, 9)


def test_afirmar_ordenada():
    assert modulo.afirmar_ordenada([1, 2, 3]) == [1, 2, 3]
    with pytest.raises(AssertionError):
        modulo.afirmar_ordenada([3, 1, 2])


def test_afirmar_unicos():
    assert modulo.afirmar_unicos([1, 2, 3]) == [1, 2, 3]
    with pytest.raises(AssertionError):
        modulo.afirmar_unicos([1, 1, 2])


def test_afirmar_misma_longitud():
    assert modulo.afirmar_misma_longitud([1, 2], ["a", "b"]) is True
    with pytest.raises(AssertionError):
        modulo.afirmar_misma_longitud([1], [1, 2])


def test_afirmar_clave():
    assert modulo.afirmar_clave({"hp": 35}, "hp") == 35
    with pytest.raises(AssertionError):
        modulo.afirmar_clave({}, "hp")


def test_afirmar_positivos():
    assert modulo.afirmar_positivos([1, 2, 3]) == [1, 2, 3]
    with pytest.raises(AssertionError):
        modulo.afirmar_positivos([1, -2])


def test_afirmar_porcentaje():
    assert modulo.afirmar_porcentaje(50) == 50
    with pytest.raises(AssertionError):
        modulo.afirmar_porcentaje(150)


def test_afirmar_es_entero():
    assert modulo.afirmar_es_entero(7) == 7
    with pytest.raises(AssertionError):
        modulo.afirmar_es_entero("7")


def test_afirmar_mayor():
    assert modulo.afirmar_mayor(9, 3) == 9
    with pytest.raises(AssertionError):
        modulo.afirmar_mayor(3, 9)


def test_afirmar_contiene():
    assert modulo.afirmar_contiene([1, 2, 3], 2) == 2
    with pytest.raises(AssertionError):
        modulo.afirmar_contiene([1, 2], 9)


def test_afirmar_longitud():
    assert modulo.afirmar_longitud([1, 2, 3], 3) == [1, 2, 3]
    with pytest.raises(AssertionError):
        modulo.afirmar_longitud([1], 3)


def test_afirmar_no_none():
    assert modulo.afirmar_no_none(0) == 0
    with pytest.raises(AssertionError):
        modulo.afirmar_no_none(None)
