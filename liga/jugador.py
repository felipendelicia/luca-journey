"""
liga.jugador — Lanza los juegos interactivos de cada capítulo.

Cada semana (y la misión de Git) tiene un archivo 'interactivo.py' con una función
'jugar()'. Este módulo permite ejecutarlo desde la Liga, sin tener que abrir cada
archivo a mano.
"""

import importlib.util
import os

from . import datos

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def ruta_interactivo(capitulo):
    """Devuelve la ruta al interactivo.py de un capítulo."""
    return os.path.join(BASE_DIR, capitulo["dir"], "interactivo.py")


def tiene_interactivo(capitulo):
    """True si el capítulo tiene un juego interactivo."""
    return os.path.exists(ruta_interactivo(capitulo))


def jugables():
    """Lista de capítulos (semanas + bonus) que tienen juego interactivo."""
    todos = list(datos.SEMANAS) + list(datos.BONUS)
    return [c for c in todos if tiene_interactivo(c)]


def lanzar(capitulo):
    """
    Carga el interactivo.py del capítulo y ejecuta su 'jugar()' (o 'run()').
    Devuelve True si se pudo lanzar. Bloquea hasta que el jugador sale del juego.
    """
    ruta = ruta_interactivo(capitulo)
    if not os.path.exists(ruta):
        return False
    spec = importlib.util.spec_from_file_location(
        f"interactivo_{capitulo['id']}", ruta
    )
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    funcion = getattr(modulo, "jugar", None) or getattr(modulo, "run", None)
    if funcion is None:
        return False
    funcion()
    return True
