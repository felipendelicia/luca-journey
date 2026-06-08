"""🧪 Tests — pandas: Selección y filtrado"""
import importlib.util
import os

import pandas as pd

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"pdsel_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _pokedex():
    return pd.DataFrame({
        "nombre": ["Pikachu", "Charizard", "Bulbasaur", "Snorlax"],
        "nivel": [25, 90, 12, 70],
        "tipo": ["Electrico", "Fuego", "Planta", "Normal"],
        "hp": [35, 78, 45, 160],
    })


def test_fila_por_posicion():
    f = modulo.fila_por_posicion(_pokedex(), 1)
    assert f["nombre"] == "Charizard"


def test_filtrar_nivel():
    r = modulo.filtrar_nivel(_pokedex(), 70)
    assert sorted(r["nombre"]) == ["Charizard", "Snorlax"]


def test_de_tipo():
    r = modulo.de_tipo(_pokedex(), "Fuego")
    assert list(r["nombre"]) == ["Charizard"]


def test_ordenar_por_nivel():
    r = modulo.ordenar_por_nivel(_pokedex())
    assert list(r["nombre"]) == ["Charizard", "Snorlax", "Pikachu", "Bulbasaur"]


def test_nombres_fuertes():
    r = modulo.nombres_fuertes(_pokedex(), 50)
    assert isinstance(r, list)
    assert sorted(r) == ["Charizard", "Snorlax"]


def test_solo_columnas():
    r = modulo.solo_columnas(_pokedex(), ["nombre", "hp"])
    assert list(r.columns) == ["nombre", "hp"]


def test_quitar_columna():
    df = _pokedex()
    r = modulo.quitar_columna(df, "hp")
    assert "hp" not in r.columns
    assert "hp" in df.columns, "No modifiques el original"


def test_el_mas_fuerte():
    assert modulo.el_mas_fuerte(_pokedex()) == "Charizard"


def _dfs():
    return pd.DataFrame({
        "nombre": ["pikachu", "onix", "eevee", "staryu"],
        "tipo": ["electrico", "roca", "normal", "agua"],
        "nivel": [25, 12, 18, 30],
    })


def test_nombres():
    assert modulo.nombres(_dfs()) == ["pikachu", "onix", "eevee", "staryu"]


def test_valor_en():
    assert modulo.valor_en(_dfs(), 0, "nivel") == 25


def test_ultima_fila():
    assert modulo.ultima_fila(_dfs()) == {"nombre": "staryu", "tipo": "agua", "nivel": 30}


def test_mas_debil():
    assert modulo.mas_debil(_dfs())["nombre"] == "onix"


def test_nivel_de():
    assert modulo.nivel_de(_dfs(), "onix") == 12
    assert modulo.nivel_de(_dfs(), "mew") is None, "Si no está, devolvé None"


def test_existe_nombre():
    assert modulo.existe_nombre(_dfs(), "eevee") is True
    assert modulo.existe_nombre(_dfs(), "mew") is False


def test_primeros_nombres():
    assert modulo.primeros_nombres(_dfs(), 2) == ["pikachu", "onix"]


def test_ordenar_nombres():
    assert modulo.ordenar_nombres(_dfs()) == ["eevee", "onix", "pikachu", "staryu"]


def test_contar_tipo():
    assert modulo.contar_tipo(_dfs(), "agua") == 1


def test_niveles_entre():
    assert modulo.niveles_entre(_dfs(), 15, 30) == ["pikachu", "eevee", "staryu"]


def test_top_niveles():
    assert modulo.top_niveles(_dfs(), 2) == [30, 25]


def test_nombres_de_tipo():
    assert modulo.nombres_de_tipo(_dfs(), "agua") == ["staryu"]
