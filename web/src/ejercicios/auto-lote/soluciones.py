"""🔁 Soluciones — Procesar carpetas en lote"""
from pathlib import Path


def solo_extension(archivos, ext):
    return [a for a in archivos if a.endswith(ext)]


def contar_por_extension(archivos):
    conteo = {}
    for a in archivos:
        ext = Path(a).suffix
        conteo[ext] = conteo.get(ext, 0) + 1
    return conteo


def renombrar_lote(archivos, viejo, nuevo):
    return [a.replace(viejo, nuevo) for a in archivos]


def mas_grande(archivos):
    if not archivos:
        return None
    return max(archivos, key=lambda par: par[1])[0]
