"""
liga.tarjeta — Dibuja la Tarjeta de Entrenador en ASCII.
"""

from . import datos, progreso


def barra_exp(actual, necesaria, largo=20):
    """Barra visual de EXP hacia el siguiente nivel."""
    if necesaria <= 0:
        llenos = largo
    else:
        llenos = int((actual / necesaria) * largo)
    llenos = max(0, min(largo, llenos))
    return "█" * llenos + "░" * (largo - llenos)


def rango(nivel):
    """Un título copado según el nivel."""
    if nivel >= 20:
        return "Campeón"
    if nivel >= 12:
        return "As Pokémon"
    if nivel >= 7:
        return "Entrenador Experto"
    if nivel >= 3:
        return "Entrenador"
    return "Novato"


def render(estado):
    """Devuelve la tarjeta de entrenador como string."""
    exp = progreso.exp_total(estado)
    nivel, exp_en_nivel, exp_necesaria = progreso.progreso_nivel(exp)
    completas = len(progreso.semanas_completas(estado))
    total_semanas = len(datos.SEMANAS)
    n_medallas = len(estado.get("medallas", []))
    n_logros = len(estado.get("logros", []))
    racha = estado.get("racha", 0)

    nombre = (estado.get("nombre") or "Entrenador")[:24]

    # Medallas como íconos: ganadas con su emoji, faltantes como ·
    iconos = ""
    for g in datos.GIMNASIOS:
        iconos += g["emoji"] if g["id"] in estado.get("medallas", []) else "·"

    # Diseño sin borde derecho: así los emojis (que ocupan doble ancho en la
    # terminal) nunca desalinean el recuadro.
    borde = "─" * 46
    return f"""
┌{borde}┐
│   🎴  TARJETA DE ENTRENADOR
├{borde}┤
   Nombre:   {nombre}
   Rango:    {rango(nivel)}   (Nivel {nivel})
   EXP:      [{barra_exp(exp_en_nivel, exp_necesaria)}] {exp_en_nivel}/{exp_necesaria}   ·   Total: {exp}
   🏅 Medallas:  {n_medallas}/8   {iconos}
   ✨ Logros:    {n_logros}
   📚 Semanas:   {completas}/{total_semanas}
   🔥 Racha:     {racha} día(s)
└{borde}┘
"""
