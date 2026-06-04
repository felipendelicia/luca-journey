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


def _nombre_legible(nodo):
    """Convierte 'archivo.py::test_suma_de_niveles' en 'suma de niveles'."""
    func = nodo.split("::")[-1]
    if func.startswith("test_"):
        func = func[len("test_"):]
    return func.replace("_", " ")


def parsear_fallos(texto):
    """
    Extrae la lista de ejercicios que fallaron, con su pista (el mensaje del test).
    Lee las líneas 'FAILED archivo::test_x - AssertionError: pista'.
    Devuelve una lista de (nombre_legible, pista).
    """
    fallos = []
    for linea in texto.splitlines():
        m = re.match(r"^FAILED\s+(\S+)(?:\s+-\s+(.*))?$", linea.strip())
        if not m:
            continue
        nodo = m.group(1)
        mensaje = (m.group(2) or "").strip()
        # Sacamos el prefijo del tipo de error (ej "AssertionError: ").
        mensaje = re.sub(r"^\w+Error:\s*", "", mensaje)
        fallos.append((_nombre_legible(nodo), mensaje))
    return fallos


def _runner_real(args, env):
    """Corre pytest de verdad como subproceso y devuelve su salida de texto."""
    resultado = subprocess.run(
        args, cwd=BASE_DIR, env=env,
        capture_output=True, text=True,
    )
    # Juntamos stdout y stderr por las dudas.
    return resultado.stdout + resultado.stderr


def _comando(semana):
    """Arma (args, env) para correr los tests de una semana o desafío."""
    objetivo = semana["dir"]
    if semana.get("archivo"):
        objetivo = os.path.join(semana["dir"], semana["archivo"])

    # --tb=no -rf lista los tests fallidos con su mensaje; COLUMNS evita que se corten.
    args = [sys.executable, "-m", "pytest", objetivo,
            "-q", "--no-header", "--tb=no", "-rf"]
    # 'filtro' (opcional) selecciona un subconjunto de tests con -k (combates).
    if semana.get("filtro"):
        args += ["-k", semana["filtro"]]

    env = dict(os.environ)
    env["COLUMNS"] = "1000"
    # Si hay 'objetivo' (ej "ejercicios" o "desafios"), le decimos a los tests qué
    # archivo del alumno evaluar vía CURSO_MODULO. Si es None, se usan los tests provistos.
    if semana.get("objetivo"):
        env["CURSO_MODULO"] = semana["objetivo"]
    else:
        env.pop("CURSO_MODULO", None)
    return args, env


def evaluar_semana_detallado(semana, runner=None):
    """
    Corre los tests y devuelve un dict {passed, total, fallos}.
    'fallos' es la lista de (nombre, pista) de los ejercicios que no pasaron.
    """
    runner = runner or _runner_real
    args, env = _comando(semana)
    salida = runner(args, env)
    passed, total = parsear_resultado(salida)
    return {"passed": passed, "total": total, "fallos": parsear_fallos(salida)}


def evaluar_semana(semana, runner=None):
    """Versión simple: devuelve (passed, total)."""
    d = evaluar_semana_detallado(semana, runner)
    return d["passed"], d["total"]
