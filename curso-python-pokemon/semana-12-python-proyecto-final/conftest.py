"""
conftest.py — Configuración de pytest para la Pokédex Web.

Agrega esta carpeta a sys.path para poder importar el paquete 'pokedex_web'.
"""

import os
import sys

_DIR = os.path.dirname(__file__)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)
