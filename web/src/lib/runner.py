# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
# Escribe el código del alumno como ejercicios.py + el test + helpers, con
# CURSO_MODULO=ejercicios, y ejecuta pytest recolectando el resultado por test.
import os
import sys
import json


def _msg(report):
    """Saca un mensaje corto del fallo (la última línea útil)."""
    rep = report.longrepr
    cr = getattr(rep, "reprcrash", None)
    if cr is not None and getattr(cr, "message", None):
        return cr.message.strip().splitlines()[0]
    texto = str(rep).strip()
    return texto.splitlines()[-1] if texto else "falló"


def correr(slug, ejercicios_code, test_code, extra_json):
    import pytest

    extra = json.loads(extra_json or "{}")
    d = "/work/" + slug
    os.makedirs(d, exist_ok=True)
    with open(d + "/ejercicios.py", "w") as f:
        f.write(ejercicios_code)
    with open(d + "/soluciones.py", "w") as f:  # respaldo, no se usa para corregir
        f.write(ejercicios_code)
    for nombre, contenido in extra.items():
        with open(d + "/" + nombre, "w") as f:
            f.write(contenido or "")
    with open(d + "/test_ejercicios.py", "w") as f:
        f.write(test_code)

    os.environ["CURSO_MODULO"] = "ejercicios"
    if d not in sys.path:
        sys.path.insert(0, d)
    os.chdir(d)

    # releer el código nuevo en cada corrida
    for m in list(sys.modules):
        if m.startswith("test_ejercicios") or "_ejercicios" in m or "_soluciones" in m or m == "ejercicios":
            del sys.modules[m]

    class Recolector:
        def __init__(self):
            self.res = []
            self.carga = None

        def pytest_runtest_logreport(self, report):
            nombre = report.nodeid.split("::")[-1]
            if report.when == "call":
                self.res.append({"name": nombre, "ok": report.passed, "msg": "" if report.passed else _msg(report)})
            elif report.when == "setup" and report.outcome in ("failed", "error"):
                self.res.append({"name": nombre, "ok": False, "msg": _msg(report)})

        def pytest_collectreport(self, report):
            if report.failed and self.carga is None:
                self.carga = _msg(report)

    rec = Recolector()
    try:
        pytest.main(
            ["-p", "no:cacheprovider", "-q", "--no-header", "-o", "addopts=", d + "/test_ejercicios.py"],
            plugins=[rec],
        )
    except SystemExit:
        pass
    except Exception as e:
        return json.dumps({"carga_error": "%s: %s" % (type(e).__name__, e), "tests": rec.res})

    carga = rec.carga
    if carga is None and not rec.res:
        carga = "No se pudieron cargar los tests (revisá errores de sintaxis)."
    return json.dumps({"carga_error": carga, "tests": rec.res})
