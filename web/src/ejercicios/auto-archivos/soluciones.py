"""📁 Soluciones — Archivos y rutas"""
from pathlib import Path


def nombre_archivo(ruta):
    return Path(ruta).name


def extension(ruta):
    return Path(ruta).suffix


def cambiar_extension(ruta, ext):
    return str(Path(ruta).with_suffix(ext))


def guardar_y_leer(ruta, texto):
    Path(ruta).write_text(texto)
    return Path(ruta).read_text()
