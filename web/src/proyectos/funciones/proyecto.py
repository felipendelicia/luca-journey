# Líder Lt. Surge — Calculadora de combate (solución de referencia).
# El preamble (TABLA_EFECTIVIDAD) está en meta.json y se antepone al corregir.

import math

def efectividad(tipo_ataque, tipo_defensor):
    return TABLA_EFECTIVIDAD.get((tipo_ataque, tipo_defensor), 1.0)

def danio_base(ataque, defensa, poder):
    return int((ataque * poder) / defensa)

def danio_total(ataque, defensa, poder, tipo_ataque, tipo_defensor):
    return int(danio_base(ataque, defensa, poder) * efectividad(tipo_ataque, tipo_defensor))

def resultado_combate(atacante, defensor):
    dmg = danio_total(
        atacante["ataque"],
        defensor["defensa"],
        atacante["poder"],
        atacante["tipo"],
        defensor["tipo"],
    )
    golpes = math.ceil(defensor["hp"] / dmg)
    return "%s derrota a %s en %d golpe(s)." % (atacante["nombre"], defensor["nombre"], golpes)
