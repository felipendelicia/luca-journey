# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
# Escribe el código del alumno como ejercicios.py + el test + helpers, con
# CURSO_MODULO=ejercicios, y ejecuta pytest recolectando el resultado por test.
import os
import sys
import json
import ast
import io
import re
import contextlib
import traceback


def ejecutar(code):
    """Corre el código del alumno y devuelve {out, ret}: lo impreso (prints) y el valor
    de la última expresión (si la última línea es una expresión, ej. una llamada)."""
    g = {"__name__": "__main__"}
    buf = io.StringIO()
    ret = None
    try:
        tree = ast.parse(code)
        ultimo = tree.body.pop() if (tree.body and isinstance(tree.body[-1], ast.Expr)) else None
        with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
            exec(compile(ast.Module(tree.body, []), "<ejercicio>", "exec"), g)
            if ultimo is not None:
                val = eval(compile(ast.Expression(ultimo.value), "<ejercicio>", "eval"), g)
                if val is not None:
                    ret = repr(val)
    except Exception:
        buf.write(traceback.format_exc())
    return json.dumps({"out": buf.getvalue(), "ret": ret})


def _msg(report):
    """Mensaje del fallo. Priorizamos la línea de COMPARACIÓN con valores reales
    ('assert <lo que devolvió tu función> == <lo esperado>', que pytest arma al reescribir el assert),
    para que se vea QUÉ devolvió tu función. Si no hay, caemos al mensaje custom / la 1ra línea útil."""
    rep = report.longrepr
    cr = getattr(rep, "reprcrash", None)
    crash = cr.message if (cr is not None and getattr(cr, "message", None)) else ""
    full = str(rep) if rep is not None else ""
    # pytest prefija las líneas de detalle con "E"; las limpiamos.
    lineas = [l.strip().lstrip("E").strip() for l in (crash + "\n" + full).splitlines() if l.strip()]
    # la línea de comparación puede venir sola ('assert 75 == 50') o embebida
    # ('AssertionError: assert 'Onix' == 'Pikachu''); en ambos casos extraemos desde 'assert '.
    cmp_line = next(
        (l for l in lineas if "assert " in l and any(op in l for op in ("==", "!=", " in ", " is ", "<", ">"))),
        None,
    )
    if cmp_line:
        i = cmp_line.find("assert ")
        return cmp_line[i:] if i >= 0 else cmp_line
    # la EXCEPCIÓN real de Python (SyntaxError/NameError/IndentationError/…): la ÚLTIMA línea que parece
    # excepción. Clave cuando el módulo no importa por un error de sintaxis (si no, se ve el path interno de pytest).
    errs = [l for l in lineas if re.match(r"^[A-Za-z_][\w.]*(Error|Exception)\s*:", l)]
    if errs:
        return errs[-1]
    # pytest.raises que no se cumplió: 'Failed: DID NOT RAISE <class ...>'. La traducimos aparte.
    noraise = next((l for l in lineas if "DID NOT RAISE" in l), None)
    if noraise:
        i = noraise.find("DID NOT RAISE")
        return "DID NOT RAISE" + noraise[i + len("DID NOT RAISE"):]
    custom = next((l for l in lineas if l.startswith("AssertionError:")), None)
    if custom:
        return custom
    return lineas[0] if lineas else "falló"


def correr(slug, ejercicios_code, test_code, extra_json, solo_json="[]"):
    import pytest

    solo = json.loads(solo_json or "[]")

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
                salida = (getattr(report, "capstdout", "") or "").strip()
                self.res.append({"name": nombre, "ok": report.passed, "msg": "" if report.passed else _msg(report), "out": salida})
            elif report.when == "setup" and report.outcome in ("failed", "error"):
                self.res.append({"name": nombre, "ok": False, "msg": _msg(report), "out": (getattr(report, "capstdout", "") or "").strip()})

        def pytest_collectreport(self, report):
            if report.failed and self.carga is None:
                self.carga = _msg(report)

    rec = Recolector()
    args = ["-p", "no:cacheprovider", "-q", "--no-header", "--capture=sys", "-o", "addopts="]
    if solo:
        args += [d + "/test_ejercicios.py::" + n for n in solo]
    else:
        args += [d + "/test_ejercicios.py"]
    try:
        pytest.main(args, plugins=[rec])
    except SystemExit:
        pass
    except Exception as e:
        return json.dumps({"carga_error": "%s: %s" % (type(e).__name__, e), "tests": rec.res})

    carga = rec.carga
    if carga is None and not rec.res:
        carga = "No se pudieron cargar los tests (revisá errores de sintaxis)."
    return json.dumps({"carga_error": carga, "tests": rec.res})
