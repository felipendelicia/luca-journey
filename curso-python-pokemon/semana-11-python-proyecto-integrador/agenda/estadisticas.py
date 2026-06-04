"""
agenda.estadisticas — Cálculos de estadísticas.

Funciones puras que reciben datos y devuelven números/textos. No tocan archivos
ni la consola, así son fáciles de testear.
"""


def total_capturados(capturados):
    """Cantidad total de Pokémon capturados."""
    return len(capturados)


def porcentaje_victorias(historial):
    """
    Porcentaje de batallas ganadas (0 a 100), redondeado a entero.
    Si no hubo batallas, devuelve 0.
    """
    total = historial.total()
    if total == 0:
        return 0
    return round((historial.victorias() / total) * 100)


def pokemon_mas_usado(historial):
    """
    Devuelve el nombre del Pokémon más usado en batallas, o None si no hubo.
    Si hay empate, devuelve uno de los que más aparece.
    """
    if historial.total() == 0:
        return None
    # Contamos cuántas veces se usó cada Pokémon.
    conteo = {}
    for batalla in historial.batallas:
        nombre = batalla.pokemon_usado
        conteo[nombre] = conteo.get(nombre, 0) + 1
    # max con key=... devuelve la clave con el valor (conteo) más alto.
    return max(conteo, key=conteo.get)


def resumen(capturados, historial):
    """Devuelve un diccionario con todas las estadísticas principales."""
    return {
        "total_capturados": total_capturados(capturados),
        "batallas_totales": historial.total(),
        "victorias": historial.victorias(),
        "derrotas": historial.derrotas(),
        "porcentaje_victorias": porcentaje_victorias(historial),
        "pokemon_mas_usado": pokemon_mas_usado(historial),
    }
