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


def test_dia_de_semana():
    assert modulo.dia_de_semana(date(2024, 3, 9)) == "sabado"
    assert modulo.dia_de_semana(date(2024, 3, 11)) == "lunes"


def test_sumar_dias():
    assert modulo.sumar_dias(date(2024, 1, 1), 7) == date(2024, 1, 8)


def test_restar_dias():
    assert modulo.restar_dias(date(2024, 1, 8), 7) == date(2024, 1, 1)


def test_es_pasado():
    assert modulo.es_pasado(date(2024, 1, 1), date(2024, 1, 2)) is True
    assert modulo.es_pasado(date(2024, 1, 3), date(2024, 1, 2)) is False


def test_dias_hasta():
    assert modulo.dias_hasta(date(2024, 1, 1), date(2024, 1, 8)) == 7


def test_mismo_mes():
    assert modulo.mismo_mes(date(2024, 3, 1), date(2024, 3, 28)) is True
    assert modulo.mismo_mes(date(2024, 3, 1), date(2024, 4, 1)) is False


def test_anio_de():
    assert modulo.anio_de(date(2024, 3, 9)) == 2024


def test_mes_de():
    assert modulo.mes_de(date(2024, 3, 9)) == 3


def test_es_bisiesto():
    assert modulo.es_bisiesto(2024) is True
    assert modulo.es_bisiesto(1900) is False


def test_mas_reciente():
    assert modulo.mas_reciente([date(2024, 1, 1), date(2024, 5, 1)]) == date(2024, 5, 1)


def test_mas_antigua():
    assert modulo.mas_antigua([date(2024, 1, 1), date(2024, 5, 1)]) == date(2024, 1, 1)


def test_ordenar_fechas():
    assert modulo.ordenar_fechas([date(2024, 5, 1), date(2024, 1, 1)]) == [date(2024, 1, 1), date(2024, 5, 1)]


def test_cuantos_fines_de_semana():
    fechas = [date(2024, 3, 9), date(2024, 3, 10), date(2024, 3, 11)]  # sab, dom, lun
    assert modulo.cuantos_fines_de_semana(fechas) == 2


def test_formatear_hora():
    assert modulo.formatear_hora(datetime(2024, 1, 1, 14, 30)) == "14:30"


def test_proximo_lunes():
    assert modulo.proximo_lunes(date(2024, 3, 9)) == date(2024, 3, 11)  # sábado → lunes


def test_cantidad_dias_laborales():
    fechas = [date(2024, 3, 9), date(2024, 3, 11), date(2024, 3, 12)]  # sab, lun, mar
    assert modulo.cantidad_dias_laborales(fechas) == 2
