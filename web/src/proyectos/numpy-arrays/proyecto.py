# Líder Falkner — Estadísticas de combate (solución de referencia).
# El preamble (STATS_EQUIPO, NOMBRES) está en meta.json y se antepone al corregir.
import numpy as np


def crear_stats(niveles):
    return np.array(niveles)


def estadisticas(arr):
    return {
        "total": int(arr.sum()),
        "promedio": float(arr.mean()),
        "maximo": int(arr.max()),
        "minimo": int(arr.min()),
    }


def fuertes_y_debiles(arr, umbral):
    return arr[arr >= umbral], arr[arr < umbral]


def resumen_equipo(nombres, stats):
    resultado = ["%s: %d pts" % (n, s) for n, s in zip(nombres, stats)]
    resultado.append("Promedio: %.1f pts" % stats.mean())
    return resultado
