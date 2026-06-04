"""🧪 Tests — pandas: Agrupar y combinar"""
import importlib.util
import os

import pandas as pd

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"pdgrp_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _pokedex():
    return pd.DataFrame({
        "nombre": ["Pikachu", "Raichu", "Charizard", "Bulbasaur", "Ivysaur"],
        "tipo": ["Electrico", "Electrico", "Fuego", "Planta", "Planta"],
        "nivel": [25, 40, 90, 12, 30],
        "hp": [35, 60, 78, 45, 60],
    })


def test_contar_por_tipo():
    r = modulo.contar_por_tipo(_pokedex())
    assert r["Electrico"] == 2 and r["Planta"] == 2 and r["Fuego"] == 1


def test_nivel_promedio_por_tipo():
    r = modulo.nivel_promedio_por_tipo(_pokedex())
    assert r["Electrico"] == 32.5
    assert r["Fuego"] == 90


def test_nivel_maximo_por_tipo():
    r = modulo.nivel_maximo_por_tipo(_pokedex())
    assert r["Electrico"] == 40 and r["Planta"] == 30


def test_hp_total_por_tipo():
    r = modulo.hp_total_por_tipo(_pokedex())
    assert r["Electrico"] == 95 and r["Planta"] == 105


def test_tipo_mas_comun():
    assert modulo.tipo_mas_comun(_pokedex()) in ("Electrico", "Planta")


def test_combinar():
    df1 = pd.DataFrame({"tipo": ["Fuego", "Agua"], "nivel": [90, 30]})
    df2 = pd.DataFrame({"tipo": ["Fuego", "Agua"], "debilidad": ["Agua", "Planta"]})
    r = modulo.combinar(df1, df2, "tipo")
    assert "debilidad" in r.columns
    assert len(r) == 2
    fila = r[r["tipo"] == "Fuego"].iloc[0]
    assert fila["debilidad"] == "Agua"


def test_tipos_populares():
    r = modulo.tipos_populares(_pokedex())
    assert set(r.index) == {"Electrico", "Planta"}
    assert "Fuego" not in r.index
