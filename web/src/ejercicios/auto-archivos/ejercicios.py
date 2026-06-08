"""📁 Ejercicios — Archivos y rutas

Automatizar = trabajar con archivos. `pathlib` arma y descompone rutas sin pelear con
las barras, y te deja leer/escribir en una línea. ✅ Corregí cuando termines.
"""
from pathlib import Path
import os


# Nombre del archivo
# Dada una ruta como "datos/pokedex/kanto.csv", devolvé SOLO el nombre del archivo
# final ("kanto.csv"), sin las carpetas. (Path(...).name hace justo esto.)
# Ejemplo:  nombre_archivo("datos/pokedex/kanto.csv")  →  "kanto.csv"
def nombre_archivo(ruta):
    """Devolvé el nombre final de la ruta."""


# Extensión
# Devolvé la extensión del archivo, con el punto incluido (".csv"). Si no tiene
# extensión, devolvé "" (texto vacío).
# Ejemplo:  extension("kanto.csv")  →  ".csv"   ·   extension("LEEME")  →  ""
def extension(ruta):
    """Devolvé el sufijo/extensión de la ruta."""


# Cambiar la extensión
# Devolvé la misma ruta pero con otra extensión `ext` (que viene con punto, ".json").
# Devolvé el resultado como TEXTO (str).
# Ejemplo:  cambiar_extension("kanto.csv", ".json")  →  "kanto.json"
def cambiar_extension(ruta, ext):
    """Devolvé la ruta con la nueva extensión, como str."""


# Guardar y leer
# Escribí `texto` en el archivo `ruta` y después leelo de vuelta, devolviendo su
# contenido. (Path(ruta).write_text(...) y .read_text() te sirven.)
# Ejemplo:  guardar_y_leer("nota.txt", "hola")  →  "hola"
def guardar_y_leer(ruta, texto):
    """Escribí texto en ruta y devolvé lo leído."""


# Directorio
# Devolvé la carpeta de una ruta (todo menos el nombre del archivo).
# Ejemplo:  directorio("/home/ash/pokedex.txt")  →  "/home/ash"
def directorio(ruta):
    """Devolvé la carpeta de la ruta."""
    # TU CÓDIGO ACÁ


# Sin extensión
# Devolvé la ruta sin la extensión.
# Ejemplo:  sin_extension("/home/ash/pokedex.txt")  →  "/home/ash/pokedex"
def sin_extension(ruta):
    """Devolvé la ruta sin la extensión."""
    # TU CÓDIGO ACÁ


# Unir
# Uní una carpeta y un archivo en una ruta (usá os.path.join).
# Ejemplo:  unir("/home/ash", "pokedex.txt")  →  "/home/ash/pokedex.txt"
def unir(carpeta, archivo):
    """Devolvé carpeta y archivo unidos."""
    # TU CÓDIGO ACÁ


# ¿Es absoluta?
# Devolvé True si la ruta empieza con "/".
def es_absoluta(ruta):
    """Devolvé True si la ruta es absoluta."""
    # TU CÓDIGO ACÁ


# Partes
# Devolvé una lista con las partes de la ruta separadas por "/".
# Ejemplo:  partes("home/ash/x.txt")  →  ["home", "ash", "x.txt"]
def partes(ruta):
    """Devolvé las partes de la ruta."""
    # TU CÓDIGO ACÁ


# Nombre sin extensión
# Devolvé solo el nombre del archivo, sin carpeta ni extensión.
# Ejemplo:  nombre_sin_ext("/home/ash/pokedex.txt")  →  "pokedex"
def nombre_sin_ext(ruta):
    """Devolvé el nombre del archivo sin extensión."""
    # TU CÓDIGO ACÁ


# ¿Tiene esa extensión?
# Devolvé True si la ruta termina con `ext`.
# Ejemplo:  tiene_extension("a.json", ".json")  →  True
def tiene_extension(ruta, ext):
    """Devolvé True si la ruta termina con ext."""
    # TU CÓDIGO ACÁ


# Cambiar de carpeta
# Devolvé la ruta con el mismo nombre de archivo pero en la carpeta `nueva`.
# Ejemplo:  cambiar_carpeta("/viejo/x.txt", "/nuevo")  →  "/nuevo/x.txt"
def cambiar_carpeta(ruta, nueva):
    """Devolvé el archivo en la carpeta nueva."""
    # TU CÓDIGO ACÁ


# Normalizar barras
# Cambiá las barras invertidas "\\" por barras normales "/".
# Ejemplo:  normalizar_barras("home\\ash\\x.txt")  →  "home/ash/x.txt"
def normalizar_barras(ruta):
    """Cambiá '\\' por '/'."""
    # TU CÓDIGO ACÁ


# Agregar un sufijo
# Insertá `sufijo` antes de la extensión.
# Ejemplo:  agregar_sufijo("foto.png", "_chica")  →  "foto_chica.png"
def agregar_sufijo(ruta, sufijo):
    """Insertá el sufijo antes de la extensión."""
    # TU CÓDIGO ACÁ


# ¿Es oculto?
# Devolvé True si el nombre del archivo empieza con un punto.
# Ejemplo:  es_oculto("/home/ash/.config")  →  True
def es_oculto(ruta):
    """Devolvé True si el archivo es oculto."""
    # TU CÓDIGO ACÁ


# ¿Mismo directorio?
# Devolvé True si las dos rutas están en la misma carpeta.
def mismo_directorio(a, b):
    """Devolvé True si a y b están en la misma carpeta."""
    # TU CÓDIGO ACÁ


# Extensión en minúscula
# Devolvé la extensión (con el punto) en minúsculas.
# Ejemplo:  extension_minuscula("FOTO.PNG")  →  ".png"
def extension_minuscula(ruta):
    """Devolvé la extensión en minúsculas."""
    # TU CÓDIGO ACÁ


# Contar niveles
# Devolvé cuántas partes no vacías tiene la ruta.
# Ejemplo:  contar_niveles("/home/ash/x.txt")  →  3
def contar_niveles(ruta):
    """Devolvé cuántas partes no vacías hay."""
    # TU CÓDIGO ACÁ


# Quitar barra final
# Devolvé la ruta sin las barras "/" del final.
# Ejemplo:  quitar_barra_final("/home/ash/")  →  "/home/ash"
def quitar_barra_final(ruta):
    """Devolvé la ruta sin '/' al final."""
    # TU CÓDIGO ACÁ


# ¿Es de alguno de estos tipos?
# Devolvé True si la extensión de la ruta está en la lista `exts`.
# Ejemplo:  es_tipo("a.png", [".png", ".jpg"])  →  True
def es_tipo(ruta, exts):
    """Devolvé True si la extensión está en exts."""
    # TU CÓDIGO ACÁ
