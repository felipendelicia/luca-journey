"""
liga.combates — Los Combates de Gimnasio (jefes).

Cada gimnasio tiene un combate: un desafío integrador (en combates/desafios.py).
Se desbloquea cuando tenés la medalla de ese gimnasio. Vencerlo da EXP extra.
"""

# Cuánta EXP da vencer a un líder de gimnasio.
EXP_POR_COMBATE = 120

# Un combate por gimnasio. 'filtro' selecciona sus tests con pytest -k.
# dir/archivo/objetivo se usan igual que en datos.SEMANAS (los lee el evaluador).
COMBATES = [
    {"id": "roca",     "lider": "Brock",       "emoji": "🪨", "reto": "Organizar archivos por tipo"},
    {"id": "cascada",  "lider": "Misty",       "emoji": "💧", "reto": "Un duelo por turnos"},
    {"id": "trueno",   "lider": "Tnte. Surge", "emoji": "⚡", "reto": "Aplicar una función N veces"},
    {"id": "arcoiris", "lider": "Erika",       "emoji": "🌈", "reto": "Parsear un equipo desde texto"},
    {"id": "alma",     "lider": "Koga",        "emoji": "💜", "reto": "Programar una Mochila (POO)"},
    {"id": "pantano",  "lider": "Sabrina",     "emoji": "🔮", "reto": "Calcular estadísticas"},
    {"id": "volcan",   "lider": "Blaine",      "emoji": "🌋", "reto": "Equipo sin tipos repetidos"},
    {"id": "tierra",   "lider": "Giovanni",    "emoji": "🌍", "reto": "El resumen del entrenador"},
]


def combate_a_objetivo(combate):
    """Convierte un combate en el dict que entiende el evaluador (dir/archivo/etc)."""
    return {
        "id": "combate-" + combate["id"],
        "dir": "combates",
        "archivo": "test_combates.py",
        "objetivo": "desafios",
        "filtro": combate["id"],
    }


def combate_por_id(cid):
    for c in COMBATES:
        if c["id"] == cid:
            return c
    return None


def disponible(estado, combate):
    """Un combate se desbloquea si tenés la medalla de ese gimnasio."""
    return combate["id"] in estado.get("medallas", [])


def disponibles(estado):
    """Lista de combates desbloqueados (tenés su medalla)."""
    return [c for c in COMBATES if disponible(estado, c)]


def vencido(estado, cid):
    return cid in estado.get("bosses", [])


def todos_vencidos(estado):
    return len(estado.get("bosses", [])) >= len(COMBATES)
