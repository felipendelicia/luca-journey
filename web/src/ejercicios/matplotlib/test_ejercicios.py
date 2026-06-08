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


def test_poner_limites_x():
    ax = modulo.poner_limites_x(_ax(), 0, 10)
    assert ax.get_xlim() == (0.0, 10.0)


def test_poner_limites_y():
    ax = modulo.poner_limites_y(_ax(), 0, 50)
    assert ax.get_ylim() == (0.0, 50.0)


def test_dibujar_barras_horizontales():
    ax = modulo.dibujar_barras_horizontales(_ax(), ["a", "b", "c"], [10, 20, 30])
    anchos = sorted(p.get_width() for p in ax.patches)
    assert anchos == [10, 20, 30]


def test_dibujar_torta():
    ax = modulo.dibujar_torta(_ax(), [10, 20, 30])
    assert len(ax.patches) == 3


def test_dibujar_dos_lineas():
    ax = modulo.dibujar_dos_lineas(_ax(), [1, 2], [1, 2], [3, 4])
    assert len(ax.lines) == 2


def test_cantidad_lineas():
    ax = _ax()
    ax.plot([1, 2], [3, 4])
    assert modulo.cantidad_lineas(ax) == 1


def test_cantidad_barras():
    ax = _ax()
    ax.bar(["a", "b"], [1, 2])
    assert modulo.cantidad_barras(ax) == 2


def test_titulo_actual():
    ax = _ax()
    ax.set_title("Hola")
    assert modulo.titulo_actual(ax) == "Hola"


def test_etiqueta_x_actual():
    ax = _ax()
    ax.set_xlabel("X")
    assert modulo.etiqueta_x_actual(ax) == "X"


def test_limpiar():
    ax = _ax()
    ax.plot([1, 2], [3, 4])
    modulo.limpiar(ax)
    assert len(ax.lines) == 0


def test_poner_titulo_y_etiquetas():
    ax = modulo.poner_titulo_y_etiquetas(_ax(), "T", "X", "Y")
    assert ax.get_title() == "T"
    assert ax.get_xlabel() == "X"
    assert ax.get_ylabel() == "Y"


def test_agregar_punto():
    ax = modulo.agregar_punto(_ax(), 1, 2)
    assert len(ax.collections) >= 1


def test_invertir_eje_y():
    ax = _ax()
    ax.set_ylim(0, 10)
    modulo.invertir_eje_y(ax)
    lo, hi = ax.get_ylim()
    assert lo > hi


def test_marcar_horizontal():
    ax = modulo.marcar_horizontal(_ax(), 5)
    assert len(ax.lines) >= 1
