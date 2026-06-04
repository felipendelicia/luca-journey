"""
🧪 Tests del Constructor de Scripts Bash y el Quiz — Semana 02

Correr con:
    pytest semana-02-linux-intermedio/ -v
"""

import importlib.util
import os

_DIR = os.path.dirname(__file__)


def _cargar(nombre):
    """Carga un módulo vecino con nombre único para no chocar entre semanas."""
    ruta = os.path.join(_DIR, f"{nombre}.py")
    spec = importlib.util.spec_from_file_location(f"semana02_{nombre}", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


interactivo = _cargar("interactivo")
quiz = _cargar("quiz")


# ----------------------------------------------------------------------
#  Constructor de scripts bash
# ----------------------------------------------------------------------
def test_hay_al_menos_5_pasos():
    assert len(interactivo.PASOS) >= 5, "El constructor debería tener al menos 5 pasos"


def test_shebang_valido():
    paso = interactivo.PASOS[0]
    ok, _ = paso["validar"]("#!/usr/bin/env bash")
    assert ok, "El shebang #!/usr/bin/env bash debería ser válido"


def test_shebang_alternativo_valido():
    ok, _ = interactivo._validar_shebang("#!/bin/bash")
    assert ok, "El shebang #!/bin/bash también debería ser válido"


def test_shebang_invalido():
    ok, _ = interactivo._validar_shebang("bin/bash")
    assert not ok, "Sin '#!' no debería ser un shebang válido"


def test_comentario_valido():
    ok, _ = interactivo._validar_comentario("# Esto registra un Pokemon")
    assert ok, "Una línea que empieza con # debería ser un comentario válido"


def test_comentario_no_confunde_shebang():
    ok, _ = interactivo._validar_comentario("#!/usr/bin/env bash")
    assert not ok, "El shebang no debe contar como comentario común"


def test_variable_valida():
    ok, _ = interactivo._validar_variable('POKEMON="Pikachu"')
    assert ok, 'POKEMON="Pikachu" debería ser una variable válida'


def test_variable_con_espacios_falla():
    ok, msg = interactivo._validar_variable('POKEMON = "Pikachu"')
    assert not ok, "Con espacios alrededor del = debería fallar"
    assert "espacios" in msg.lower(), "El mensaje debería mencionar el problema de los espacios"


def test_echo_a_archivo_valido():
    ok, _ = interactivo._validar_echo_archivo('echo "$POKEMON" >> capturados.txt')
    assert ok, "Agregar con >> a capturados.txt usando la variable debería ser válido"


def test_echo_con_un_solo_mayor_falla():
    ok, msg = interactivo._validar_echo_archivo('echo "$POKEMON" > capturados.txt')
    assert not ok, "Usar '>' en vez de '>>' debería fallar (pisa el archivo)"


def test_echo_confirmacion_valido():
    ok, _ = interactivo._validar_echo_confirmacion('echo "$POKEMON registrado!"')
    assert ok, "El echo de confirmación con la variable debería ser válido"


def test_construir_script():
    lineas = ["#!/usr/bin/env bash", "# comentario", 'POKEMON="Pikachu"']
    script = interactivo.construir_script(lineas)
    assert script.startswith("#!/usr/bin/env bash"), "El script debería empezar con el shebang"
    assert script.endswith("\n"), "El script debería terminar con un salto de línea"
    assert 'POKEMON="Pikachu"' in script


# ----------------------------------------------------------------------
#  Quiz
# ----------------------------------------------------------------------
def test_hay_20_preguntas():
    assert len(quiz.PREGUNTAS) == 20, "El quiz debe tener exactamente 20 preguntas"


def test_cada_pregunta_bien_formada():
    for i, p in enumerate(quiz.PREGUNTAS):
        assert "enunciado" in p and p["enunciado"], f"Pregunta {i} sin enunciado"
        assert len(p["opciones"]) >= 2, f"Pregunta {i} debería tener al menos 2 opciones"
        assert 0 <= p["correcta"] < len(p["opciones"]), (
            f"Pregunta {i}: el índice correcto está fuera de rango"
        )
        assert p["explicacion"], f"Pregunta {i} sin explicación"


def test_corregir_respuesta_correcta():
    pregunta = quiz.PREGUNTAS[0]
    es_correcta, _ = quiz.corregir(pregunta, pregunta["correcta"])
    assert es_correcta, "Elegir la opción correcta debería dar es_correcta=True"


def test_corregir_respuesta_incorrecta():
    pregunta = quiz.PREGUNTAS[0]
    # Elegimos una opción distinta a la correcta.
    mala = (pregunta["correcta"] + 1) % len(pregunta["opciones"])
    es_correcta, _ = quiz.corregir(pregunta, mala)
    assert not es_correcta, "Una opción incorrecta debería dar es_correcta=False"


def test_mensaje_final_perfecto():
    msg = quiz.mensaje_final(20, 20)
    assert "PERFECTO" in msg, "Con puntaje perfecto debería felicitar fuerte"


def test_mensaje_final_bajo():
    msg = quiz.mensaje_final(2, 20)
    assert msg, "Siempre debería devolver algún mensaje"
