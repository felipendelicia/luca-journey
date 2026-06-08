"""🧪 Tests — pandas: Series y DataFrame"""
import importlib.util
import os

import pandas as pd

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"pdsdf_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _pokedex():
    return pd.DataFrame({
        "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
        "nivel": [25, 90, 12, 70],
        "tipo": ["Electrico", "Fuego", "Planta", "Normal"],
    })


def test_crear_serie():
    s = modulo.crear_serie([10, 20, 30])
    assert isinstance(s, pd.Series)
    assert list(s) == [10, 20, 30]


def test_serie_con_indices():
    s = modulo.serie_con_indices([25, 90], ["Pikachu", "Charizard"])
    assert s["Charizard"] == 90


def test_crear_pokedex():
    df = modulo.crear_pokedex({"nombre": ["Eevee"], "nivel": [15]})
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns) == ["nombre", "nivel"]
    assert df.iloc[0]["nivel"] == 15


def test_nombres_columnas():
    assert modulo.nombres_columnas(_pokedex()) == ["nombre", "nivel", "tipo"]


def test_columna():
    col = modulo.columna(_pokedex(), "nivel")
    assert list(col) == [25, 90, 12, 70]


def test_cantidad_filas():
    assert modulo.cantidad_filas(_pokedex()) == 4


def test_primeras_filas():
    r = modulo.primeras_filas(_pokedex(), 2)
    assert len(r) == 2
    assert list(r["nombre"]) == ["Pikachu", "Charizard"]


def test_promedio_columna():
    assert modulo.promedio_columna(_pokedex(), "nivel") == (25 + 90 + 12 + 70) / 4


def test_agregar_columna():
    df = _pokedex()
    r = modulo.agregar_columna(df, "hp", [35, 78, 45, 160])
    assert "hp" in r.columns
    assert list(r["hp"]) == [35, 78, 45, 160]
    assert "hp" not in df.columns, "No modifiques el DataFrame original (usá .copy())"


def _df():
    return pd.DataFrame({"nombre": ["pikachu", "onix", "eevee"], "nivel": [25, 12, 18]})


def test_suma_columna():
    assert modulo.suma_columna(_df(), "nivel") == 55


def test_maximo_columna():
    assert modulo.maximo_columna(_df(), "nivel") == 25


def test_minimo_columna():
    assert modulo.minimo_columna(_df(), "nivel") == 12


def test_columna_a_lista():
    assert modulo.columna_a_lista(_df(), "nombre") == ["pikachu", "onix", "eevee"]


def test_cantidad_columnas():
    assert modulo.cantidad_columnas(_df()) == 2


def test_existe_columna():
    assert modulo.existe_columna(_df(), "nivel") is True
    assert modulo.existe_columna(_df(), "hp") is False


def test_contar_donde():
    assert modulo.contar_donde(_df(), "nivel", 15) == 2


def test_valores_ordenados():
    assert modulo.valores_ordenados(_df(), "nivel") == [12, 18, 25]


def test_fila_como_dict():
    assert modulo.fila_como_dict(_df(), 0) == {"nombre": "pikachu", "nivel": 25}


def test_renombrar_columnas():
    assert modulo.renombrar_columnas(_df(), {"nivel": "lvl"}) == ["nombre", "lvl"]


def test_mediana_columna():
    assert modulo.mediana_columna(_df(), "nivel") == 18.0
