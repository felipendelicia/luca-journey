"""🧪 Tests — Lanzar errores: raise"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"raise_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_validar_edad():
    assert modulo.validar_edad(25) == 25
    with pytest.raises(ValueError):
        modulo.validar_edad(-1)


def test_validar_nivel():
    assert modulo.validar_nivel(50) == 50
    with pytest.raises(ValueError):
        modulo.validar_nivel(0)
    with pytest.raises(ValueError):
        modulo.validar_nivel(101)


def test_dividir():
    assert modulo.dividir(10, 2) == 5
    with pytest.raises(ValueError):
        modulo.dividir(5, 0)


def test_solo_texto():
    assert modulo.solo_texto("Pikachu") == "Pikachu"
    with pytest.raises(TypeError):
        modulo.solo_texto(123)


def test_validar_hp():
    assert modulo.validar_hp(50) == 50
    with pytest.raises(ValueError):
        modulo.validar_hp(150)


def test_validar_no_vacio():
    assert modulo.validar_no_vacio("Ash") == "Ash"
    with pytest.raises(ValueError):
        modulo.validar_no_vacio("")


def test_validar_positivo():
    assert modulo.validar_positivo(5) == 5
    with pytest.raises(ValueError):
        modulo.validar_positivo(0)


def test_validar_tipo():
    assert modulo.validar_tipo("Agua") == "Agua"
    with pytest.raises(ValueError):
        modulo.validar_tipo("Cosmico")


def test_raiz():
    assert modulo.raiz(9) == 3.0
    with pytest.raises(ValueError):
        modulo.raiz(-1)


def test_retirar():
    assert modulo.retirar(100, 30) == 70
    with pytest.raises(ValueError):
        modulo.retirar(20, 50)


def test_validar_porcentaje():
    assert modulo.validar_porcentaje(75) == 75
    with pytest.raises(ValueError):
        modulo.validar_porcentaje(101)


def test_validar_email():
    assert modulo.validar_email("ash@kanto.com") == "ash@kanto.com"
    with pytest.raises(ValueError):
        modulo.validar_email("ash")


def test_indexar():
    assert modulo.indexar([10, 20], 1) == 20
    with pytest.raises(IndexError):
        modulo.indexar([10], 5)


def test_validar_par():
    assert modulo.validar_par(4) == 4
    with pytest.raises(ValueError):
        modulo.validar_par(3)


def test_validar_longitud():
    assert modulo.validar_longitud("pikachu", 3) == "pikachu"
    with pytest.raises(ValueError):
        modulo.validar_longitud("pi", 3)


def test_dividir_entero():
    assert modulo.dividir_entero(7, 2) == 3
    with pytest.raises(ZeroDivisionError):
        modulo.dividir_entero(5, 0)


def test_validar_rango():
    assert modulo.validar_rango(5, 1, 10) == 5
    with pytest.raises(ValueError):
        modulo.validar_rango(20, 1, 10)


def test_validar_lista_no_vacia():
    assert modulo.validar_lista_no_vacia([1]) == [1]
    with pytest.raises(ValueError):
        modulo.validar_lista_no_vacia([])


def test_validar_clave():
    assert modulo.validar_clave({"hp": 35}, "hp") == 35
    with pytest.raises(KeyError):
        modulo.validar_clave({}, "hp")


def test_validar_mayor_de_edad():
    assert modulo.validar_mayor_de_edad(20) == 20
    with pytest.raises(ValueError):
        modulo.validar_mayor_de_edad(15)
