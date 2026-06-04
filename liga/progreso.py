"""
liga.progreso — El estado del jugador y la matemática de EXP/nivel/racha.

El "estado" es un diccionario simple (fácil de guardar en JSON):
    {
      "nombre": "Luca",
      "semanas": {"3": {"passed": 18, "total": 20}, ...},
      "medallas": ["roca", ...],
      "logros": ["primera_victoria", ...],
      "racha": 3,
      "ultima_actividad": "2026-06-04",
    }

Todas las funciones son puras (no tocan archivos), así son fáciles de testear.
"""

from datetime import date, timedelta

from . import datos, combates


def estado_inicial(nombre="Entrenador"):
    """Devuelve un estado nuevo y vacío."""
    return {
        "nombre": nombre,
        "semanas": {},
        "medallas": [],
        "logros": [],
        "jugados": [],          # ids de capítulos jugados/completados
        "bosses": [],           # ids de combates de gimnasio vencidos
        "racha": 0,
        "ultima_actividad": None,
    }


# ----------------------------------------------------------------------
#  EXP y nivel
# ----------------------------------------------------------------------
def exp_total(estado):
    """
    EXP total = (tests pasados * EXP_POR_TEST) + bonus por semanas completas.
    Se recalcula desde cero cada vez (es determinista).
    """
    total = 0
    for semana_id, datos_sem in estado["semanas"].items():
        passed = datos_sem.get("passed", 0)
        total_tests = datos_sem.get("total", 0)
        total += passed * datos.EXP_POR_TEST
        # Bonus si la semana está completa (todos los tests pasados).
        if total_tests > 0 and passed >= total_tests:
            total += datos.BONUS_SEMANA_COMPLETA
    # EXP extra por cada combate de gimnasio vencido.
    total += len(estado.get("bosses", [])) * combates.EXP_POR_COMBATE
    return total


def nivel_desde_exp(exp):
    """
    Nivel a partir de la EXP. Para llegar al nivel L hace falta 50*L*(L-1) de EXP.
    Así cada nivel cuesta un poco más que el anterior (curva clásica de RPG).
    """
    nivel = 1
    while 50 * (nivel + 1) * nivel <= exp:
        nivel += 1
    return nivel


def exp_para_nivel(nivel):
    """EXP acumulada necesaria para alcanzar ese nivel."""
    return 50 * nivel * (nivel - 1)


def progreso_nivel(exp):
    """
    Devuelve (nivel, exp_en_nivel, exp_necesaria) para dibujar la barra de EXP.
    'exp_en_nivel' es cuánto llevás dentro del nivel actual.
    """
    nivel = nivel_desde_exp(exp)
    base = exp_para_nivel(nivel)
    siguiente = exp_para_nivel(nivel + 1)
    return nivel, exp - base, siguiente - base


# ----------------------------------------------------------------------
#  Registrar resultados de "entrenar"
# ----------------------------------------------------------------------
def registrar_resultado(estado, semana_id, passed, total):
    """Guarda el resultado de una semana (tests pasados / totales)."""
    # Guardamos el MEJOR resultado: si ya tenía más passed, no lo bajamos.
    clave = str(semana_id)
    anterior = estado["semanas"].get(clave, {})
    mejor_passed = max(anterior.get("passed", 0), passed)
    estado["semanas"][clave] = {"passed": mejor_passed, "total": total}
    return estado


def semana_completa(estado, semana_id):
    """True si esa semana tiene todos sus tests pasados."""
    d = estado["semanas"].get(str(semana_id))
    if not d or d.get("total", 0) == 0:
        return False
    return d["passed"] >= d["total"]


def semanas_completas(estado):
    """Lista de ids de semanas completadas al 100%."""
    return [s["id"] for s in datos.SEMANAS if semana_completa(estado, s["id"])]


def total_tests_pasados(estado):
    """Suma de todos los tests pasados en todas las semanas."""
    return sum(d.get("passed", 0) for d in estado["semanas"].values())


# ----------------------------------------------------------------------
#  Racha (días seguidos jugando)
# ----------------------------------------------------------------------
def actualizar_racha(estado, hoy=None):
    """
    Actualiza la racha de días. Si jugaste ayer, suma. Si ya jugaste hoy, no cambia.
    Si pasó más de un día, la racha se reinicia en 1.
    'hoy' se puede pasar para testear (por defecto, la fecha real).
    """
    if hoy is None:
        hoy = date.today()
    hoy_iso = hoy.isoformat()

    ultima = estado.get("ultima_actividad")
    if ultima == hoy_iso:
        # Ya jugó hoy: la racha no cambia.
        return estado

    if ultima is None:
        estado["racha"] = 1
    else:
        ultima_fecha = date.fromisoformat(ultima)
        if hoy - ultima_fecha == timedelta(days=1):
            estado["racha"] = estado.get("racha", 0) + 1
        else:
            estado["racha"] = 1

    estado["ultima_actividad"] = hoy_iso
    return estado
