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


def _dfg():
    return pd.DataFrame({
        "nombre": ["pikachu", "raichu", "onix", "staryu", "gyarados"],
        "tipo": ["electrico", "electrico", "roca", "agua", "agua"],
        "nivel": [25, 40, 12, 18, 35],
    })


def test_minimo_por_tipo():
    assert modulo.minimo_por_tipo(_dfg()) == {"agua": 18, "electrico": 25, "roca": 12}


def test_suma_nivel_por_tipo():
    assert modulo.suma_nivel_por_tipo(_dfg()) == {"agua": 53, "electrico": 65, "roca": 12}


def test_tipos_distintos():
    assert modulo.tipos_distintos(_dfg()) == ["agua", "electrico", "roca"]


def test_cantidad_tipos():
    assert modulo.cantidad_tipos(_dfg()) == 3


def test_tipo_con_mas_pokemon():
    assert modulo.tipo_con_mas_pokemon(_dfg()) == "agua"


def test_nombres_por_tipo():
    assert modulo.nombres_por_tipo(_dfg()) == {"agua": ["staryu", "gyarados"], "electrico": ["pikachu", "raichu"], "roca": ["onix"]}


def test_nivel_total():
    assert modulo.nivel_total(_dfg()) == 130


def test_hay_tipo():
    assert modulo.hay_tipo(_dfg(), "agua") is True
    assert modulo.hay_tipo(_dfg(), "fuego") is False


def test_promedio_general():
    assert modulo.promedio_general(_dfg(), "nivel") == 26.0


def test_ordenar_tipos_por_cantidad():
    assert modulo.ordenar_tipos_por_cantidad(_dfg()) == ["agua", "electrico", "roca"]


def test_tipo_con_nivel_mas_alto():
    assert modulo.tipo_con_nivel_mas_alto(_dfg()) == "electrico"


def test_filtrar_grupos_grandes():
    assert modulo.filtrar_grupos_grandes(_dfg(), 2) == ["agua", "electrico"]


def test_mediana_por_tipo():
    assert modulo.mediana_por_tipo(_dfg()) == {"agua": 26.5, "electrico": 32.5, "roca": 12.0}
