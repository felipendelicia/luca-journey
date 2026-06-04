"""
liga.logros — Logros (achievements) que se desbloquean al cumplir hitos.

Cada logro tiene una función 'check(estado)' que devuelve True cuando se cumple.
"""

from . import progreso, medallas, combates


# Cada logro: id, nombre, emoji, descripción y la condición para desbloquearlo.
LOGROS = [
    {
        "id": "primera_victoria",
        "nombre": "Primera Victoria",
        "emoji": "🎉",
        "desc": "Pasaste tu primer test.",
        "check": lambda e: progreso.total_tests_pasados(e) >= 1,
    },
    {
        "id": "perfeccionista",
        "nombre": "Perfeccionista",
        "emoji": "✨",
        "desc": "Completaste una semana al 100%.",
        "check": lambda e: len(progreso.semanas_completas(e)) >= 1,
    },
    {
        "id": "maestro_linux",
        "nombre": "Maestro de Linux",
        "emoji": "🐧",
        "desc": "Completaste las semanas 1 y 2.",
        "check": lambda e: progreso.semana_completa(e, 1) and progreso.semana_completa(e, 2),
    },
    {
        "id": "pythonista",
        "nombre": "Pythonista",
        "emoji": "🐍",
        "desc": "Completaste 5 semanas.",
        "check": lambda e: len(progreso.semanas_completas(e)) >= 5,
    },
    {
        "id": "medio_camino",
        "nombre": "Medio Camino",
        "emoji": "🛣️",
        "desc": "Completaste 6 semanas. ¡Vas por la mitad!",
        "check": lambda e: len(progreso.semanas_completas(e)) >= 6,
    },
    {
        "id": "constante",
        "nombre": "Constante",
        "emoji": "🔥",
        "desc": "Racha de 3 días seguidos.",
        "check": lambda e: e.get("racha", 0) >= 3,
    },
    {
        "id": "imparable",
        "nombre": "Imparable",
        "emoji": "🚀",
        "desc": "Racha de 7 días seguidos.",
        "check": lambda e: e.get("racha", 0) >= 7,
    },
    {
        "id": "nivel_10",
        "nombre": "Veterano",
        "emoji": "🎖️",
        "desc": "Llegaste al nivel 10.",
        "check": lambda e: progreso.nivel_desde_exp(progreso.exp_total(e)) >= 10,
    },
    {
        "id": "coleccionista",
        "nombre": "Coleccionista de Medallas",
        "emoji": "🏅",
        "desc": "Conseguiste 4 medallas de gimnasio.",
        "check": lambda e: len(e.get("medallas", [])) >= 4,
    },
    {
        "id": "campeon",
        "nombre": "¡CAMPEÓN!",
        "emoji": "🏆",
        "desc": "Conseguiste las 8 medallas y completaste el viaje.",
        "check": lambda e: medallas.es_campeon(e),
    },
    {
        "id": "viajero_del_tiempo",
        "nombre": "Viajero del Tiempo",
        "emoji": "🔀",
        "desc": "Completaste la misión bonus de Git.",
        "check": lambda e: progreso.semana_completa(e, "git"),
    },
    {
        "id": "domador",
        "nombre": "Domador de Gimnasios",
        "emoji": "⚔️",
        "desc": "Venciste a los 8 líderes de gimnasio.",
        "check": lambda e: combates.todos_vencidos(e),
    },
]


def chequear_nuevos(estado):
    """
    Desbloquea los logros recién cumplidos (los agrega a estado["logros"]).
    Devuelve la lista de logros (dicts) nuevos.
    """
    nuevos = []
    for logro in LOGROS:
        if logro["id"] in estado["logros"]:
            continue
        if logro["check"](estado):
            estado["logros"].append(logro["id"])
            nuevos.append(logro)
    return nuevos


def logro_por_id(lid):
    for logro in LOGROS:
        if logro["id"] == lid:
            return logro
    return None
