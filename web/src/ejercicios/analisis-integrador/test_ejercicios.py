"""🧪 Tests — Análisis integrador"""
import importlib.util
import os

import numpy as np
import pandas as pd

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"integr_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))

DATOS = {
    "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Ivysaur", "Eevee"],
    "tipo": ["Electrico", "Fuego", "Planta", "Planta", "Normal"],
    "nivel": [25, 90, 12, 30, np.nan],
}


def test_cargar():
    df = modulo.cargar(DATOS)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 5


def test_limpiar():
    r = modulo.limpiar(modulo.cargar(DATOS))
    assert len(r) == 4
    assert list(r.index) == [0, 1, 2, 3]


def test_cantidad():
    assert modulo.cantidad(modulo.cargar(DATOS)) == 5


def test_tipo_mas_comun():
    assert modulo.tipo_mas_comun(modulo.cargar(DATOS)) == "Planta"


def test_nivel_promedio():
    df = modulo.limpiar(modulo.cargar(DATOS))
    assert modulo.nivel_promedio(df) == (25 + 90 + 12 + 30) / 4


def test_top_n():
    df = modulo.limpiar(modulo.cargar(DATOS))
    r = modulo.top_n(df, 2)
    assert list(r["nombre"]) == ["Charizard", "Ivysaur"]


def test_promedio_por_tipo():
    df = modulo.limpiar(modulo.cargar(DATOS))
    r = modulo.promedio_por_tipo(df)
    assert r["Planta"] == 21.0


def test_campeon_del_tipo():
    df = modulo.limpiar(modulo.cargar(DATOS))
    assert modulo.campeon_del_tipo(df, "Planta") == "Ivysaur"
