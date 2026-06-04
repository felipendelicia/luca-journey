"""Tests del módulo agenda.estadisticas."""

from agenda.pokemon import Pokemon
from agenda.batallas import Batalla, Historial, GANO, PERDIO
from agenda import estadisticas


def _historial(resultados_y_pokemon):
    """Crea un historial a partir de pares (resultado, pokemon_usado)."""
    h = Historial()
    for resultado, poke in resultados_y_pokemon:
        h.registrar(Batalla("rival", resultado, poke))
    return h


def test_total_capturados():
    capturados = [Pokemon("Pikachu", "Electrico", 25), Pokemon("Onix", "Roca", 30)]
    assert estadisticas.total_capturados(capturados) == 2
    assert estadisticas.total_capturados([]) == 0


def test_porcentaje_victorias():
    h = _historial([(GANO, "Pikachu"), (GANO, "Pikachu"), (PERDIO, "Onix"), (PERDIO, "Onix")])
    assert estadisticas.porcentaje_victorias(h) == 50


def test_porcentaje_victorias_sin_batallas():
    h = Historial()
    assert estadisticas.porcentaje_victorias(h) == 0, "Sin batallas: 0% (no error)"


def test_pokemon_mas_usado():
    h = _historial([(GANO, "Pikachu"), (PERDIO, "Pikachu"), (GANO, "Onix")])
    assert estadisticas.pokemon_mas_usado(h) == "Pikachu"


def test_pokemon_mas_usado_sin_batallas():
    h = Historial()
    assert estadisticas.pokemon_mas_usado(h) is None


def test_resumen_completo():
    capturados = [Pokemon("Pikachu", "Electrico", 25)]
    h = _historial([(GANO, "Pikachu"), (PERDIO, "Pikachu")])
    r = estadisticas.resumen(capturados, h)
    assert r["total_capturados"] == 1
    assert r["batallas_totales"] == 2
    assert r["victorias"] == 1
    assert r["porcentaje_victorias"] == 50
    assert r["pokemon_mas_usado"] == "Pikachu"
