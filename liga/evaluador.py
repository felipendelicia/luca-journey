"""
liga.evaluador — Corre los tests de una semana y cuenta cuántos pasaron.

Para las semanas con ejercicios (3 a 10), corre los tests con la variable de
entorno CURSO_MODULO=ejercicios, así evalúa el archivo ejercicios.py del alumno
(su trabajo real) en vez de las soluciones.

El "runner" (lo que ejecuta pytest) se puede reemplazar en los tests para no
tener que correr pytest de verdad.
"""

import os
import re
import subprocess
import sys

from . import datos

# Carpeta raíz del curso (un nivel arriba de 'liga').
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def parsear_resultado(texto):
    """
    Lee la salida de pytest y devuelve (passed, total).
    Busca patrones como '18 passed', '2 failed', '1 error'.
    """
    def _buscar(palabra):
        m = re.search(rf"(\d+) {palabra}", texto)
        return int(m.group(1)) if m else 0

    passed = _buscar("passed")
    failed = _buscar("failed")
    errores = _buscar("error") + _buscar("errors")
    total = passed + failed + errores
    return passed, total


def _runner_real(args, env):
    """Corre pytest de verdad como subproceso y devuelve su salida de texto."""
    resultado = subprocess.run(
        args, cwd=BASE_DIR, env=env,
        capture_output=True, text=True,
    )
    # Juntamos stdout y stderr por las dudas.
    return resultado.stdout + resultado.stderr


def evaluar_semana(semana, runner=None):
    """
    Corre los tests de 'semana' (un dict de datos.SEMANAS) y devuelve (passed, total).
    'runner' es una función(args, env) -> texto; por defecto corre pytest real.
    """
    runner = runner or _runner_real

    # Qué corremos: un archivo puntual o toda la carpeta de la semana.
    objetivo = semana["dir"]
    if semana.get("archivo"):
        objetivo = os.path.join(semana["dir"], semana["archivo"])

    args = [sys.executable, "-m", "pytest", objetivo, "-q", "--no-header"]

    # Si la semana evalúa ejercicios, le decimos a los tests que usen ejercicios.py.
    env = dict(os.environ)
    if semana.get("objetivo") == "ejercicios":
        env["CURSO_MODULO"] = "ejercicios"
    else:
        env.pop("CURSO_MODULO", None)

    salida = runner(args, env)
    return parsear_resultado(salida)
