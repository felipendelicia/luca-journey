"""
liga.hub — El centro de la aventura: el menú interactivo de la Liga Pokémon.

La función 'procesar_resultado' (pura, sin input/print) hace toda la lógica de
"entrenar": registra el resultado, actualiza racha, EXP, medallas y logros, y
devuelve un resumen de lo que cambió. La función 'jugar' es la interfaz.
"""

from . import (
    datos, progreso, medallas, logros, almacen, evaluador, tarjeta, mapa, jugador,
    combates,
)


def procesar_resultado(estado, semana_id, passed, total, hoy=None):
    """
    Aplica el resultado de entrenar una semana y devuelve un resumen de lo nuevo:
    EXP ganada, si subió de nivel, medallas y logros conseguidos.
    """
    exp_antes = progreso.exp_total(estado)
    nivel_antes = progreso.nivel_desde_exp(exp_antes)
    ya_completa = progreso.semana_completa(estado, semana_id)

    # Registramos el resultado (guarda el mejor) y actualizamos la racha.
    progreso.registrar_resultado(estado, semana_id, passed, total)
    progreso.actualizar_racha(estado, hoy)

    # Chequeamos medallas y logros nuevos (modifican el estado).
    medallas_nuevas = medallas.chequear_nuevas(estado)
    logros_nuevos = logros.chequear_nuevos(estado)

    exp_despues = progreso.exp_total(estado)
    nivel_despues = progreso.nivel_desde_exp(exp_despues)

    return {
        "exp_antes": exp_antes,
        "exp_despues": exp_despues,
        "exp_ganada": exp_despues - exp_antes,
        "nivel_antes": nivel_antes,
        "nivel_despues": nivel_despues,
        "subio_nivel": nivel_despues > nivel_antes,
        "medallas_nuevas": medallas_nuevas,
        "logros_nuevos": logros_nuevos,
        "semana_recien_completada": (not ya_completa)
        and progreso.semana_completa(estado, semana_id),
        "passed": passed,
        "total": total,
    }


def proximo_paso(estado):
    """Sugiere la próxima semana a entrenar (la primera no completada)."""
    for s in datos.SEMANAS:
        if not progreso.semana_completa(estado, s["id"]):
            return s
    return None


# ======================================================================
#  Interfaz interactiva
# ======================================================================
def _mostrar_resumen(resumen):
    print(f"\n  Resultado: {resumen['passed']}/{resumen['total']} tests pasados.")
    if resumen["exp_ganada"] > 0:
        print(f"  ⭐ ¡Ganaste {resumen['exp_ganada']} EXP!")
    else:
        print("  (sin EXP nueva esta vez — ¡seguí intentando!)")
    if resumen["subio_nivel"]:
        print(f"  🆙 ¡SUBISTE AL NIVEL {resumen['nivel_despues']}! 🎉")
    if resumen["semana_recien_completada"]:
        print("  ✅ ¡Semana completada al 100%!")
    for g in resumen["medallas_nuevas"]:
        print(f"  🏅 ¡GANASTE LA {g['nombre'].upper()} {g['emoji']}! (venciste a {g['lider']})")
    for l in resumen["logros_nuevos"]:
        print(f"  {l['emoji']} ¡LOGRO DESBLOQUEADO: {l['nombre']}! — {l['desc']}")


def _mostrar_fallos(fallos):
    """Muestra los ejercicios que todavía no pasan, con una pista cada uno."""
    if not fallos:
        return
    print(f"\n  📋 Te faltan {len(fallos)} ejercicio(s):")
    for nombre, pista in fallos[:10]:
        if pista:
            print(f"   ✗ {nombre} — {pista}")
        else:
            print(f"   ✗ {nombre}")
    if len(fallos) > 10:
        print(f"   ...y {len(fallos) - 10} más.")
    print("  💡 Corregí tu ejercicios.py y volvé a entrenar para ganar la EXP.")


def _entrenar(estado):
    """Submenú para elegir una semana y correr sus tests."""
    print("\n🏋️  ENTRENAR — ¿qué semana querés intentar?")
    for s in datos.SEMANAS:
        marca = "✅" if progreso.semana_completa(estado, s["id"]) else "  "
        print(f"   {marca} {s['id']:>2}) {s['emoji']} {s['nombre']}")
    eleccion = input("   Número de semana (o Enter para volver) > ").strip()
    if not eleccion.isdigit():
        return
    semana = datos.semana_por_id(int(eleccion))
    if semana is None:
        print("   ⚠️ No existe esa semana.")
        return

    if semana.get("objetivo") == "ejercicios":
        print(f"\n   📝 Evaluando TU ejercicios.py de la semana {semana['id']}...")
    else:
        print(f"\n   📝 Corriendo los tests de la semana {semana['id']}...")
    print("   (esto puede tardar unos segundos)")

    res = evaluador.evaluar_semana_detallado(semana)
    if res["total"] == 0:
        print("   ⚠️ No se pudo evaluar (¿pytest instalado? ¿la carpeta tiene tests?).")
        return

    resumen = procesar_resultado(estado, semana["id"], res["passed"], res["total"])
    _mostrar_resumen(resumen)
    _mostrar_fallos(res["fallos"])
    almacen.guardar(estado)


def _entrenar_bonus(estado, ruta=None):
    """Corre la misión bonus de Git (un descanso entre las clases de Python)."""
    bonus = datos.bonus_por_id("git")
    print(f"\n🔀  MISIÓN BONUS: {bonus['nombre']}")
    print("   Un respiro entre tanto Python. Corramos el simulador de Git...")
    res = evaluador.evaluar_semana_detallado(bonus)
    if res["total"] == 0:
        print("   ⚠️ No se pudo evaluar (¿pytest instalado?).")
        return
    resumen = procesar_resultado(estado, "git", res["passed"], res["total"])
    _mostrar_resumen(resumen)
    _mostrar_fallos(res["fallos"])
    if ruta:
        almacen.guardar(estado, ruta)
    else:
        almacen.guardar(estado)


# ======================================================================
#  Jugar capítulos (lanzar los interactivos)
# ======================================================================
def marcar_jugado(estado, cid):
    """Marca un capítulo como completado (si no lo estaba). Devuelve True si lo agregó."""
    cid = str(cid)
    jugados = estado.setdefault("jugados", [])
    if cid in jugados:
        return False
    jugados.append(cid)
    return True


def ya_jugado(estado, cid):
    return str(cid) in estado.get("jugados", [])


def proximo_jugable(estado):
    """Primer capítulo jugable que todavía no está completado, o None si están todos."""
    for c in jugador.jugables():
        if not ya_jugado(estado, c["id"]):
            return c
    return None


def _guardar(estado, ruta):
    almacen.guardar(estado, ruta) if ruta else almacen.guardar(estado)


def _jugar_capitulo(estado, capitulo, ruta=None):
    """Lanza el juego interactivo de un capítulo, con continuar/reintentar."""
    if ya_jugado(estado, capitulo["id"]):
        try:
            r = input(f"   Ya completaste «{capitulo['nombre']}». ¿Reintentar? (s/n) ")
        except (EOFError, KeyboardInterrupt):
            return
        if not r.strip().lower().startswith("s"):
            return

    print(f"\n🎮 Lanzando: {capitulo['emoji']} {capitulo['nombre']}")
    print("   (cuando termines el juego, volvés a la Liga)\n")
    ok = jugador.lanzar(capitulo)
    if not ok:
        print("   ⚠️ Este capítulo no tiene juego interactivo.")
        return

    # Al volver del juego, preguntamos si lo completó (si no estaba ya marcado).
    if not ya_jugado(estado, capitulo["id"]):
        try:
            r = input("\n   ¿Completaste este capítulo? (s/n) ")
        except (EOFError, KeyboardInterrupt):
            return
        if r.strip().lower().startswith("s"):
            marcar_jugado(estado, capitulo["id"])
            _guardar(estado, ruta)
            print("   ✅ ¡Capítulo completado! Tu progreso quedó guardado.")


def _continuar(estado, ruta=None):
    """Continúa en el primer capítulo sin completar."""
    siguiente = proximo_jugable(estado)
    if siguiente is None:
        print("\n🏆 ¡Ya jugaste todos los capítulos! Elegí uno para reintentar.")
        _elegir_capitulo(estado, ruta)
        return
    _jugar_capitulo(estado, siguiente, ruta)


def _elegir_capitulo(estado, ruta=None):
    """Menú para elegir qué capítulo jugar."""
    print("\n🎮  ELEGÍ UN CAPÍTULO PARA JUGAR:")
    jugables = jugador.jugables()
    for i, c in enumerate(jugables, start=1):
        marca = "✅" if ya_jugado(estado, c["id"]) else "▶ "
        print(f"   {marca} {i:>2}) {c['emoji']} {c['nombre']}")
    try:
        eleccion = input("   Número (o Enter para volver) > ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not eleccion.isdigit():
        return
    idx = int(eleccion) - 1
    if 0 <= idx < len(jugables):
        _jugar_capitulo(estado, jugables[idx], ruta)
    else:
        print("   ⚠️ Número fuera de rango.")


def procesar_combate(estado, combate, passed, total, hoy=None):
    """Aplica el resultado de un combate de gimnasio. Devuelve un resumen."""
    exp_antes = progreso.exp_total(estado)
    nivel_antes = progreso.nivel_desde_exp(exp_antes)
    gano = total > 0 and passed >= total

    recien = False
    if gano and combate["id"] not in estado.setdefault("bosses", []):
        estado["bosses"].append(combate["id"])
        recien = True

    progreso.actualizar_racha(estado, hoy)
    logros_nuevos = logros.chequear_nuevos(estado)

    exp_despues = progreso.exp_total(estado)
    return {
        "gano": gano,
        "recien": recien,
        "exp_ganada": exp_despues - exp_antes,
        "subio_nivel": progreso.nivel_desde_exp(exp_despues) > nivel_antes,
        "nivel_despues": progreso.nivel_desde_exp(exp_despues),
        "logros_nuevos": logros_nuevos,
        "passed": passed,
        "total": total,
    }


def _combates(estado, ruta=None):
    """Menú de combates de gimnasio (jefes integradores)."""
    disponibles = combates.disponibles(estado)
    if not disponibles:
        print("\n⚔️  Todavía no desbloqueaste ningún combate.")
        print("   Ganá medallas (completá las semanas) para retar a los líderes.")
        return

    print("\n⚔️  COMBATES DE GIMNASIO — retá a un líder (resolvé combates/desafios.py):")
    for i, c in enumerate(disponibles, start=1):
        estado_txt = "✅ vencido" if combates.vencido(estado, c["id"]) else "⚔️ disponible"
        print(f"   {i:>2}) {c['emoji']} vs {c['lider']} — {c['reto']}  [{estado_txt}]")

    try:
        eleccion = input("   Número (o Enter para volver) > ").strip()
    except (EOFError, KeyboardInterrupt):
        return
    if not eleccion.isdigit():
        return
    idx = int(eleccion) - 1
    if not (0 <= idx < len(disponibles)):
        print("   ⚠️ Número fuera de rango.")
        return

    combate = disponibles[idx]
    print(f"\n   🥊 Combate contra {combate['lider']}... evaluando tu desafío.")
    objetivo = combates.combate_a_objetivo(combate)
    res = evaluador.evaluar_semana_detallado(objetivo)
    if res["total"] == 0:
        print("   ⚠️ No se pudo evaluar (¿pytest instalado?).")
        return

    resumen = procesar_combate(estado, combate, res["passed"], res["total"])
    if resumen["gano"]:
        print(f"   🏆 ¡VENCISTE A {combate['lider'].upper()}! {combate['emoji']}")
        if resumen["exp_ganada"] > 0:
            print(f"   ⭐ ¡Ganaste {resumen['exp_ganada']} EXP!")
        if resumen["subio_nivel"]:
            print(f"   🆙 ¡Subiste al nivel {resumen['nivel_despues']}!")
        for l in resumen["logros_nuevos"]:
            print(f"   {l['emoji']} ¡LOGRO: {l['nombre']}! — {l['desc']}")
    else:
        print(f"   💪 Todavía no. Pasaste {res['passed']}/{res['total']} del desafío.")
        _mostrar_fallos(res["fallos"])
    _guardar(estado, ruta)


def _ver_medallas(estado):
    print("\n🏅  TUS MEDALLAS")
    for g in datos.GIMNASIOS:
        tiene = g["id"] in estado.get("medallas", [])
        icono = g["emoji"] if tiene else "🔒"
        sufijo = "" if tiene else f"  (necesitás completar: {g['requiere']})"
        print(f"   {icono} {g['nombre']} — {g['lider']}, {g['ciudad']}{sufijo}")


def _ver_logros(estado):
    print("\n✨  TUS LOGROS")
    for l in logros.LOGROS:
        tiene = l["id"] in estado.get("logros", [])
        icono = l["emoji"] if tiene else "🔒"
        print(f"   {icono} {l['nombre']} — {l['desc']}")


def jugar(ruta=None):
    """Bucle principal de la Liga Pokémon."""
    estado = almacen.cargar(ruta) if ruta else almacen.cargar()

    # Primera vez: pedimos el nombre.
    if not estado.get("ultima_actividad") and estado.get("nombre") in (None, "Entrenador"):
        try:
            nombre = input("¡Hola! ¿Cómo te llamás, Entrenador? ").strip()
        except (EOFError, KeyboardInterrupt):
            return
        if nombre:
            estado["nombre"] = nombre

    print(tarjeta.render(estado))

    while True:
        # Mostramos en qué capítulo continuar (el primero sin completar).
        siguiente_juego = proximo_jugable(estado)
        if siguiente_juego:
            print(f"\n🎯 Continuá en: {siguiente_juego['emoji']} {siguiente_juego['nombre']}")
        else:
            print("\n🏆 ¡Jugaste todos los capítulos! Sos una leyenda. (Podés reintentar)")

        print("\n¿Qué querés hacer?")
        print("   1) ▶️   Continuar (jugar el próximo capítulo)")
        print("   2) 🎮  Elegir un capítulo para jugar")
        print("   3) 🏋️  Entrenar (correr tests y ganar EXP)")
        print("   4) ⚔️   Combates de gimnasio (jefes)")
        print("   5) 🎴  Ver mi tarjeta de entrenador")
        print("   6) 🗺️  Ver el mapa de la región")
        print("   7) 🏅  Ver mis medallas")
        print("   8) ✨  Ver mis logros")
        print("   9) 🔀  Misión bonus: Git (semana de descanso)")
        print("  10) 💾  Salir (se guarda solo)")

        try:
            opcion = input("Opción > ").strip()
        except (EOFError, KeyboardInterrupt):
            _guardar(estado, ruta)
            print("\n¡Hasta la próxima, Entrenador! 👋")
            return

        if opcion == "1":
            _continuar(estado, ruta)
        elif opcion == "2":
            _elegir_capitulo(estado, ruta)
        elif opcion == "3":
            _entrenar(estado)
        elif opcion == "4":
            _combates(estado, ruta)
        elif opcion == "5":
            print(tarjeta.render(estado))
        elif opcion == "6":
            print(mapa.render(estado))
        elif opcion == "7":
            _ver_medallas(estado)
        elif opcion == "8":
            _ver_logros(estado)
        elif opcion == "9":
            _entrenar_bonus(estado, ruta)
        elif opcion == "10":
            _guardar(estado, ruta)
            print("💾 Progreso guardado. ¡Seguí así! 👋")
            return
        else:
            print("⚠️ Opción no válida.")
