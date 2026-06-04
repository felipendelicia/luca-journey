"""🧪 Tests — matplotlib: Gráficos"""
import importlib.util
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"mpl_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def _ax():
    fig, ax = plt.subplots()
    return ax


def test_dibujar_barras():
    ax = modulo.dibujar_barras(_ax(), ["a", "b", "c"], [10, 20, 30])
    alturas = sorted(p.get_height() for p in ax.patches)
    assert alturas == [10, 20, 30]


def test_poner_titulo():
    ax = modulo.poner_titulo(_ax(), "Niveles de mi equipo")
    assert ax.get_title() == "Niveles de mi equipo"


def test_poner_etiquetas():
    ax = modulo.poner_etiquetas(_ax(), "Pokémon", "Nivel")
    assert ax.get_xlabel() == "Pokémon"
    assert ax.get_ylabel() == "Nivel"


def test_dibujar_linea():
    ax = modulo.dibujar_linea(_ax(), [1, 2, 3], [10, 20, 30])
    assert len(ax.lines) >= 1
    assert list(ax.lines[0].get_ydata()) == [10, 20, 30]


def test_dibujar_dispersion():
    ax = modulo.dibujar_dispersion(_ax(), [1, 2, 3], [4, 5, 6])
    assert len(ax.collections) >= 1


def test_dibujar_histograma():
    ax = modulo.dibujar_histograma(_ax(), [1, 1, 2, 3, 3, 3, 4])
    assert len(ax.patches) > 0
