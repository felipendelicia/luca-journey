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
