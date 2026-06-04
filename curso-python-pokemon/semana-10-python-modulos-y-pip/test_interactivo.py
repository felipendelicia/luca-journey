"""
🧪 Tests de la Pokédex Online — Semana 10

Usan datos FALSOS (no tocan internet) para probar el parseo y el formateo.
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana10_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")


# Un JSON falso con la forma que devuelve la PokéAPI (recortado).
DATOS_FALSOS = {
    "id": 25,
    "name": "pikachu",
    "height": 4,    # decímetros -> 0.4 m
    "weight": 60,   # hectogramos -> 6.0 kg
    "types": [{"type": {"name": "electric"}}],
    "stats": [
        {"stat": {"name": "hp"}, "base_stat": 35},
        {"stat": {"name": "attack"}, "base_stat": 55},
        {"stat": {"name": "speed"}, "base_stat": 90},
    ],
}


def test_parsear_datos_nombre_y_numero():
    info = interactivo.parsear_datos(DATOS_FALSOS)
    assert info["nombre"] == "pikachu"
    assert info["numero"] == 25


def test_parsear_datos_convierte_unidades():
    info = interactivo.parsear_datos(DATOS_FALSOS)
    assert info["altura_m"] == 0.4, "4 decímetros = 0.4 m"
    assert info["peso_kg"] == 6.0, "60 hectogramos = 6.0 kg"


def test_parsear_datos_tipos():
    info = interactivo.parsear_datos(DATOS_FALSOS)
    assert info["tipos"] == ["electric"]


def test_parsear_datos_stats():
    info = interactivo.parsear_datos(DATOS_FALSOS)
    assert info["stats"]["hp"] == 35
    assert info["stats"]["speed"] == 90


def test_parsear_datos_vacio_no_rompe():
    # Con un diccionario vacío, no debería explotar.
    info = interactivo.parsear_datos({})
    assert info["nombre"] == "?"
    assert info["tipos"] == []


def test_formatear_ficha():
    info = interactivo.parsear_datos(DATOS_FALSOS)
    ficha = interactivo.formatear_ficha(info)
    assert "PIKACHU" in ficha
    assert "electric" in ficha
    assert "0.4 m" in ficha
