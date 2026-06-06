import ejercicios
from datetime import datetime


def test_minutos():
    assert ejercicios.minutos_entre(datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 11, 30)) == 90
    assert ejercicios.minutos_entre(datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 10, 0)) == 0


def test_vencida():
    assert ejercicios.vencida(datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 10, 5)) is True
    assert ejercicios.vencida(datetime(2024, 1, 1, 10, 0), datetime(2024, 1, 1, 9, 0)) is False


def test_proxima():
    assert ejercicios.proxima(datetime(2024, 1, 1, 10, 0), 15) == datetime(2024, 1, 1, 10, 15)


def test_pendientes():
    t = [("backup", datetime(2024, 1, 1, 9, 0)), ("reporte", datetime(2024, 1, 1, 12, 0))]
    assert ejercicios.pendientes(t, datetime(2024, 1, 1, 10, 0)) == ["backup"]
