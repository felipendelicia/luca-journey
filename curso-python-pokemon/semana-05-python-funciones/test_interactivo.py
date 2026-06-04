"""
🧪 Tests de la Calculadora de Estadísticas — Semana 05
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana05_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")


def test_calcular_dano_basico():
    assert interactivo.calcular_dano(50, 20) == 30


def test_calcular_dano_super_efectivo():
    assert interactivo.calcular_dano(50, 20, es_super=True) == 60


def test_calcular_dano_minimo_uno():
    assert interactivo.calcular_dano(10, 50) == 1, "Siempre hace al menos 1 de daño"


def test_velocidad_efectiva():
    assert interactivo.velocidad_efectiva(40, 10) == 60


def test_velocidad_efectiva_paralizado():
    assert interactivo.velocidad_efectiva(40, 10, paralizado=True) == 30, (
        "Paralizado debería reducir la velocidad a la mitad"
    )


def test_nivel_desde_experiencia():
    assert interactivo.nivel_desde_experiencia(550) == 5
    assert interactivo.nivel_desde_experiencia(0) == 1, "Mínimo nivel 1"


def test_hp_maximo():
    assert interactivo.hp_maximo(45, 10) == 75, "45 + 10*2 + 10 = 75"


def test_pedir_entero_reintenta(monkeypatch, capsys):
    # Primero el usuario escribe basura, después un número válido.
    respuestas = iter(["abc", "25"])
    monkeypatch.setattr("builtins.input", lambda *a, **k: next(respuestas))
    resultado = interactivo.pedir_entero("Nivel: ")
    assert resultado == 25, "Debería reintentar hasta recibir un número válido"
