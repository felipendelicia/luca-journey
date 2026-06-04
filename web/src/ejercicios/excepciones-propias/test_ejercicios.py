"""🧪 Tests — Excepciones personalizadas"""
import importlib.util
import os

import pytest

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"excprop_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_EquipoLlenoError():
    e = modulo.EquipoLlenoError()
    assert isinstance(e, Exception)
    assert str(e) == "equipo lleno"


def test_EntrenadorError():
    e = modulo.EntrenadorError("ups", 7)
    assert isinstance(e, Exception)
    assert str(e) == "ups"
    assert e.codigo == 7


def test_agregar():
    assert modulo.agregar(["Pikachu"], "Eevee") == ["Pikachu", "Eevee"]
    with pytest.raises(Exception) as info:
        modulo.agregar(["a", "b", "c", "d", "e", "f"], "Mew")
    assert type(info.value).__name__ == "EquipoLlenoError"


def test_fallar():
    with pytest.raises(Exception) as info:
        modulo.fallar(404)
    assert type(info.value).__name__ == "EntrenadorError"
    assert info.value.codigo == 404
