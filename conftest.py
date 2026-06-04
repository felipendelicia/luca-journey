"""
conftest.py (raíz del curso) — Hace importable el paquete 'liga' (la Liga Pokémon)
desde los tests, agregando la raíz del curso a sys.path.
"""

import os
import sys

_RAIZ = os.path.dirname(__file__)
if _RAIZ not in sys.path:
    sys.path.insert(0, _RAIZ)
