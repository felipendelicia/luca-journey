"""
agenda_entrenador.estadisticas — Cálculos de estadísticas.

Versión pulida: agrega 'tipo_favorito' y 'capturados_ordenados'.
"""


def total_capturados(capturados):
    return len(capturados)


def porcentaje_victorias(historial):
    total = historial.total()
    if total == 0:
        return 0
    return round((historial.victorias() / total) * 100)


def pokemon_mas_usado(historial):
    if historial.total() == 0:
        return None
    conteo = {}
    for b in historial.batallas:
        conteo[b.pokemon_usado] = conteo.get(b.pokemon_usado, 0) + 1
    return max(conteo, key=conteo.get)


def tipo_favorito(capturados):
    """Tipo más frecuente entre los capturados, o None si no hay ninguno."""
    if not capturados:
        return None
    conteo = {}
    for p in capturados:
        conteo[p.tipo] = conteo.get(p.tipo, 0) + 1
    return max(conteo, key=conteo.get)


def capturados_ordenados(capturados):
    """Devuelve los capturados ordenados por nivel, de mayor a menor."""
    return sorted(capturados, key=lambda p: p.nivel, reverse=True)


def resumen(capturados, historial):
    return {
        "total_capturados": total_capturados(capturados),
        "batallas_totales": historial.total(),
        "victorias": historial.victorias(),
        "derrotas": historial.derrotas(),
        "porcentaje_victorias": porcentaje_victorias(historial),
        "pokemon_mas_usado": pokemon_mas_usado(historial),
        "tipo_favorito": tipo_favorito(capturados),
    }
