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


def test_validar_hp_propia():
    assert modulo.validar_hp(50) == 50
    with pytest.raises(modulo.HPInvalidoError):
        modulo.validar_hp(200)


def test_validar_nivel_propia():
    assert modulo.validar_nivel(50) == 50
    with pytest.raises(modulo.NivelInvalidoError):
        modulo.validar_nivel(0)


def test_retirar_propia():
    assert modulo.retirar(100, 30) == 70
    with pytest.raises(modulo.SaldoInsuficienteError):
        modulo.retirar(10, 50)


def test_buscar_pokemon_propia():
    assert modulo.buscar_pokemon({"pikachu": 25}, "pikachu") == 25
    with pytest.raises(modulo.PokemonNoEncontradoError):
        modulo.buscar_pokemon({}, "mew")


def test_clases_heredan_de_exception():
    for clase in (modulo.HPInvalidoError, modulo.NivelInvalidoError, modulo.SaldoInsuficienteError,
                  modulo.PokemonNoEncontradoError, modulo.ColeccionVaciaError):
        assert issubclass(clase, Exception), "Tu excepción tiene que heredar de Exception"


def test_rango_error_guarda_valor():
    with pytest.raises(modulo.RangoError) as info:
        modulo.validar_en_rango(50, 1, 10)
    assert info.value.valor == 50, "RangoError tiene que guardar el valor que falló en self.valor"


def test_validar_en_rango():
    assert modulo.validar_en_rango(5, 1, 10) == 5


def test_nombre_del_error():
    assert modulo.nombre_del_error(int, "pika") == "ValueError"
    assert modulo.nombre_del_error(int, "42") is None, "Si no tira error, devolvé None"


def test_mensaje_de():
    assert modulo.mensaje_de(ValueError("mal")) == "mal"


def test_es_instancia():
    assert modulo.es_instancia(ValueError("x"), ValueError) is True
    assert modulo.es_instancia(ValueError("x"), KeyError) is False


def test_lanza_ese_error():
    assert modulo.lanza_ese_error(int, "pika", ValueError) is True
    assert modulo.lanza_ese_error(int, "42", ValueError) is False


def test_sacar_uno():
    assert modulo.sacar_uno([1, 2, 3]) == 3
    with pytest.raises(modulo.ColeccionVaciaError):
        modulo.sacar_uno([])
