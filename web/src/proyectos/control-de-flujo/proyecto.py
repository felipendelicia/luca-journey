# Líder Misty — Clasificador de Pokémon (solución de referencia).
# El preamble (EQUIPO) está en meta.json y se antepone al corregir.

def categoria(nivel):
    if nivel < 10:
        return "principiante"
    elif nivel < 30:
        return "intermedio"
    else:
        return "experto"

def puede_combatir(poke):
    return poke["estado"] == "normal" and poke["nivel"] >= 5

def filtrar_tipo(equipo, tipo):
    return [p for p in equipo if p["tipo"] == tipo]

def resumen_equipo(equipo):
    resultado = []
    for p in equipo:
        cat = categoria(p["nivel"])
        estado = "listo" if puede_combatir(p) else "no disponible"
        resultado.append("%s: %s | %s" % (p["nombre"], cat, estado))
    return resultado
