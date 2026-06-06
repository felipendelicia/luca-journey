"""📁 Ejercicios — Archivos y rutas

Automatizar = trabajar con archivos. `pathlib` arma y descompone rutas sin pelear con
las barras, y te deja leer/escribir en una línea. ✅ Corregí cuando termines.
"""
from pathlib import Path


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
