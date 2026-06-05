# Líder Erika — Gestor de equipo (solución de referencia).
# El preamble (EQUIPO_INICIAL) está en meta.json y se antepone al corregir.

def agregar_pokemon(equipo, nombre, tipo, nivel, ps):
    equipo.append({"nombre": nombre, "tipo": tipo, "nivel": nivel, "ps": ps})
    return equipo

def filtrar_nivel_minimo(equipo, nivel_min):
    return [p for p in equipo if p["nivel"] >= nivel_min]

def ordenar_por_ps(equipo):
    return sorted(equipo, key=lambda p: p["ps"], reverse=True)

def resumen_equipo(equipo):
    cantidad = len(equipo)
    ps_total = sum(p["ps"] for p in equipo)
    nivel_promedio = sum(p["nivel"] for p in equipo) / cantidad
    mas_fuerte = max(equipo, key=lambda p: p["ps"])["nombre"]
    return {
        "cantidad": cantidad,
        "ps_total": ps_total,
        "nivel_promedio": nivel_promedio,
        "mas_fuerte": mas_fuerte,
    }
