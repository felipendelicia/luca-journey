"""
🧪 Tests del Simulador de Batalla — Semana 04
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana04_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")


def test_aplicar_dano_resta():
    assert interactivo.aplicar_dano(100, 30) == 70, "100 - 30 = 70"


def test_aplicar_dano_no_baja_de_cero():
    assert interactivo.aplicar_dano(10, 50) == 0, (
        "El HP nunca debería quedar negativo: mínimo 0"
    )


def test_esta_debilitado():
    assert interactivo.esta_debilitado(0) is True
    assert interactivo.esta_debilitado(-5) is True
    assert interactivo.esta_debilitado(1) is False


def test_barra_hp_full():
    barra = interactivo.barra_hp(100, 100, largo=10)
    assert "100/100" in barra, "La barra debería mostrar el HP actual/máximo"
    assert "█" * 10 in barra, "Con HP lleno, la barra debería estar toda llena"


def test_barra_hp_vacia():
    barra = interactivo.barra_hp(0, 100, largo=10)
    assert "0/100" in barra
    assert "░" * 10 in barra, "Con HP en 0, la barra debería estar toda vacía"


def test_pikachu_tiene_tres_ataques():
    assert len(interactivo.ATAQUES_PIKACHU) == 3, "Pikachu debería tener 3 ataques"
