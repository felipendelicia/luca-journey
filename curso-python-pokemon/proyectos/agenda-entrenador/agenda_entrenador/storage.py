"""agenda_entrenador.storage — Persistencia en JSON."""

import json

ESTADO_VACIO = {"capturados": [], "equipo": [], "batallas": []}


def guardar(estado, ruta):
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(estado, f, indent=2, ensure_ascii=False)


def cargar(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    except FileNotFoundError:
        return dict(ESTADO_VACIO)
    except json.JSONDecodeError:
        return dict(ESTADO_VACIO)
    for clave in ESTADO_VACIO:
        datos.setdefault(clave, [])
    return datos
