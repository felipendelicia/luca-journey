"""conftest.py — hace importable el paquete agenda_entrenador en los tests."""

import os
import sys

_DIR = os.path.dirname(__file__)
if _DIR not in sys.path:
    sys.path.insert(0, _DIR)
