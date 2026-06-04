"""
🧪 Tests del Sistema de Tipos — Semana 09
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana09_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")


def test_efectividad_super():
    mult, texto = interactivo.efectividad("Fuego", "Planta")
    assert mult == 2.0
    assert "súper efectivo" in texto


def test_efectividad_debil():
    mult, _ = interactivo.efectividad("Fuego", "Agua")
    assert mult == 0.5, "Fuego contra Agua debería ser poco efectivo"


def test_efectividad_normal():
    mult, _ = interactivo.efectividad("Fuego", "Electrico")
    assert mult == 1.0


def test_calcular_dano():
    assert interactivo.calcular_dano("Fuego", "Planta", 30) == 60, "Ventaja x2"
    assert interactivo.calcular_dano("Fuego", "Agua", 30) == 15, "Desventaja x0.5"


def test_clases_de_tipo():
    fuego = interactivo.Fuego("Charizard")
    assert fuego.tipo == "Fuego"
    assert fuego.nombre_ataque() == "Lanzallamas"
    agua = interactivo.Agua("Blastoise")
    assert agua.nombre_ataque() == "Hidrobomba"


def test_recibir_dano_y_debilitado():
    p = interactivo.Electrico("Pikachu")
    p.recibir_dano(100)
    assert p.esta_debilitado() is True
