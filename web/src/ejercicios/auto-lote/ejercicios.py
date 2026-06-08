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


# Solo imágenes
# Devolvé los archivos cuya extensión sea .png, .jpg o .gif.
def solo_imagenes(archivos):
    """Devolvé los archivos de imagen."""
    # TU CÓDIGO ACÁ


# Nombres sin extensión
# Devolvé cada nombre sin su extensión.
# Ejemplo:  nombres_sin_extension(["a.py", "b.txt"])  →  ["a", "b"]
def nombres_sin_extension(archivos):
    """Devolvé los nombres sin extensión."""
    # TU CÓDIGO ACÁ


# Agregar prefijo
# Devolvé cada nombre con `prefijo` adelante.
# Ejemplo:  agregar_prefijo(["a.py"], "viejo_")  →  ["viejo_a.py"]
def agregar_prefijo(archivos, prefijo):
    """Devolvé los nombres con el prefijo adelante."""
    # TU CÓDIGO ACÁ


# Tamaño total
# `archivos` es una lista de tuplas (nombre, tamaño). Devolvé la suma de los tamaños.
def tamano_total(archivos):
    """Devolvé la suma de los tamaños."""
    # TU CÓDIGO ACÁ


# El más chico
# Devolvé el NOMBRE del archivo de menor tamaño (lista de tuplas), o None si está vacía.
def mas_chico(archivos):
    """Devolvé el nombre del más chico, o None."""
    # TU CÓDIGO ACÁ


# Ordenar por tamaño
# Devolvé los NOMBRES ordenados de mayor a menor tamaño (lista de tuplas).
# Ejemplo:  ordenar_por_tamano([("a", 10), ("b", 99), ("c", 5)])  →  ["b", "a", "c"]
def ordenar_por_tamano(archivos):
    """Devolvé los nombres ordenados por tamaño (desc)."""
    # TU CÓDIGO ACÁ


# Filtrar mayores a
# Devolvé los NOMBRES de los archivos con tamaño ESTRICTAMENTE mayor que `minimo` (tuplas).
def filtrar_mayores_a(archivos, minimo):
    """Devolvé los nombres de tamaño > minimo."""
    # TU CÓDIGO ACÁ


# Extensiones únicas
# Devolvé una lista ORDENADA con las extensiones distintas (con punto).
# Ejemplo:  extensiones_unicas(["a.py", "b.txt", "c.py"])  →  [".py", ".txt"]
def extensiones_unicas(archivos):
    """Devolvé las extensiones distintas, ordenadas."""
    # TU CÓDIGO ACÁ


# Contar
# Devolvé cuántos archivos hay.
def contar(archivos):
    """Devolvé la cantidad de archivos."""
    # TU CÓDIGO ACÁ


# Quitar duplicados
# Devolvé los nombres sin repetir, en orden de aparición.
def quitar_duplicados(archivos):
    """Devolvé los nombres sin repetir."""
    # TU CÓDIGO ACÁ


# ¿Todos tienen esa extensión?
# Devolvé True si TODOS los nombres terminan en `ext`.
def tienen_extension(archivos, ext):
    """Devolvé True si todos terminan en ext."""
    # TU CÓDIGO ACÁ


# Cambiar todas las extensiones
# Devolvé los nombres con su extensión cambiada a `ext`.
# Ejemplo:  cambiar_todas_extensiones(["a.txt", "b.txt"], ".md")  →  ["a.md", "b.md"]
def cambiar_todas_extensiones(archivos, ext):
    """Devolvé los nombres con la extensión cambiada."""
    # TU CÓDIGO ACÁ


# Promedio de tamaño
# Devolvé el tamaño promedio (lista de tuplas).
def promedio_tamano(archivos):
    """Devolvé el tamaño promedio."""
    # TU CÓDIGO ACÁ


# Nombres largos
# Devolvé los nombres con más de `n` caracteres.
def nombres_largos(archivos, n):
    """Devolvé los nombres de más de n caracteres."""
    # TU CÓDIGO ACÁ


# Agrupar por extensión
# Devolvé un dict extensión → lista de nombres con esa extensión (en orden de aparición).
def agrupar_por_extension(archivos):
    """Devolvé un dict extensión → lista de nombres."""
    # TU CÓDIGO ACÁ


# ¿Hay algún archivo con esa extensión?
# Devolvé True si al menos un nombre termina en `ext`.
def hay_extension(archivos, ext):
    """Devolvé True si hay alguno con esa extensión."""
    # TU CÓDIGO ACÁ
