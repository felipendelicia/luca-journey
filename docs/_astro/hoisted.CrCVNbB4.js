import{E as f,b as h,o as x,k as w,i as k,p as E}from"./index.16Gn__M7.js";import{c as u,s as b}from"./sonidos.RiAsfTje.js";import"./hoisted.CXtnsQH5.js";const I=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
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
`,o=JSON.parse(document.getElementById("ej-data").textContent),c=t=>"ej:"+o.slug+":"+t,l=t=>{document.getElementById("estado").textContent=t},p=t=>String(t).replace(/[&<>]/g,e=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[e]);let y;const d=new f({doc:localStorage.getItem(c(o.exId))??o.starter,extensions:[h,w.of([k]),E(),x,f.updateListener.of(t=>{t.docChanged&&(clearTimeout(y),y=setTimeout(()=>localStorage.setItem(c(o.exId),d.state.doc.toString()),500))})],parent:document.getElementById("editor")});function S(){const t=[o.preamble];for(const e of o.ejercicios)t.push(e.id===o.exId?d.state.doc.toString():localStorage.getItem(c(e.id))??e.starter);return t.join(`


`)}let m=null,_=!1;async function v(){m||(l("⏳ Cargando Python + pytest (~20s la primera vez)…"),m=(async()=>{const e=await window.loadPyodide(),a=o.packages||[],n=a.filter(r=>r!=="flask"),s=a.includes("flask");return await e.loadPackage(["pytest",...n,...s?["micropip"]:[]]),s&&await e.runPythonAsync(`import micropip
await micropip.install('flask')`),e})());const t=await m;return _||(await t.runPythonAsync(I),_=!0),l(""),t}function j(t,e){const a=document.getElementById("result");if(e){a.innerHTML='<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+p(e)+"</code></div>",u();return}const n=t.length,s=t.filter(i=>i.ok).length,r=n>0&&s===n;r?b():u(),localStorage.setItem(c(o.exId)+":ok",r?"1":"0");let g='<div class="ejer-resumen '+(r?"win":"")+'">'+s+" / "+n+" tests"+(r?" · +"+s*10+" EXP · ¡COMPLETO! 🏅":"")+'</div><ul class="ejer-lista">';for(const i of t)g+='<li class="'+(i.ok?"ok":"no")+'"><span class="ic">'+(i.ok?"✅":"❌")+"</span><code>"+p(i.name)+"</code>"+(i.msg?'<div class="m">'+p(i.msg)+"</div>":"")+"</li>";a.innerHTML=g+"</ul>"}async function N(){const t=document.getElementById("corregir");t.disabled=!0,l("Corrigiendo…");try{const e=await v();e.globals.set("_slug",o.slug),e.globals.set("_ej",S()),e.globals.set("_test",o.test),e.globals.set("_extra",JSON.stringify(o.extra||{})),e.globals.set("_solo",JSON.stringify(o.exTests));const a=await e.runPythonAsync("correr(_slug, _ej, _test, _extra, _solo)"),n=JSON.parse(a),s={};n.tests.forEach(r=>s[r.name]=r),j(o.exTests.map(r=>s[r]).filter(Boolean),n.carga_error)}catch(e){j([],e&&e.message||String(e))}finally{t.disabled=!1,l("")}}o.exTests.length&&document.getElementById("corregir").addEventListener("click",N);document.getElementById("reset").addEventListener("click",()=>{confirm("¿Volver al código original de este ejercicio?")&&(d.dispatch({changes:{from:0,to:d.state.doc.length,insert:o.starter}}),localStorage.removeItem(c(o.exId)),localStorage.removeItem(c(o.exId)+":ok"),document.getElementById("result").innerHTML="")});
