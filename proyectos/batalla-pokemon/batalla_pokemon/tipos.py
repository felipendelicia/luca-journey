"""
batalla_pokemon.tipos — Tabla de efectividad entre tipos.

Devuelve el multiplicador de daño de un tipo atacante contra un tipo defensor.
"""

# Para cada tipo atacante: a qué tipos les pega DOBLE y a cuáles MITAD.
_SUPER_EFECTIVO = {
    "fuego": {"planta", "hielo", "bicho"},
    "agua": {"fuego", "roca", "tierra"},
    "planta": {"agua", "roca", "tierra"},
    "electrico": {"agua", "volador"},
    "roca": {"fuego", "volador", "bicho"},
    "hielo": {"planta", "volador", "dragon"},
}

_POCO_EFECTIVO = {
    "fuego": {"agua", "roca", "fuego"},
    "agua": {"planta", "agua"},
    "planta": {"fuego", "planta", "volador"},
    "electrico": {"planta", "electrico"},
    "roca": {"agua", "planta"},
    "hielo": {"fuego", "agua", "hielo"},
}


def efectividad(tipo_atacante, tipo_defensor):
    """
    Devuelve el multiplicador de daño:
      2.0 si es súper efectivo, 0.5 si es poco efectivo, 1.0 si es normal.
    """
    atacante = tipo_atacante.lower()
    defensor = tipo_defensor.lower()
    if defensor in _SUPER_EFECTIVO.get(atacante, set()):
        return 2.0
    if defensor in _POCO_EFECTIVO.get(atacante, set()):
        return 0.5
    return 1.0


def texto_efectividad(multiplicador):
    """Devuelve un texto descriptivo del multiplicador."""
    if multiplicador > 1:
        return "¡Es súper efectivo!"
    if multiplicador < 1:
        return "No es muy efectivo..."
    return ""
