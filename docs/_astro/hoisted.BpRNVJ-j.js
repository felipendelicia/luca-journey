import{e as N}from"./editor.C-mImdU9.js";import"./hoisted.DMWX6Ptn.js";const A=`# trazador.py — traza la ejecución del código PASO A PASO para el visualizador del libro.
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
`,u=t=>String(t??"").replace(/[&<>]/g,l=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[l]);let y=null;async function x(t){return y||(t.innerHTML='<span class="lbl">SALIDA</span>⏳ Cargando Python (~15s la primera vez)…',y=window.loadPyodide()),y}async function _(t,l,d){l.classList.add("show"),l.innerHTML='<span class="lbl">SALIDA</span>',d.disabled=!0;try{const a=await x(l),e=[];/\bnumpy\b|\bnp\./.test(t)&&e.push("numpy"),/\bpandas\b|\bpd\./.test(t)&&e.push("pandas");const n=/\bmatplotlib\b|\bplt\./.test(t);n&&e.push("matplotlib"),/\bimport sqlite3\b|\bsqlite3\./.test(t)&&e.push("sqlite3"),/\bfrom sklearn\b|\bimport sklearn\b|\bsklearn\./.test(t)&&e.push("scikit-learn");const o=/\bflask\b|\bFlask\(/.test(t);if(o&&e.push("micropip"),e.length&&(l.innerHTML='<span class="lbl">SALIDA</span>⏳ cargando librerías…',await a.loadPackage(e)),o&&await a.runPythonAsync(`import micropip
await micropip.install('flask')`),l.innerHTML='<span class="lbl">SALIDA</span>',a.setStdout({batched:i=>l.appendChild(document.createTextNode(i+`
`))}),a.setStderr({batched:i=>{const r=document.createElement("span");r.className="err",r.textContent=i+`
`,l.appendChild(r)}}),a.setStdin({stdin:()=>{const i=window.prompt("input():");return i===null?"":i}}),n&&await a.runPythonAsync("import matplotlib; matplotlib.use('AGG')"),await a.runPythonAsync(t),n){const i=await a.runPythonAsync(`import io,base64,matplotlib.pyplot as _p
_b=''
if _p.get_fignums():
    _f=io.BytesIO(); _p.gcf().savefig(_f,format='png',bbox_inches='tight',dpi=110); _p.close('all'); _b=base64.b64encode(_f.getvalue()).decode()
_b`);if(i){const r=document.createElement("img");r.className="cw-img",r.src="data:image/png;base64,"+i,l.appendChild(r)}}}catch(a){const e=document.createElement("span");e.className="err",e.textContent=`
`+(a&&a.message?a.message:a),l.appendChild(e)}finally{d.disabled=!1}}let z=!1;async function k(t,l,d){d.disabled=!0;const a=l.querySelector(".cw-viz");a&&a.remove();const e=document.createElement("div");e.className="cw-viz",e.innerHTML='<span class="lbl">VISUALIZADOR</span> ⏳ Cargando Python (~15s la primera vez)…',l.appendChild(e);try{const n=await x(e);z||(await n.runPythonAsync(A),z=!0),n.globals.set("_cod",t);const o=JSON.parse(await n.runPythonAsync("trazar(_cod)"));w(e,t,o)}catch(n){e.innerHTML='<span class="lbl">VISUALIZADOR</span><span class="err"> '+u(n&&n.message||n)+"</span>"}finally{d.disabled=!1}}function w(t,l,d){const a=l.split(`
`),e=d.pasos||[];if(!e.length){t.innerHTML='<span class="lbl">VISUALIZADOR</span> Sin pasos para mostrar.';return}let n=0;t.innerHTML="";const o=document.createElement("div");o.className="viz-head";const i=document.createElement("div");i.className="viz-cuerpo";const r=document.createElement("pre");r.className="viz-code";const c=document.createElement("div");c.className="viz-lado",i.appendChild(r),i.appendChild(c),t.appendChild(o),t.appendChild(i);function s(){const p=e[n];o.innerHTML="";const m=document.createElement("button");m.className="viz-btn",m.textContent="◀ atrás",m.disabled=n===0;const f=document.createElement("button");f.className="viz-btn",f.textContent="siguiente ▶",f.disabled=n===e.length-1;const g=document.createElement("span");g.className="viz-paso",g.textContent="👁️ Paso "+(n+1)+"/"+e.length+(p.fin?" · final":p.linea?" · línea "+p.linea:"");const h=document.createElement("button");h.className="viz-btn cerrar",h.textContent="✕",h.addEventListener("click",()=>t.remove()),m.addEventListener("click",()=>{n>0&&(n--,s())}),f.addEventListener("click",()=>{n<e.length-1&&(n++,s())}),o.appendChild(m),o.appendChild(f),o.appendChild(g),o.appendChild(h),r.innerHTML=a.map((v,L)=>'<span class="viz-ln'+(p.linea===L+1?" activa":"")+'">'+u(v===""?" ":v)+"</span>").join(`
`);const C=p.vars||{},E=Object.keys(C);let b='<div class="viz-tit">Variables</div>';b+=E.length?'<table class="viz-vars">'+E.map(v=>'<tr><td class="vn">'+u(v)+'</td><td class="vv">'+u(C[v])+"</td></tr>").join("")+"</table>":'<div class="viz-vacio">(ninguna todavía)</div>',p.salida&&(b+='<div class="viz-tit">Salida</div><pre class="viz-salida">'+u(p.salida)+"</pre>"),p.error&&(b+='<div class="viz-errbox">⚠️ '+u(p.error)+"</div>"),d.truncado&&n===e.length-1&&(b+='<div class="viz-vacio">(traza cortada a '+(e.length-1)+" pasos — código muy largo o bucle grande)</div>"),c.innerHTML=b}s()}function S(t,l){let d="",a="";const e=[];for(const c of l.split(`
`)){const s=c.trim();s.startsWith("P:")?d=s.slice(2).trim():s.startsWith("+ ")?e.push({txt:s.slice(2).trim(),ok:!0}):s.startsWith("- ")?e.push({txt:s.slice(2).trim(),ok:!1}):s.startsWith("> ")&&(a=s.slice(2).trim())}if(!d||!e.length)return;const n=document.createElement("div");n.className="quiz";const o=document.createElement("div");o.className="quiz-q",o.textContent="🤔 "+d;const i=document.createElement("div");i.className="quiz-ops";const r=document.createElement("div");r.className="quiz-expl",r.hidden=!0,r.textContent=a,e.forEach(c=>{const s=document.createElement("button");s.className="quiz-op",s.type="button",s.textContent=c.txt,s.addEventListener("click",()=>{n.classList.contains("resuelto")||(n.classList.add("resuelto"),Array.from(i.children).forEach((p,m)=>{e[m].ok&&p.classList.add("correcta")}),s.classList.add(c.ok?"elegida-ok":"elegida-mal"),a&&(r.hidden=!1))}),i.appendChild(s)}),n.appendChild(o),n.appendChild(i),n.appendChild(r),t.parentNode.replaceChild(n,t)}document.querySelectorAll(".book pre.astro-code").forEach(t=>{const l=(t.getAttribute("data-language")||"").toLowerCase(),d=t.innerText.replace(/\n+$/,"");if(l==="quiz"){S(t,d);return}const a=document.createElement("figure");a.className="cw";const e=document.createElement("div");if(e.className="cw-bar",e.innerHTML='<span class="dots"><i></i><i></i><i></i></span><span class="cw-lang">'+(l||"code")+"</span>",t.parentNode.insertBefore(a,t),a.appendChild(e),l==="python"){const n=document.createElement("div");n.className="cw-edit",a.appendChild(n),t.remove();const o=N({doc:d,parent:n,onRun:()=>_(o.state.doc.toString(),r,c)}),i=document.createElement("span");i.className="cw-hint",i.textContent="✎ editable",e.appendChild(i);const r=document.createElement("div");r.className="cw-out",r.innerHTML='<span class="lbl">SALIDA</span>';const c=document.createElement("button");c.className="cw-run",c.type="button",c.textContent="▶ ejecutar",c.addEventListener("click",()=>_(o.state.doc.toString(),r,c)),e.appendChild(c);const s=document.createElement("button");s.className="cw-run cw-viz-btn",s.type="button",s.textContent="👁️ visualizar",s.title="Ver cómo corre el código paso a paso",s.addEventListener("click",()=>k(o.state.doc.toString(),a,s)),e.appendChild(s),a.appendChild(r)}else a.appendChild(t)});
