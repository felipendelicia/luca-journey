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


def _dfa():
    return pd.DataFrame({
        "nombre": ["pikachu", "raichu", "onix", "staryu", "gyarados"],
        "tipo": ["electrico", "electrico", "roca", "agua", "agua"],
        "nivel": [25, 40, 12, 18, 35],
    })


def test_mediana_nivel():
    assert modulo.mediana_nivel(_dfa()) == 25.0


def test_proporcion_tipo():
    assert modulo.proporcion_tipo(_dfa(), "agua") == 0.4


def test_nombres_top():
    assert modulo.nombres_top(_dfa(), 2) == ["raichu", "gyarados"]


def test_tipos_unicos():
    assert modulo.tipos_unicos(_dfa()) == ["agua", "electrico", "roca"]


def test_filtrar_fuertes():
    assert modulo.filtrar_fuertes(_dfa(), 30) == ["raichu", "gyarados"]


def test_rango_niveles():
    assert modulo.rango_niveles(_dfa()) == 28


def test_tipo_con_mayor_promedio():
    assert modulo.tipo_con_mayor_promedio(_dfa()) == "electrico"


def test_contar_por_rango():
    assert modulo.contar_por_rango(_dfa(), 15, 30) == 2


def test_nivel_total():
    assert modulo.nivel_total(_dfa()) == 130


def test_hay_fuertes():
    assert modulo.hay_fuertes(_dfa(), 35) is True
    assert modulo.hay_fuertes(_dfa(), 50) is False


def test_tabla_resumen():
    assert modulo.tabla_resumen(_dfa()) == {"total": 5, "tipos": 3, "nivel_total": 130}


def test_cantidad_por_tipo():
    assert modulo.cantidad_por_tipo(_dfa()) == {"agua": 2, "electrico": 2, "roca": 1}
