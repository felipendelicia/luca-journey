import{e as h}from"./editor.C-mImdU9.js";import{c as f,s as x}from"./sonidos.RiAsfTje.js";import"./hoisted.B6Up9u9X.js";const w=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
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
                self.res.append({"name": nombre, "ok": report.passed, "msg": "" if report.passed else _msg(report)})
            elif report.when == "setup" and report.outcome in ("failed", "error"):
                self.res.append({"name": nombre, "ok": False, "msg": _msg(report)})

        def pytest_collectreport(self, report):
            if report.failed and self.carga is None:
                self.carga = _msg(report)

    rec = Recolector()
    args = ["-p", "no:cacheprovider", "-q", "--no-header", "-o", "addopts="]
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
`,o=JSON.parse(document.getElementById("ej-data").textContent),c=t=>"ej:"+o.slug+":"+t,l=t=>{document.getElementById("estado").textContent=t},d=t=>String(t).replace(/[&<>]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[e]);let u;const m=h({doc:localStorage.getItem(c(o.exId))??o.starter,parent:document.getElementById("editor"),onRun:()=>{o.exTests.length&&j()},onChange:t=>{clearTimeout(u),u=setTimeout(()=>localStorage.setItem(c(o.exId),t),500)}});function k(){const t=[o.preamble];for(const e of o.ejercicios)t.push(e.id===o.exId?m.state.doc.toString():localStorage.getItem(c(e.id))??e.starter);return t.join(`


`)}let p=null,y=!1;async function E(){p||(l("⏳ Cargando Python + pytest (~20s la primera vez)…"),p=(async()=>{const e=await window.loadPyodide(),a=o.packages||[],s=a.filter(r=>r!=="flask"),n=a.includes("flask");return await e.loadPackage(["pytest",...s,...n?["micropip"]:[]]),n&&await e.runPythonAsync(`import micropip
await micropip.install('flask')`),e})());const t=await p;return y||(await t.runPythonAsync(w),y=!0),l(""),t}function _(t,e){const a=document.getElementById("result");if(e){a.innerHTML='<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+d(e)+"</code></div>",f();return}const s=t.length,n=t.filter(i=>i.ok).length,r=s>0&&n===s;r?x():f(),localStorage.setItem(c(o.exId)+":ok",r?"1":"0");let g='<div class="ejer-resumen '+(r?"win":"")+'">'+n+" / "+s+" tests"+(r?" · +"+n*10+" EXP · ¡COMPLETO! 🏅":"")+'</div><ul class="ejer-lista">';for(const i of t)g+='<li class="'+(i.ok?"ok":"no")+'"><span class="ic">'+(i.ok?"✅":"❌")+"</span><code>"+d(i.name)+"</code>"+(i.msg?'<div class="m">'+d(i.msg)+"</div>":"")+"</li>";a.innerHTML=g+"</ul>"}async function j(){const t=document.getElementById("corregir");t.disabled=!0,l("Corrigiendo…");try{const e=await E();e.globals.set("_slug",o.slug),e.globals.set("_ej",k()),e.globals.set("_test",o.test),e.globals.set("_extra",JSON.stringify(o.extra||{})),e.globals.set("_solo",JSON.stringify(o.exTests));const a=await e.runPythonAsync("correr(_slug, _ej, _test, _extra, _solo)"),s=JSON.parse(a),n={};s.tests.forEach(r=>n[r.name]=r),_(o.exTests.map(r=>n[r]).filter(Boolean),s.carga_error)}catch(e){_([],e&&e.message||String(e))}finally{t.disabled=!1,l("")}}o.exTests.length&&document.getElementById("corregir").addEventListener("click",j);document.getElementById("reset").addEventListener("click",()=>{confirm("¿Volver al código original de este ejercicio?")&&(m.dispatch({changes:{from:0,to:m.state.doc.length,insert:o.starter}}),localStorage.removeItem(c(o.exId)),localStorage.removeItem(c(o.exId)+":ok"),document.getElementById("result").innerHTML="")});
