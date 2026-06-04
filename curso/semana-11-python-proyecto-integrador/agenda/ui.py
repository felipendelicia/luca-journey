"""
agenda.ui — Textos y formato para la consola.

Funciones que arman strings para mostrar. No usan input() (eso vive en main.py),
así se pueden testear fácil.
"""


def titulo():
    return (
        "=" * 50 + "\n"
        "📒  AGENDA DEL ENTRENADOR\n"
        + "=" * 50
    )


def menu_principal():
    """Devuelve el texto del menú principal."""
    return (
        "\n¿Qué querés hacer?\n"
        "  1) Registrar Pokémon capturado\n"
        "  2) Ver Pokémon capturados\n"
        "  3) Gestionar equipo activo\n"
        "  4) Registrar una batalla\n"
        "  5) Ver historial de batallas\n"
        "  6) Ver estadísticas\n"
        "  7) Guardar\n"
        "  8) Salir"
    )


def formatear_pokemon(pokemon):
    """Una línea linda para un Pokémon."""
    return f"• {pokemon.nombre} ({pokemon.tipo}) Nv{pokemon.nivel} — {pokemon.fecha_captura}"


def formatear_lista_capturados(capturados):
    """Devuelve el texto de la lista de capturados."""
    if not capturados:
        return "  (todavía no capturaste ningún Pokémon)"
    return "\n".join(f"  {i}. {formatear_pokemon(p)[2:]}"
                     for i, p in enumerate(capturados, start=1))


def formatear_batalla(batalla):
    """Una línea para una batalla."""
    icono = "🏆 Ganó" if batalla.gano() else "💀 Perdió"
    return f"{icono} vs {batalla.rival} (usó {batalla.pokemon_usado}) — {batalla.fecha}"


def formatear_estadisticas(resumen):
    """Devuelve el texto de las estadísticas a partir del dict resumen."""
    mas_usado = resumen["pokemon_mas_usado"] or "—"
    return (
        "\n--- 📊 ESTADÍSTICAS ---\n"
        f"  Total capturados:    {resumen['total_capturados']}\n"
        f"  Batallas jugadas:    {resumen['batallas_totales']}\n"
        f"  Victorias:           {resumen['victorias']}\n"
        f"  Derrotas:            {resumen['derrotas']}\n"
        f"  % de victorias:      {resumen['porcentaje_victorias']}%\n"
        f"  Pokémon más usado:   {mas_usado}"
    )
