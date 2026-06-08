"""🧪 Tests — pandas: Limpieza de datos"""
import importlib.util
import os

import numpy as np
import pandas as pd

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"pdlimp_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _sucio():
    return pd.DataFrame({
        "nombre": ["Pikachu", "Charizard", "Bulbasaur"],
        "nivel": [25.0, np.nan, 12.0],
        "hp": [np.nan, 78.0, 45.0],
    })


def test_contar_nulos():
    r = modulo.contar_nulos(_sucio())
    assert r == 2
    assert isinstance(r, int)


def test_rellenar_ceros():
    df = _sucio()
    r = modulo.rellenar_ceros(df, "nivel")
    assert list(r["nivel"]) == [25.0, 0.0, 12.0]
    assert df["nivel"].isna().sum() == 1, "No modifiques el original"


def test_quitar_filas_nulas():
    r = modulo.quitar_filas_nulas(_sucio())
    assert len(r) == 1
    assert list(r["nombre"]) == ["Bulbasaur"]


def test_a_entero():
    r = modulo.a_entero(pd.Series([1.0, 2.0, 3.0]))
    assert list(r) == [1, 2, 3]
    assert r.dtype == int


def test_sin_duplicados():
    df = pd.DataFrame({"x": [1, 1, 2], "y": ["a", "a", "b"]})
    assert len(modulo.sin_duplicados(df)) == 2


def test_renombrar():
    r = modulo.renombrar(_sucio(), "hp", "vida")
    assert "vida" in r.columns and "hp" not in r.columns


def test_a_mayusculas():
    r = modulo.a_mayusculas(pd.Series(["pikachu", "eevee"]))
    assert list(r) == ["PIKACHU", "EEVEE"]


def test_aplicar():
    r = modulo.aplicar(pd.Series([1, 2, 3]), lambda x: x * 10)
    assert list(r) == [10, 20, 30]


def test_sacar_espacios():
    assert modulo.sacar_espacios(pd.Series([" a ", "b "])).tolist() == ["a", "b"]


def test_a_minusculas():
    assert modulo.a_minusculas(pd.Series(["PIKA", "Onix"])).tolist() == ["pika", "onix"]


def test_reemplazar_valor():
    assert modulo.reemplazar_valor(pd.Series(["a", "b", "a"]), "a", "z").tolist() == ["z", "b", "z"]


def test_contar_unicos():
    assert modulo.contar_unicos(pd.Series([1, 1, 2, 3, 3])) == 3


def test_valores_unicos():
    assert modulo.valores_unicos(pd.Series([3, 1, 3, 2])) == [1, 2, 3]


def test_promedio_sin_nulos():
    assert modulo.promedio_sin_nulos(pd.Series([2, None, 4])) == 3.0


def test_contar_valor():
    assert modulo.contar_valor(pd.Series(["a", "b", "a"]), "a") == 2


def test_mas_frecuente():
    assert modulo.mas_frecuente(pd.Series(["agua", "agua", "fuego"])) == "agua"


def test_capitalizar():
    assert modulo.capitalizar(pd.Series(["pIKA", "onix"])).tolist() == ["Pika", "Onix"]


def test_columnas_con_nulos():
    df = pd.DataFrame({"a": [1, None], "b": [3, 4]})
    assert modulo.columnas_con_nulos(df) == ["a"]


def test_normalizar_texto():
    assert modulo.normalizar_texto(pd.Series([" Pikachu ", "ONIX"])).tolist() == ["pikachu", "onix"]


def test_longitud_textos():
    assert modulo.longitud_textos(pd.Series(["pi", "onix"])) == [2, 4]
