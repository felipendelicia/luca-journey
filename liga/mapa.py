"""
liga.mapa — Dibuja el mapa de la región con los gimnasios y su estado.

Cada gimnasio puede estar:
  ✅ ganado       (ya tenés la medalla)
  ⚔️ disponible   (cumpliste los requisitos, ¡andá a ganarla!)
  🔒 bloqueado    (te faltan semanas)
"""

from . import datos, progreso, medallas


def estado_gimnasio(estado, gimnasio):
    """Devuelve 'ganado', 'disponible' o 'bloqueado' para un gimnasio."""
    if gimnasio["id"] in estado.get("medallas", []):
        return "ganado"
    if medallas.gimnasio_ganado(estado, gimnasio):
        return "disponible"
    return "bloqueado"


def _icono(estadito):
    return {"ganado": "✅", "disponible": "⚔️", "bloqueado": "🔒"}[estadito]


def render(estado):
    """Devuelve el mapa de la región como string."""
    lineas = []
    lineas.append("🗺️  MAPA DE LA REGIÓN KANTO")
    lineas.append("=" * 50)

    for i, gimnasio in enumerate(datos.GIMNASIOS):
        situacion = estado_gimnasio(estado, gimnasio)
        icono = _icono(situacion)

        # Mostramos el progreso de las semanas que pide este gimnasio.
        partes = []
        for sid in gimnasio["requiere"]:
            d = estado["semanas"].get(str(sid), {})
            passed = d.get("passed", 0)
            total = d.get("total", 0)
            marca = "✓" if progreso.semana_completa(estado, sid) else f"{passed}/{total or '?'}"
            partes.append(f"S{sid}:{marca}")
        detalle = "  ".join(partes)

        lineas.append(
            f"{icono} {gimnasio['emoji']} {gimnasio['nombre']:<16} "
            f"({gimnasio['ciudad']}, {gimnasio['lider']})"
        )
        lineas.append(f"     └─ {detalle}")
        # Camino entre gimnasios.
        if i < len(datos.GIMNASIOS) - 1:
            lineas.append("     │")

    lineas.append("=" * 50)
    if medallas.es_campeon(estado):
        lineas.append("🏆 ¡COMPLETASTE LA LIGA! SOS EL CAMPEÓN DE KANTO 🏆")
    else:
        faltan = len(datos.GIMNASIOS) - len(estado.get("medallas", []))
        lineas.append(f"   Te faltan {faltan} medalla(s) para ser Campeón.")
    return "\n".join(lineas)
