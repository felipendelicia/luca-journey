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
