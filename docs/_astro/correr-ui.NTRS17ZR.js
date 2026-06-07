import{r as c}from"./editor.D60dbama.js";import{p as g,t as v,a as _}from"./errores.d5M1PzV8.js";const h=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
# Escribe el código del alumno como ejercicios.py + el test + helpers, con
# CURSO_MODULO=ejercicios, y ejecuta pytest recolectando el resultado por test.
import os
import sys
import json
import ast
import io
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
    lineas = [l.strip().lstrip("E").strip() for l in (crash + "\\n" + full).splitlines() if l.strip()]
    cmp_line = next(
        (l for l in lineas if l.startswith("assert ") and any(op in l for op in ("==", "!=", " in ", "<", ">"))),
        None,
    )
    if cmp_line:
        return cmp_line
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
`;function j(r){const e=r||[],s=e.includes("flask");return{packages:["pytest",...s?["micropip"]:[],...e.filter(t=>t!=="flask")],flask:s}}function w(r,e,s=1e4){const{packages:t,flask:d}=j(e),i=d?`import micropip
await micropip.install('flask')

`+r:r;let a=null;function l(){return a||(a=c(i,t,"ejecutar",[""],6e4).catch(o=>{throw a=null,o})),a}return{asegurar:l,async correr(o,p,u,m,f){return await l(),c(i,t,"correr",[o,p,u,m,f],s)},async ejecutar(o){return await l(),c(i,t,"ejecutar",[o],s)}}}const n=r=>String(r??"").replace(/[&<>]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[e]);function y(r){if(/⏱️|tardó demasiado/.test(r))return'<div class="ejer-err">'+n(r)+"</div>";const e=v(r);return e?'<div class="ejer-err err-amigable"><div class="err-tit">'+e.ico+" "+n(e.titulo)+(e.linea?' <span class="err-linea">línea '+e.linea+"</span>":"")+'</div><div class="err-causa">'+n(e.causa)+'</div><div class="err-fix">💡 '+n(e.fix)+'</div><details class="err-raw"><summary>Ver el error técnico</summary><code>'+n(r)+"</code></details></div>":'<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+n(r)+"</code></div>"}function k(r){let e='<ul class="ejer-lista">';for(const s of r){if(e+='<li class="'+(s.ok?"ok":"no")+'"><span class="ic">'+(s.ok?"✅":"❌")+"</span><code>"+n(s.name)+"</code>",s.msg){const t=_(s.msg);e+='<div class="m">💡 '+n(t)+"</div>",t!==s.msg&&(e+='<details class="m-raw"><summary>detalle del test</summary><code>'+n(s.msg)+"</code></details>")}s.out&&(e+='<div class="ej-out"><span class="lbl">🖨️ tus prints</span>'+n(s.out)+"</div>"),e+="</li>"}return e+"</ul>"}function E(r){let e='<div class="ejer-run"><span class="lbl">▶ Ejecutar</span>';r.out&&g(r.out)?e+=y(r.out):r.out&&(e+='<pre class="ej-stdout">'+n(r.out)+"</pre>");const s=r.ret!==null&&r.ret!==void 0;return s&&(e+='<div class="ej-ret">↩ devuelve <code>'+n(r.ret)+"</code></div>"),!r.out&&!s&&(e+='<div class="ej-vacio">Sin salida. Agregá <code>print(...)</code> o poné una llamada como última línea para ver qué devuelve.</div>'),e+"</div>"}export{y as b,w as c,k as l,h as r,E as s};
