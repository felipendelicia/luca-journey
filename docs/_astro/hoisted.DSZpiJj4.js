import{e as x}from"./editor.C-mImdU9.js";import{c as g,s as b}from"./sonidos.RiAsfTje.js";import"./hoisted.n2eibj9L.js";const h=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
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
    """Saca un mensaje corto del fallo (la última línea útil)."""
    rep = report.longrepr
    cr = getattr(rep, "reprcrash", None)
    if cr is not None and getattr(cr, "message", None):
        return cr.message.strip().splitlines()[0]
    texto = str(rep).strip()
    return texto.splitlines()[-1] if texto else "falló"


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
`,n=JSON.parse(document.getElementById("ej-data").textContent),l=t=>"ej:"+n.slug+":"+t,d=t=>{document.getElementById("estado").textContent=t},c=t=>String(t).replace(/[&<>]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[e]);let f;const u=x({doc:localStorage.getItem(l(n.exId))??n.starter,parent:document.getElementById("editor"),onRun:()=>{n.exTests.length&&v()},onChange:t=>{clearTimeout(f),f=setTimeout(()=>localStorage.setItem(l(n.exId),t),500)}});function w(){const t=[n.preamble];for(const e of n.ejercicios)t.push(e.id===n.exId?u.state.doc.toString():localStorage.getItem(l(e.id))??e.starter);return t.join(`


`)}let m=null,y=!1;async function j(){m||(d("⏳ Cargando Python + pytest (~20s la primera vez)…"),m=(async()=>{const e=await window.loadPyodide(),r=n.packages||[],o=r.filter(a=>a!=="flask"),s=r.includes("flask");return await e.loadPackage(["pytest",...o,...s?["micropip"]:[]]),s&&await e.runPythonAsync(`import micropip
await micropip.install('flask')`),e})());const t=await m;return y||(await t.runPythonAsync(h),y=!0),d(""),t}function _(t,e){const r=document.getElementById("result");if(e){r.innerHTML='<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+c(e)+"</code></div>",g();return}const o=t.length,s=t.filter(i=>i.ok).length,a=o>0&&s===o;a?b():g(),localStorage.setItem(l(n.exId)+":ok",a?"1":"0");let p='<div class="ejer-resumen '+(a?"win":"")+'">'+s+" / "+o+" tests"+(a?" · +"+s*10+" EXP · ¡COMPLETO! 🏅":"")+'</div><ul class="ejer-lista">';for(const i of t)p+='<li class="'+(i.ok?"ok":"no")+'"><span class="ic">'+(i.ok?"✅":"❌")+"</span><code>"+c(i.name)+"</code>",i.msg&&(p+='<div class="m">'+c(i.msg)+"</div>"),i.out&&(p+='<div class="ej-out"><span class="lbl">🖨️ tus prints</span>'+c(i.out)+"</div>"),p+="</li>";r.innerHTML=p+"</ul>"}async function v(){const t=document.getElementById("corregir");t.disabled=!0,d("Corrigiendo…");try{const e=await j();e.globals.set("_slug",n.slug),e.globals.set("_ej",w()),e.globals.set("_test",n.test),e.globals.set("_extra",JSON.stringify(n.extra||{})),e.globals.set("_solo",JSON.stringify(n.exTests));const r=await e.runPythonAsync("correr(_slug, _ej, _test, _extra, _solo)"),o=JSON.parse(r),s={};o.tests.forEach(a=>s[a.name]=a),_(n.exTests.map(a=>s[a]).filter(Boolean),o.carga_error)}catch(e){_([],e&&e.message||String(e))}finally{t.disabled=!1,d("")}}async function E(){const t=document.getElementById("ejecutar");t.disabled=!0,d("Ejecutando…");const e=document.getElementById("result");e.innerHTML="";try{const r=await j();r.globals.set("_code",n.preamble+`

`+u.state.doc.toString());const o=JSON.parse(await r.runPythonAsync("ejecutar(_code)"));let s='<div class="ejer-run"><span class="lbl">▶ Ejecutar</span>';o.out&&(s+='<pre class="ej-stdout">'+c(o.out)+"</pre>"),o.ret!==null&&(s+='<div class="ej-ret">↩ devuelve <code>'+c(o.ret)+"</code></div>"),!o.out&&o.ret===null&&(s+='<div class="ej-vacio">Sin salida. Agregá <code>print(...)</code> o poné una llamada como última línea (ej. <code>mi_funcion(2, 3)</code>) para ver qué devuelve.</div>'),e.innerHTML=s+"</div>"}catch(r){e.innerHTML='<div class="ejer-err">⚠️ '+c(r&&r.message||r)+"</div>"}finally{t.disabled=!1,d("")}}document.getElementById("ejecutar").addEventListener("click",E);n.exTests.length&&document.getElementById("corregir").addEventListener("click",v);document.getElementById("reset").addEventListener("click",()=>{confirm("¿Volver al código original de este ejercicio?")&&(u.dispatch({changes:{from:0,to:u.state.doc.length,insert:n.starter}}),localStorage.removeItem(l(n.exId)),localStorage.removeItem(l(n.exId)+":ok"),document.getElementById("result").innerHTML="")});
