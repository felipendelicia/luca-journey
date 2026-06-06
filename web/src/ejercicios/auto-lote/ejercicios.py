"""🔁 Ejercicios — Procesar carpetas en lote

El corazón de la automatización: hacerle lo MISMO a muchos archivos de una. Acá
trabajás sobre un "listado de carpeta" (una lista de nombres) y lo procesás en lote.
✅ Corregí cuando termines.
"""
from pathlib import Path


# Filtrar por extensión
# Dada una lista de nombres de archivo, devolvé solo los que terminan en `ext`.
# Ejemplo:  solo_extension(["a.py", "b.txt", "c.py"], ".py")  →  ["a.py", "c.py"]
def solo_extension(archivos, ext):
    """Devolvé los nombres que terminan en ext."""


# Contar por extensión
# Devolvé un diccionario que cuenta cuántos archivos hay de cada extensión (con punto).
# Ejemplo:  contar_por_extension(["a.py", "b.txt", "c.py"])  →  {".py": 2, ".txt": 1}
def contar_por_extension(archivos):
    """Devolvé un dict extensión → cantidad."""


# Renombrar en lote
# Devolvé la lista de nombres reemplazando en cada uno el texto `viejo` por `nuevo`.
# Ejemplo:  renombrar_lote(["IMG_1.png", "IMG_2.png"], "IMG", "foto")
#               →  ["foto_1.png", "foto_2.png"]
def renombrar_lote(archivos, viejo, nuevo):
    """Devolvé los nombres con viejo reemplazado por nuevo."""


# El más grande
# `archivos` es una lista de tuplas (nombre, tamaño). Devolvé el NOMBRE del archivo
# más grande. Si la lista está vacía, devolvé None.
# Ejemplo:  mas_grande([("a.txt", 10), ("b.txt", 99), ("c.txt", 5)])  →  "b.txt"
def mas_grande(archivos):
    """Devolvé el nombre del archivo de mayor tamaño, o None."""
