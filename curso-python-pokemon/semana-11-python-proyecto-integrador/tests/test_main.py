"""Tests de integración de agenda.app.App y agenda.ui."""

from agenda.app import App
from agenda import ui
from agenda.pokemon import Pokemon
from agenda.batallas import Batalla, GANO


def test_app_registrar_captura(tmp_path):
    app = App(ruta=str(tmp_path / "datos.json"))
    msg = app.registrar_captura("Pikachu", "Electrico", 25)
    assert "registrado" in msg
    assert len(app.capturados) == 1


def test_app_no_registra_duplicado(tmp_path):
    app = App(ruta=str(tmp_path / "datos.json"))
    app.registrar_captura("Pikachu", "Electrico", 25)
    msg = app.registrar_captura("Pikachu", "Electrico", 30)
    assert "ya estaba" in msg
    assert len(app.capturados) == 1


def test_app_registrar_batalla(tmp_path):
    app = App(ruta=str(tmp_path / "datos.json"))
    app.registrar_batalla("Brock", True, "Pikachu")
    assert app.historial.total() == 1
    assert app.historial.victorias() == 1


def test_app_persistencia_completa(tmp_path):
    ruta = str(tmp_path / "datos.json")
    # Creamos una app, cargamos datos y guardamos.
    app1 = App(ruta=ruta)
    app1.registrar_captura("Pikachu", "Electrico", 25)
    app1.registrar_captura("Onix", "Roca", 30)
    app1.equipo.agregar(app1.capturados[0])
    app1.registrar_batalla("Brock", True, "Pikachu")
    app1.guardar()

    # Una app nueva debería cargar exactamente lo guardado.
    app2 = App(ruta=ruta)
    assert len(app2.capturados) == 2
    assert app2.equipo.nombres() == ["Pikachu"]
    assert app2.historial.total() == 1
    assert app2.historial.victorias() == 1


def test_ui_formatear_pokemon():
    p = Pokemon("Pikachu", "Electrico", 25, "2024-01-01")
    linea = ui.formatear_pokemon(p)
    assert "Pikachu" in linea
    assert "Electrico" in linea


def test_ui_formatear_estadisticas():
    resumen = {
        "total_capturados": 2,
        "batallas_totales": 4,
        "victorias": 3,
        "derrotas": 1,
        "porcentaje_victorias": 75,
        "pokemon_mas_usado": "Pikachu",
    }
    texto = ui.formatear_estadisticas(resumen)
    assert "75%" in texto
    assert "Pikachu" in texto


def test_ui_lista_vacia():
    assert "todavía no" in ui.formatear_lista_capturados([])
