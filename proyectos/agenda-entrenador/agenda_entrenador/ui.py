"""agenda_entrenador.ui — Textos y formato para la consola."""


def titulo():
    return "=" * 52 + "\n📒  AGENDA DEL ENTRENADOR (edición pulida)\n" + "=" * 52


def menu_principal():
    return (
        "\n¿Qué querés hacer?\n"
        "  1) Registrar Pokémon capturado\n"
        "  2) Ver capturados (ordenados por nivel)\n"
        "  3) Buscar un Pokémon capturado\n"
        "  4) Gestionar equipo activo\n"
        "  5) Registrar una batalla\n"
        "  6) Ver historial de batallas\n"
        "  7) Ver estadísticas\n"
        "  8) Guardar\n"
        "  9) Salir"
    )


def formatear_pokemon(p):
    return f"{p.nombre} ({p.tipo}) Nv{p.nivel} — capturado {p.fecha_captura}"


def formatear_lista(capturados):
    if not capturados:
        return "  (todavía no capturaste ningún Pokémon)"
    return "\n".join(f"  {i}. {formatear_pokemon(p)}"
                     for i, p in enumerate(capturados, start=1))


def formatear_batalla(b):
    icono = "🏆 Ganó" if b.gano() else "💀 Perdió"
    return f"{icono} vs {b.rival} (usó {b.pokemon_usado}) — {b.fecha}"


def formatear_estadisticas(resumen):
    mas_usado = resumen["pokemon_mas_usado"] or "—"
    tipo = resumen["tipo_favorito"] or "—"
    return (
        "\n--- 📊 ESTADÍSTICAS ---\n"
        f"  Total capturados:    {resumen['total_capturados']}\n"
        f"  Batallas jugadas:    {resumen['batallas_totales']}\n"
        f"  Victorias:           {resumen['victorias']}\n"
        f"  Derrotas:            {resumen['derrotas']}\n"
        f"  % de victorias:      {resumen['porcentaje_victorias']}%\n"
        f"  Pokémon más usado:   {mas_usado}\n"
        f"  Tipo favorito:       {tipo}"
    )
