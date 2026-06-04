"""
conftest.py — Configuración de pytest para la Agenda del Entrenador.

Agrega esta carpeta a sys.path para que los tests puedan importar el paquete
'agenda' y el módulo 'main' como en un proyecto real.
"""

import os
import sys

_DIR = os.path.dirname(__file__)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)
