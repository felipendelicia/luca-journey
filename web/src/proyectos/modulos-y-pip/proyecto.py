# Líder Giovanni — Módulo de utilidades (solución de referencia).
# El preamble (POKEMON) está en meta.json y se antepone al corregir.

def filtrar_tipo(lista, tipo):
    return [p for p in lista if p["tipo"] == tipo]


def ordenar_por(lista, clave):
    return sorted(lista, key=lambda p: p[clave])


def estadisticas(lista, clave):
    valores = [p[clave] for p in lista]
    return {
        "minimo": min(valores),
        "maximo": max(valores),
        "promedio": sum(valores) / len(valores),
    }


def buscar_nombre(lista, texto):
    texto_lower = texto.lower()
    return [p for p in lista if texto_lower in p["nombre"].lower()]


def reporte(lista, tipo):
    equipo = ordenar_por(filtrar_tipo(lista, tipo), "nivel")
    return {
        "equipo": equipo,
        "stats_nivel": estadisticas(equipo, "nivel"),
        "stats_hp": estadisticas(equipo, "hp"),
    }
