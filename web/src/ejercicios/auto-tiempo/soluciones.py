"""⏰ Soluciones — Fechas, esperas y agendado"""
from datetime import date, datetime, timedelta


def dias_entre(d1, d2):
    return (d2 - d1).days


def formatear(dt):
    return dt.strftime("%Y-%m-%d")


def es_fin_de_semana(d):
    return d.weekday() >= 5


def toca_correr(ultima, ahora, cada_horas):
    return (ahora - ultima).total_seconds() >= cada_horas * 3600


def dia_de_semana(d):
    dias = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]
    return dias[d.weekday()]


def sumar_dias(d, n):
    return d + timedelta(days=n)


def restar_dias(d, n):
    return d - timedelta(days=n)


def es_pasado(d, hoy):
    return d < hoy


def dias_hasta(d, objetivo):
    return (objetivo - d).days


def mismo_mes(a, b):
    return a.year == b.year and a.month == b.month


def anio_de(d):
    return d.year


def mes_de(d):
    return d.month


def es_bisiesto(anio):
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def mas_reciente(fechas):
    return max(fechas)


def mas_antigua(fechas):
    return min(fechas)


def ordenar_fechas(fechas):
    return sorted(fechas)


def cuantos_fines_de_semana(fechas):
    return sum(1 for d in fechas if d.weekday() >= 5)


def formatear_hora(dt):
    return dt.strftime("%H:%M")


def proximo_lunes(d):
    dias = (7 - d.weekday()) % 7
    if dias == 0:
        dias = 7
    return d + timedelta(days=dias)


def cantidad_dias_laborales(fechas):
    return sum(1 for d in fechas if d.weekday() < 5)
