"""🧪 Tests — Fechas, esperas y agendado"""
import importlib.util
import os
from datetime import date, datetime

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"auto_tiempo_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


modulo = _cargar(os.environ.get("CURSO_MODULO", "soluciones"))


def test_dias_entre():
    assert modulo.dias_entre(date(2024, 1, 1), date(2024, 1, 8)) == 7
    assert modulo.dias_entre(date(2024, 1, 8), date(2024, 1, 1)) == -7


def test_formatear():
    assert modulo.formatear(date(2024, 3, 9)) == "2024-03-09"


def test_es_fin_de_semana():
    assert modulo.es_fin_de_semana(date(2024, 3, 9)) is True   # sábado
    assert modulo.es_fin_de_semana(date(2024, 3, 11)) is False  # lunes


def test_toca_correr():
    assert modulo.toca_correr(datetime(2024, 1, 1, 0, 0), datetime(2024, 1, 1, 7, 0), 6) is True
    assert modulo.toca_correr(datetime(2024, 1, 1, 0, 0), datetime(2024, 1, 1, 3, 0), 6) is False
