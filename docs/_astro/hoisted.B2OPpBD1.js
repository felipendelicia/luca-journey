import{E as u,b as h,o as x,k as w,i as E,p as k}from"./index.16Gn__M7.js";import{s as f,a as b}from"./sonidos.IWHAmFk-.js";const I=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
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
`,o=JSON.parse(document.getElementById("ej-data").textContent),c=e=>"ej:"+o.slug+":"+e,l=e=>{document.getElementById("estado").textContent=e},p=e=>String(e).replace(/[&<>]/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[t]);let y;const d=new u({doc:localStorage.getItem(c(o.exId))??o.starter,extensions:[h,w.of([E]),k(),x,u.updateListener.of(e=>{e.docChanged&&(clearTimeout(y),y=setTimeout(()=>localStorage.setItem(c(o.exId),d.state.doc.toString()),500))})],parent:document.getElementById("editor")});function v(){const e=[o.preamble];for(const t of o.ejercicios)e.push(t.id===o.exId?d.state.doc.toString():localStorage.getItem(c(t.id))??t.starter);return e.join(`


`)}let m=null,_=!1;async function S(){m||(l("⏳ Cargando Python + pytest (~20s la primera vez)…"),m=(async()=>{const t=await window.loadPyodide(),a=o.packages||[],r=a.filter(n=>n!=="flask"),s=a.includes("flask");return await t.loadPackage(["pytest",...r,...s?["micropip"]:[]]),s&&await t.runPythonAsync(`import micropip
await micropip.install('flask')`),t})());const e=await m;return _||(await e.runPythonAsync(I),_=!0),l(""),e}function j(e,t){const a=document.getElementById("result");if(t){a.innerHTML='<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+p(t)+"</code></div>",f();return}const r=e.length,s=e.filter(i=>i.ok).length,n=r>0&&s===r;n?b():f(),localStorage.setItem(c(o.exId)+":ok",n?"1":"0");let g='<div class="ejer-resumen '+(n?"win":"")+'">'+s+" / "+r+" tests"+(n?" · +"+s*10+" EXP · ¡COMPLETO! 🏅":"")+'</div><ul class="ejer-lista">';for(const i of e)g+='<li class="'+(i.ok?"ok":"no")+'"><span class="ic">'+(i.ok?"✅":"❌")+"</span><code>"+p(i.name)+"</code>"+(i.msg?'<div class="m">'+p(i.msg)+"</div>":"")+"</li>";a.innerHTML=g+"</ul>"}async function B(){const e=document.getElementById("corregir");e.disabled=!0,l("Corrigiendo…");try{const t=await S();t.globals.set("_slug",o.slug),t.globals.set("_ej",v()),t.globals.set("_test",o.test),t.globals.set("_extra",JSON.stringify(o.extra||{})),t.globals.set("_solo",JSON.stringify(o.exTests));const a=await t.runPythonAsync("correr(_slug, _ej, _test, _extra, _solo)"),r=JSON.parse(a),s={};r.tests.forEach(n=>s[n.name]=n),j(o.exTests.map(n=>s[n]).filter(Boolean),r.carga_error)}catch(t){j([],t&&t.message||String(t))}finally{e.disabled=!1,l("")}}o.exTests.length&&document.getElementById("corregir").addEventListener("click",B);document.getElementById("reset").addEventListener("click",()=>{confirm("¿Volver al código original de este ejercicio?")&&(d.dispatch({changes:{from:0,to:d.state.doc.length,insert:o.starter}}),localStorage.removeItem(c(o.exId)),localStorage.removeItem(c(o.exId)+":ok"),document.getElementById("result").innerHTML="")});document.getElementById("ver-sol").addEventListener("click",()=>{const e=document.getElementById("sol-box");document.getElementById("sol-pre").textContent=o.solucion||"(sin solución)",e.hidden=!e.hidden,e.hidden||(e.open=!0)});
