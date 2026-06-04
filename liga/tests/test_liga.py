"""
Tests de la Liga Pokémon (el sistema de gamificación).

No corren pytest de verdad: el evaluador usa un 'runner' falso.
"""

from datetime import date

from liga import (
    datos, progreso, medallas, logros, almacen, evaluador, tarjeta, mapa, hub
)


# ----------------------------------------------------------------------
#  progreso: EXP y nivel
# ----------------------------------------------------------------------
def test_estado_inicial():
    e = progreso.estado_inicial("Luca")
    assert e["nombre"] == "Luca"
    assert e["semanas"] == {}
    assert e["medallas"] == []
    assert e["racha"] == 0


def test_exp_total_cuenta_tests_y_bonus():
    e = progreso.estado_inicial()
    # Semana 3 con 18/20: 18*10 = 180 EXP, sin bonus (no está completa).
    progreso.registrar_resultado(e, 3, 18, 20)
    assert progreso.exp_total(e) == 180
    # Ahora completa: 20*10 + 50 de bonus = 250.
    progreso.registrar_resultado(e, 3, 20, 20)
    assert progreso.exp_total(e) == 250


def test_nivel_desde_exp():
    assert progreso.nivel_desde_exp(0) == 1
    assert progreso.nivel_desde_exp(99) == 1
    assert progreso.nivel_desde_exp(100) == 2
    assert progreso.nivel_desde_exp(300) == 3


def test_progreso_nivel():
    nivel, en_nivel, necesaria = progreso.progreso_nivel(100)
    assert nivel == 2
    assert en_nivel == 0
    assert necesaria == 200  # de nivel 2 (100) a nivel 3 (300)


def test_registrar_guarda_el_mejor():
    e = progreso.estado_inicial()
    progreso.registrar_resultado(e, 4, 15, 20)
    progreso.registrar_resultado(e, 4, 10, 20)  # peor: no debería bajar
    assert e["semanas"]["4"]["passed"] == 15


def test_semana_completa():
    e = progreso.estado_inicial()
    progreso.registrar_resultado(e, 5, 20, 20)
    assert progreso.semana_completa(e, 5) is True
    progreso.registrar_resultado(e, 6, 19, 20)
    assert progreso.semana_completa(e, 6) is False


# ----------------------------------------------------------------------
#  Racha
# ----------------------------------------------------------------------
def test_racha_primer_dia():
    e = progreso.estado_inicial()
    progreso.actualizar_racha(e, date(2026, 6, 1))
    assert e["racha"] == 1


def test_racha_dia_consecutivo_suma():
    e = progreso.estado_inicial()
    progreso.actualizar_racha(e, date(2026, 6, 1))
    progreso.actualizar_racha(e, date(2026, 6, 2))
    assert e["racha"] == 2


def test_racha_mismo_dia_no_cambia():
    e = progreso.estado_inicial()
    progreso.actualizar_racha(e, date(2026, 6, 1))
    progreso.actualizar_racha(e, date(2026, 6, 1))
    assert e["racha"] == 1


def test_racha_se_corta():
    e = progreso.estado_inicial()
    progreso.actualizar_racha(e, date(2026, 6, 1))
    progreso.actualizar_racha(e, date(2026, 6, 5))  # pasaron días
    assert e["racha"] == 1


# ----------------------------------------------------------------------
#  Medallas
# ----------------------------------------------------------------------
def _completar(e, *ids):
    for sid in ids:
        progreso.registrar_resultado(e, sid, 20, 20)


def test_medalla_roca_requiere_semanas_1_y_2():
    e = progreso.estado_inicial()
    _completar(e, 1)
    assert "roca" not in medallas.medallas_disponibles(e)
    _completar(e, 2)
    assert "roca" in medallas.medallas_disponibles(e)


def test_chequear_nuevas_otorga_una_vez():
    e = progreso.estado_inicial()
    _completar(e, 1, 2)
    nuevas = medallas.chequear_nuevas(e)
    assert any(g["id"] == "roca" for g in nuevas)
    # Segunda vez: ya la tiene, no se repite.
    assert medallas.chequear_nuevas(e) == []


def test_es_campeon():
    e = progreso.estado_inicial()
    _completar(e, *range(1, 13))
    medallas.chequear_nuevas(e)
    assert medallas.es_campeon(e) is True


# ----------------------------------------------------------------------
#  Logros
# ----------------------------------------------------------------------
def test_logro_primera_victoria():
    e = progreso.estado_inicial()
    progreso.registrar_resultado(e, 3, 1, 20)
    nuevos = logros.chequear_nuevos(e)
    assert any(l["id"] == "primera_victoria" for l in nuevos)


def test_logro_no_se_repite():
    e = progreso.estado_inicial()
    progreso.registrar_resultado(e, 3, 1, 20)
    logros.chequear_nuevos(e)
    assert logros.chequear_nuevos(e) == []


def test_logro_campeon():
    e = progreso.estado_inicial()
    _completar(e, *range(1, 13))
    medallas.chequear_nuevas(e)
    nuevos = logros.chequear_nuevos(e)
    assert any(l["id"] == "campeon" for l in nuevos)


# ----------------------------------------------------------------------
#  Evaluador (con runner falso, sin correr pytest de verdad)
# ----------------------------------------------------------------------
def test_parsear_resultado():
    assert evaluador.parsear_resultado("18 passed, 2 failed in 0.1s") == (18, 20)
    assert evaluador.parsear_resultado("20 passed in 0.05s") == (20, 20)
    assert evaluador.parsear_resultado("1 failed, 0 passed") == (0, 1)


def test_evaluar_semana_usa_runner():
    semana = datos.semana_por_id(3)
    capturado = {}

    def fake_runner(args, env):
        capturado["env"] = env
        return "15 passed, 5 failed in 0.1s"

    passed, total = evaluador.evaluar_semana(semana, runner=fake_runner)
    assert (passed, total) == (15, 20)
    # Semana 3 evalúa ejercicios: debe setear CURSO_MODULO=ejercicios.
    assert capturado["env"].get("CURSO_MODULO") == "ejercicios"


def test_evaluar_semana_linux_no_setea_modulo():
    semana = datos.semana_por_id(1)
    capturado = {}

    def fake_runner(args, env):
        capturado["env"] = env
        return "21 passed in 0.03s"

    evaluador.evaluar_semana(semana, runner=fake_runner)
    assert "CURSO_MODULO" not in capturado["env"]


# ----------------------------------------------------------------------
#  hub.procesar_resultado (orquestación)
# ----------------------------------------------------------------------
def test_procesar_resultado_da_exp_y_sube_nivel():
    e = progreso.estado_inicial()
    resumen = hub.procesar_resultado(e, 3, 20, 20, hoy=date(2026, 6, 1))
    # 20*10 + 50 bonus = 250 EXP. Nivel 3 necesita 300, así que esto es nivel 2.
    assert resumen["exp_ganada"] == 250
    assert resumen["subio_nivel"] is True
    assert resumen["nivel_despues"] == 2
    assert resumen["semana_recien_completada"] is True


def test_procesar_resultado_otorga_medalla():
    e = progreso.estado_inicial()
    hub.procesar_resultado(e, 1, 20, 20, hoy=date(2026, 6, 1))
    resumen = hub.procesar_resultado(e, 2, 20, 20, hoy=date(2026, 6, 2))
    ids = [g["id"] for g in resumen["medallas_nuevas"]]
    assert "roca" in ids


def test_proximo_paso():
    e = progreso.estado_inicial()
    assert hub.proximo_paso(e)["id"] == 1
    _completar(e, 1)
    assert hub.proximo_paso(e)["id"] == 2


# ----------------------------------------------------------------------
#  Misión bonus de Git
# ----------------------------------------------------------------------
def test_bonus_git_existe():
    assert datos.bonus_por_id("git") is not None
    assert datos.bonus_por_id("inexistente") is None


def test_bonus_git_da_exp_y_logro():
    e = progreso.estado_inicial()
    # Simulamos completar la misión bonus de Git (20/20).
    resumen = hub.procesar_resultado(e, "git", 20, 20, hoy=date(2026, 6, 1))
    assert resumen["exp_ganada"] > 0
    ids = [l["id"] for l in resumen["logros_nuevos"]]
    assert "viajero_del_tiempo" in ids


def test_bonus_git_no_cuenta_como_semana_numerada():
    e = progreso.estado_inicial()
    hub.procesar_resultado(e, "git", 20, 20, hoy=date(2026, 6, 1))
    # No debe sumar a las 12 semanas numeradas ni dar medallas.
    assert len(progreso.semanas_completas(e)) == 0
    assert e["medallas"] == []


# ----------------------------------------------------------------------
#  Almacén (persistencia)
# ----------------------------------------------------------------------
def test_almacen_ciclo(tmp_path):
    ruta = str(tmp_path / "progreso.json")
    e = progreso.estado_inicial("Luca")
    progreso.registrar_resultado(e, 3, 18, 20)
    almacen.guardar(e, ruta)
    cargado = almacen.cargar(ruta)
    assert cargado["nombre"] == "Luca"
    assert cargado["semanas"]["3"]["passed"] == 18


def test_almacen_inexistente_devuelve_inicial(tmp_path):
    e = almacen.cargar(str(tmp_path / "no_existe.json"))
    assert e["semanas"] == {}


# ----------------------------------------------------------------------
#  Render (tarjeta y mapa) no deben romperse
# ----------------------------------------------------------------------
def test_tarjeta_render():
    e = progreso.estado_inicial("Luca")
    progreso.registrar_resultado(e, 3, 20, 20)
    texto = tarjeta.render(e)
    assert "Luca" in texto
    assert "TARJETA DE ENTRENADOR" in texto


def test_mapa_render():
    e = progreso.estado_inicial()
    _completar(e, 1, 2)
    medallas.chequear_nuevas(e)
    texto = mapa.render(e)
    assert "KANTO" in texto
    assert "✅" in texto  # la medalla Roca ya está ganada


def test_mapa_marca_disponible():
    e = progreso.estado_inicial()
    _completar(e, 1, 2)  # requisitos de Roca, pero sin otorgarla todavía
    g = datos.GIMNASIOS[0]
    assert mapa.estado_gimnasio(e, g) == "disponible"
