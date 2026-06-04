import{E as u,b as j,o as h,k as x,i as w,p as E}from"./index.16Gn__M7.js";const b=`# runner.py — corre los tests de una semana en el navegador con pytest real (Pyodide).
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
`,n=JSON.parse(document.getElementById("ej-data").textContent),i=e=>"ej:"+n.slug+":"+e,l=e=>{document.getElementById("estado").textContent=e},p=e=>String(e).replace(/[&<>]/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[t]);let f;const d=new u({doc:localStorage.getItem(i(n.exId))??n.starter,extensions:[j,x.of([w]),E(),h,u.updateListener.of(e=>{e.docChanged&&(clearTimeout(f),f=setTimeout(()=>localStorage.setItem(i(n.exId),d.state.doc.toString()),500))})],parent:document.getElementById("editor")});function I(){const e=[n.preamble];for(const t of n.ejercicios)e.push(t.id===n.exId?d.state.doc.toString():localStorage.getItem(i(t.id))??t.starter);return e.join(`


`)}let g=null,y=!1;async function k(){g||(l("⏳ Cargando Python + pytest (~20s la primera vez)…"),g=(async()=>{const t=await window.loadPyodide();return await t.loadPackage(["pytest",...n.packages||[]]),t})());const e=await g;return y||(await e.runPythonAsync(b),y=!0),l(""),e}function _(e,t){const c=document.getElementById("result");if(t){c.innerHTML='<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>'+p(t)+"</code></div>";return}const s=e.length,a=e.filter(r=>r.ok).length,o=s>0&&a===s;localStorage.setItem(i(n.exId)+":ok",o?"1":"0");let m='<div class="ejer-resumen '+(o?"win":"")+'">'+a+" / "+s+" tests"+(o?" · +"+a*10+" EXP · ¡COMPLETO! 🏅":"")+'</div><ul class="ejer-lista">';for(const r of e)m+='<li class="'+(r.ok?"ok":"no")+'"><span class="ic">'+(r.ok?"✅":"❌")+"</span><code>"+p(r.name)+"</code>"+(r.msg?'<div class="m">'+p(r.msg)+"</div>":"")+"</li>";c.innerHTML=m+"</ul>"}async function v(){const e=document.getElementById("corregir");e.disabled=!0,l("Corrigiendo…");try{const t=await k();t.globals.set("_slug",n.slug),t.globals.set("_ej",I()),t.globals.set("_test",n.test),t.globals.set("_extra",JSON.stringify(n.extra||{})),t.globals.set("_solo",JSON.stringify(n.exTests));const c=await t.runPythonAsync("correr(_slug, _ej, _test, _extra, _solo)"),s=JSON.parse(c),a={};s.tests.forEach(o=>a[o.name]=o),_(n.exTests.map(o=>a[o]).filter(Boolean),s.carga_error)}catch(t){_([],t&&t.message||String(t))}finally{e.disabled=!1,l("")}}n.exTests.length&&document.getElementById("corregir").addEventListener("click",v);document.getElementById("reset").addEventListener("click",()=>{confirm("¿Volver al código original de este ejercicio?")&&(d.dispatch({changes:{from:0,to:d.state.doc.length,insert:n.starter}}),localStorage.removeItem(i(n.exId)),localStorage.removeItem(i(n.exId)+":ok"),document.getElementById("result").innerHTML="")});document.getElementById("ver-sol").addEventListener("click",()=>{const e=document.getElementById("sol-box");document.getElementById("sol-pre").textContent=n.solucion||"(sin solución)",e.hidden=!e.hidden,e.hidden||(e.open=!0)});
