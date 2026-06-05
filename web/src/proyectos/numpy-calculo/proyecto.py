# Líder Bugsy — Análisis de poder de combate (solución de referencia).
# El preamble (STATS_BUGSY) está en meta.json y se antepone al corregir.
import numpy as np


def normalizar(arr):
    return (arr - arr.min()) / (arr.max() - arr.min())


def por_encima_promedio(arr):
    return arr[arr > arr.mean()]


def comparar_equipos(a, b):
    ganadas_a = int((a > b).sum())
    ganadas_b = int((b > a).sum())
    return (ganadas_a, ganadas_b)


def informe_poder(stats):
    norm = normalizar(stats)
    sobre = int((stats > stats.mean()).sum())
    puntuacion = round(float(norm.sum()), 2)
    return {"normalizadas": norm, "sobre_promedio": sobre, "puntuacion": puntuacion}
