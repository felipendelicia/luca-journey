"""📁 Soluciones — Archivos y rutas"""
from pathlib import Path
import os


def nombre_archivo(ruta):
    return Path(ruta).name


def extension(ruta):
    return Path(ruta).suffix


def cambiar_extension(ruta, ext):
    return str(Path(ruta).with_suffix(ext))


def guardar_y_leer(ruta, texto):
    Path(ruta).write_text(texto)
    return Path(ruta).read_text()


def directorio(ruta):
    return os.path.dirname(ruta)


def sin_extension(ruta):
    return os.path.splitext(ruta)[0]


def unir(carpeta, archivo):
    return os.path.join(carpeta, archivo)


def es_absoluta(ruta):
    return ruta.startswith("/")


def partes(ruta):
    return ruta.split("/")


def nombre_sin_ext(ruta):
    return os.path.splitext(os.path.basename(ruta))[0]


def tiene_extension(ruta, ext):
    return ruta.endswith(ext)


def cambiar_carpeta(ruta, nueva):
    return os.path.join(nueva, os.path.basename(ruta))


def normalizar_barras(ruta):
    return ruta.replace("\\", "/")


def agregar_sufijo(ruta, sufijo):
    base, ext = os.path.splitext(ruta)
    return base + sufijo + ext


def es_oculto(ruta):
    return os.path.basename(ruta).startswith(".")


def mismo_directorio(a, b):
    return os.path.dirname(a) == os.path.dirname(b)


def extension_minuscula(ruta):
    return os.path.splitext(ruta)[1].lower()


def contar_niveles(ruta):
    return len([p for p in ruta.split("/") if p])


def quitar_barra_final(ruta):
    return ruta.rstrip("/")


def es_tipo(ruta, exts):
    return os.path.splitext(ruta)[1] in exts
