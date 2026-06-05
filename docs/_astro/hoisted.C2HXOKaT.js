import{e as L}from"./editor.C-mImdU9.js";import"./hoisted.672GGQaZ.js";const N=`# trazador.py — traza la ejecución del código PASO A PASO para el visualizador del libro.
# Corre el código bajo sys.settrace y registra, antes de cada línea, el número de línea,
# las variables y lo impreso hasta ese momento. Devuelve JSON con la lista de pasos.
import sys
import json
import io
import contextlib

FILENAME = '<libro>'


def trazar(codigo, max_pasos=500):
    pasos = []
    buf = io.StringIO()
    g = {'__name__': '__main__'}

    def repr_seguro(v):
        try:
            r = repr(v)
        except Exception:
            return '<?>'
        return r if len(r) <= 240 else r[:240] + '…'

    def visible(k, v):
        if k.startswith('__'):
            return False
        if callable(v):
            return False
        if isinstance(v, type(sys)):  # módulos
            return False
        return True

    def snapshot(frame):
        out = {}
        for k, v in frame.f_locals.items():
            if visible(k, v):
                out[k] = repr_seguro(v)
        return out

    def tracer(frame, event, arg):
        if event == 'line' and frame.f_code.co_filename == FILENAME:
            if len(pasos) < max_pasos:
                pasos.append({'linea': frame.f_lineno, 'vars': snapshot(frame), 'salida': buf.getvalue()})
            else:
                raise _Corte()
        return tracer

    class _Corte(Exception):
        pass

    truncado = False
    error = None
    try:
        code = compile(codigo, FILENAME, 'exec')
        with contextlib.redirect_stdout(buf):
            sys.settrace(tracer)
            try:
                exec(code, g)
            except _Corte:
                truncado = True
            finally:
                sys.settrace(None)
    except _Corte:
        truncado = True
    except Exception as e:
        error = '%s: %s' % (type(e).__name__, e)

    # estado final (después de correr todo)
    fin = {}
    for k, v in g.items():
        if visible(k, v):
            fin[k] = repr_seguro(v)
    pasos.append({'linea': None, 'vars': fin, 'salida': buf.getvalue(), 'fin': True, 'error': error})

    return json.dumps({'pasos': pasos, 'truncado': truncado})
`,m=n=>String(n??"").replace(/[&<>]/g,s=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[s]);let y=null;async function w(n){return y||(n.innerHTML='<span class="lbl">SALIDA</span>⏳ Cargando Python (~15s la primera vez)…',y=window.loadPyodide()),y}async function E(n,s,d){s.classList.add("show"),s.innerHTML='<span class="lbl">SALIDA</span>',d.disabled=!0;try{const a=await w(s),e=[];/\bnumpy\b|\bnp\./.test(n)&&e.push("numpy"),/\bpandas\b|\bpd\./.test(n)&&e.push("pandas");const t=/\bmatplotlib\b|\bplt\./.test(n);t&&e.push("matplotlib"),/\bimport sqlite3\b|\bsqlite3\./.test(n)&&e.push("sqlite3"),/\bfrom sklearn\b|\bimport sklearn\b|\bsklearn\./.test(n)&&e.push("scikit-learn");const l=/\bflask\b|\bFlask\(/.test(n);if(l&&e.push("micropip"),e.length&&(s.innerHTML='<span class="lbl">SALIDA</span>⏳ cargando librerías…',await a.loadPackage(e)),l&&await a.runPythonAsync(`import micropip
await micropip.install('flask')`),s.innerHTML='<span class="lbl">SALIDA</span>',a.setStdout({batched:r=>s.appendChild(document.createTextNode(r+`
`))}),a.setStderr({batched:r=>{const i=document.createElement("span");i.className="err",i.textContent=r+`
`,s.appendChild(i)}}),a.setStdin({stdin:()=>{const r=window.prompt("input():");return r===null?"":r}}),t&&await a.runPythonAsync("import matplotlib; matplotlib.use('AGG')"),await a.runPythonAsync(n),t){const r=await a.runPythonAsync(`import io,base64,matplotlib.pyplot as _p
_b=''
if _p.get_fignums():
    _f=io.BytesIO(); _p.gcf().savefig(_f,format='png',bbox_inches='tight',dpi=110); _p.close('all'); _b=base64.b64encode(_f.getvalue()).decode()
_b`);if(r){const i=document.createElement("img");i.className="cw-img",i.src="data:image/png;base64,"+r,s.appendChild(i)}}}catch(a){const e=document.createElement("span");e.className="err",e.textContent=`
`+(a&&a.message?a.message:a),s.appendChild(e)}finally{d.disabled=!1}}let z=!1;async function x(n,s,d){d.disabled=!0;const a=s.querySelector(".cw-viz");a&&a.remove();const e=document.createElement("div");e.className="cw-viz",e.innerHTML='<span class="lbl">VISUALIZADOR</span> ⏳ Cargando Python (~15s la primera vez)…',s.appendChild(e);try{const t=await w(e);z||(await t.runPythonAsync(N),z=!0),t.globals.set("_cod",n);const l=JSON.parse(await t.runPythonAsync("trazar(_cod)"));k(e,n,l)}catch(t){e.innerHTML='<span class="lbl">VISUALIZADOR</span><span class="err"> '+m(t&&t.message||t)+"</span>"}finally{d.disabled=!1}}function k(n,s,d){const a=s.split(`
`),e=d.pasos||[];if(!e.length){n.innerHTML='<span class="lbl">VISUALIZADOR</span> Sin pasos para mostrar.';return}let t=0;n.innerHTML="";const l=document.createElement("div");l.className="viz-head";const r=document.createElement("div");r.className="viz-cuerpo";const i=document.createElement("pre");i.className="viz-code";const o=document.createElement("div");o.className="viz-lado",r.appendChild(i),r.appendChild(o),n.appendChild(l),n.appendChild(r);function c(){const p=e[t];l.innerHTML="";const u=document.createElement("button");u.className="viz-btn",u.textContent="◀ atrás",u.disabled=t===0;const b=document.createElement("button");b.className="viz-btn",b.textContent="siguiente ▶",b.disabled=t===e.length-1;const g=document.createElement("span");g.className="viz-paso",g.textContent="👁️ Paso "+(t+1)+"/"+e.length+(p.fin?" · final":p.linea?" · línea "+p.linea:"");const h=document.createElement("button");h.className="viz-btn cerrar",h.textContent="✕",h.addEventListener("click",()=>n.remove()),u.addEventListener("click",()=>{t>0&&(t--,c())}),b.addEventListener("click",()=>{t<e.length-1&&(t++,c())}),l.appendChild(u),l.appendChild(b),l.appendChild(g),l.appendChild(h),i.innerHTML=a.map((f,A)=>'<span class="viz-ln'+(p.linea===A+1?" activa":"")+'">'+m(f===""?" ":f)+"</span>").join(`
`);const _=p.vars||{},C=Object.keys(_);let v='<div class="viz-tit">Variables</div>';v+=C.length?'<table class="viz-vars">'+C.map(f=>'<tr><td class="vn">'+m(f)+'</td><td class="vv">'+m(_[f])+"</td></tr>").join("")+"</table>":'<div class="viz-vacio">(ninguna todavía)</div>',p.salida&&(v+='<div class="viz-tit">Salida</div><pre class="viz-salida">'+m(p.salida)+"</pre>"),p.error&&(v+='<div class="viz-errbox">⚠️ '+m(p.error)+"</div>"),d.truncado&&t===e.length-1&&(v+='<div class="viz-vacio">(traza cortada a '+(e.length-1)+" pasos — código muy largo o bucle grande)</div>"),o.innerHTML=v}c()}document.querySelectorAll(".book pre.astro-code").forEach(n=>{const s=(n.getAttribute("data-language")||"").toLowerCase(),d=n.innerText.replace(/\n+$/,""),a=document.createElement("figure");a.className="cw";const e=document.createElement("div");if(e.className="cw-bar",e.innerHTML='<span class="dots"><i></i><i></i><i></i></span><span class="cw-lang">'+(s||"code")+"</span>",n.parentNode.insertBefore(a,n),a.appendChild(e),s==="python"){const t=document.createElement("div");t.className="cw-edit",a.appendChild(t),n.remove();const l=L({doc:d,parent:t,onRun:()=>E(l.state.doc.toString(),i,o)}),r=document.createElement("span");r.className="cw-hint",r.textContent="✎ editable",e.appendChild(r);const i=document.createElement("div");i.className="cw-out",i.innerHTML='<span class="lbl">SALIDA</span>';const o=document.createElement("button");o.className="cw-run",o.type="button",o.textContent="▶ ejecutar",o.addEventListener("click",()=>E(l.state.doc.toString(),i,o)),e.appendChild(o);const c=document.createElement("button");c.className="cw-run cw-viz-btn",c.type="button",c.textContent="👁️ visualizar",c.title="Ver cómo corre el código paso a paso",c.addEventListener("click",()=>x(l.state.doc.toString(),a,c)),e.appendChild(c),a.appendChild(i)}else a.appendChild(n)});
