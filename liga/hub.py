"""
liga.hub — El centro de la aventura: el menú interactivo de la Liga Pokémon.

La función 'procesar_resultado' (pura, sin input/print) hace toda la lógica de
"entrenar": registra el resultado, actualiza racha, EXP, medallas y logros, y
devuelve un resumen de lo que cambió. La función 'jugar' es la interfaz.
"""

from . import datos, progreso, medallas, logros, almacen, evaluador, tarjeta, mapa


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

    passed, total = evaluador.evaluar_semana(semana)
    if total == 0:
        print("   ⚠️ No se pudo evaluar (¿pytest instalado? ¿la carpeta tiene tests?).")
        return

    resumen = procesar_resultado(estado, semana["id"], passed, total)
    _mostrar_resumen(resumen)
    almacen.guardar(estado)


def _entrenar_bonus(estado, ruta=None):
    """Corre la misión bonus de Git (un descanso entre las clases de Python)."""
    bonus = datos.bonus_por_id("git")
    print(f"\n🔀  MISIÓN BONUS: {bonus['nombre']}")
    print("   Un respiro entre tanto Python. Corramos el simulador de Git...")
    passed, total = evaluador.evaluar_semana(bonus)
    if total == 0:
        print("   ⚠️ No se pudo evaluar (¿pytest instalado?).")
        return
    resumen = procesar_resultado(estado, "git", passed, total)
    _mostrar_resumen(resumen)
    if ruta:
        almacen.guardar(estado, ruta)
    else:
        almacen.guardar(estado)


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
        siguiente = proximo_paso(estado)
        if siguiente:
            print(f"\n🎯 Próximo objetivo: Semana {siguiente['id']} — {siguiente['nombre']}")
        else:
            print("\n🏆 ¡Completaste todas las semanas! Sos una leyenda.")

        print("\n¿Qué querés hacer?")
        print("   1) 🏋️  Entrenar (correr tests y ganar EXP)")
        print("   2) 🎴  Ver mi tarjeta de entrenador")
        print("   3) 🗺️  Ver el mapa de la región")
        print("   4) 🏅  Ver mis medallas")
        print("   5) ✨  Ver mis logros")
        print("   6) 🔀  Misión bonus: Git (semana de descanso)")
        print("   7) 💾  Salir (se guarda solo)")

        try:
            opcion = input("Opción > ").strip()
        except (EOFError, KeyboardInterrupt):
            almacen.guardar(estado) if not ruta else almacen.guardar(estado, ruta)
            print("\n¡Hasta la próxima, Entrenador! 👋")
            return

        if opcion == "1":
            _entrenar(estado)
        elif opcion == "2":
            print(tarjeta.render(estado))
        elif opcion == "3":
            print(mapa.render(estado))
        elif opcion == "4":
            _ver_medallas(estado)
        elif opcion == "5":
            _ver_logros(estado)
        elif opcion == "6":
            _entrenar_bonus(estado, ruta)
        elif opcion == "7":
            if ruta:
                almacen.guardar(estado, ruta)
            else:
                almacen.guardar(estado)
            print("💾 Progreso guardado. ¡Seguí así! 👋")
            return
        else:
            print("⚠️ Opción no válida.")
