"""
liga.almacen — Guarda y carga el progreso del jugador en JSON.
"""

import json
import os

from . import progreso

# El progreso se guarda en la raíz del curso, como 'progreso.json'.
RUTA_DEFECTO = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "progreso.json"
)


def cargar(ruta=RUTA_DEFECTO):
    """Carga el estado del jugador, o uno nuevo si no existe el archivo."""
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            estado = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return progreso.estado_inicial()

    # Nos aseguramos de que tenga todas las claves esperadas (por si es viejo).
    base = progreso.estado_inicial(estado.get("nombre", "Entrenador"))
    base.update(estado)
    return base


def guardar(estado, ruta=RUTA_DEFECTO):
    """Guarda el estado del jugador en JSON."""
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)
