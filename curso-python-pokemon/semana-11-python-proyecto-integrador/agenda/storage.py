"""
agenda.storage — Persistencia en JSON.

Guarda y carga el "estado" de la agenda (un diccionario con capturados, equipo e
historial) en un archivo JSON.
"""

import json

# Estructura por defecto cuando no hay archivo todavía.
ESTADO_VACIO = {
    "capturados": [],   # lista de dicts de Pokémon
    "equipo": [],       # lista de nombres
    "batallas": [],     # lista de dicts de Batalla
}


def guardar(estado, ruta):
    """Guarda el diccionario 'estado' en el archivo JSON 'ruta'."""
    with open(ruta, "w", encoding="utf-8") as f:
        # indent=2 hace el JSON legible; ensure_ascii=False respeta tildes y ñ.
        json.dump(estado, f, indent=2, ensure_ascii=False)


def cargar(ruta):
    """
    Carga el estado desde 'ruta'. Si el archivo no existe o está corrupto,
    devuelve un estado vacío (sin romper el programa).
    """
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        return dict(ESTADO_VACIO)  # copia del estado vacío
    except json.JSONDecodeError:
        # El archivo existe pero está mal formado: arrancamos limpio.
        return dict(ESTADO_VACIO)

    # Nos aseguramos de que estén todas las claves esperadas.
    for clave in ESTADO_VACIO:
        datos.setdefault(clave, [])
    return datos
