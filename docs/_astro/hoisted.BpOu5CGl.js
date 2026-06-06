import{e as N}from"./editor.C-mImdU9.js";import{t as w}from"./errores.gFQpAbai.js";import"./hoisted.B5eO_-ub.js";const A=`# trazador.py — traza la ejecución del código PASO A PASO para el visualizador del libro.
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
`,m=t=>String(t??"").replace(/[&<>]/g,l=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[l]);let y=null;async function z(t){return y||(t.innerHTML='<span class="lbl">SALIDA</span><span class="py-load"><span class="py-ball"></span>Preparando Python… la primera vez tarda ~15s; después es <b>instantáneo</b> ⚡</span>',y=window.loadPyodide()),y}async function _(t,l,d){l.classList.add("show"),l.innerHTML='<span class="lbl">SALIDA</span>',d.disabled=!0;try{const a=await z(l),n=[];/\bnumpy\b|\bnp\./.test(t)&&n.push("numpy"),/\bpandas\b|\bpd\./.test(t)&&n.push("pandas");const e=/\bmatplotlib\b|\bplt\./.test(t);e&&n.push("matplotlib"),/\bimport sqlite3\b|\bsqlite3\./.test(t)&&n.push("sqlite3"),/\bfrom sklearn\b|\bimport sklearn\b|\bsklearn\./.test(t)&&n.push("scikit-learn");const r=/\bflask\b|\bFlask\(/.test(t);if(r&&n.push("micropip"),n.length&&(l.innerHTML='<span class="lbl">SALIDA</span>⏳ cargando librerías…',await a.loadPackage(n)),r&&await a.runPythonAsync(`import micropip
await micropip.install('flask')`),l.innerHTML='<span class="lbl">SALIDA</span>',a.setStdout({batched:s=>l.appendChild(document.createTextNode(s+`
`))}),a.setStderr({batched:s=>{const o=document.createElement("span");o.className="err",o.textContent=s+`
`,l.appendChild(o)}}),a.setStdin({stdin:()=>{const s=window.prompt("input():");return s===null?"":s}}),e&&await a.runPythonAsync("import matplotlib; matplotlib.use('AGG')"),await a.runPythonAsync(t),e){const s=await a.runPythonAsync(`import io,base64,matplotlib.pyplot as _p
_b=''
if _p.get_fignums():
    _f=io.BytesIO(); _p.gcf().savefig(_f,format='png',bbox_inches='tight',dpi=110); _p.close('all'); _b=base64.b64encode(_f.getvalue()).decode()
_b`);if(s){const o=document.createElement("img");o.className="cw-img",o.src="data:image/png;base64,"+s,l.appendChild(o)}}}catch(a){const n=a&&a.message?a.message:String(a),e=w(n);if(e){const s=document.createElement("div");s.className="cw-errfix",s.innerHTML=e.ico+" <b>"+m(e.titulo)+"</b>"+(e.linea?" (línea "+e.linea+")":"")+" — "+m(e.causa)+"<br>💡 "+m(e.fix),l.appendChild(s)}const r=document.createElement("span");r.className="err",r.textContent=`
`+n,l.appendChild(r)}finally{d.disabled=!1}}let x=!1;async function k(t,l,d){d.disabled=!0;const a=l.querySelector(".cw-viz");a&&a.remove();const n=document.createElement("div");n.className="cw-viz",n.innerHTML='<span class="lbl">VISUALIZADOR</span> ⏳ Cargando Python (~15s la primera vez)…',l.appendChild(n);try{const e=await z(n);x||(await e.runPythonAsync(A),x=!0),e.globals.set("_cod",t);const r=JSON.parse(await e.runPythonAsync("trazar(_cod)"));S(n,t,r)}catch(e){n.innerHTML='<span class="lbl">VISUALIZADOR</span><span class="err"> '+m(e&&e.message||e)+"</span>"}finally{d.disabled=!1}}function S(t,l,d){const a=l.split(`
`),n=d.pasos||[];if(!n.length){t.innerHTML='<span class="lbl">VISUALIZADOR</span> Sin pasos para mostrar.';return}let e=0;t.innerHTML="";const r=document.createElement("div");r.className="viz-head";const s=document.createElement("div");s.className="viz-cuerpo";const o=document.createElement("pre");o.className="viz-code";const c=document.createElement("div");c.className="viz-lado",s.appendChild(o),s.appendChild(c),t.appendChild(r),t.appendChild(s);function i(){const p=n[e];r.innerHTML="";const u=document.createElement("button");u.className="viz-btn",u.textContent="◀ atrás",u.disabled=e===0;const f=document.createElement("button");f.className="viz-btn",f.textContent="siguiente ▶",f.disabled=e===n.length-1;const g=document.createElement("span");g.className="viz-paso",g.textContent="👁️ Paso "+(e+1)+"/"+n.length+(p.fin?" · final":p.linea?" · línea "+p.linea:"");const h=document.createElement("button");h.className="viz-btn cerrar",h.textContent="✕",h.addEventListener("click",()=>t.remove()),u.addEventListener("click",()=>{e>0&&(e--,i())}),f.addEventListener("click",()=>{e<n.length-1&&(e++,i())}),r.appendChild(u),r.appendChild(f),r.appendChild(g),r.appendChild(h),o.innerHTML=a.map((v,L)=>'<span class="viz-ln'+(p.linea===L+1?" activa":"")+'">'+m(v===""?" ":v)+"</span>").join(`
`);const E=p.vars||{},C=Object.keys(E);let b='<div class="viz-tit">Variables</div>';b+=C.length?'<table class="viz-vars">'+C.map(v=>'<tr><td class="vn">'+m(v)+'</td><td class="vv">'+m(E[v])+"</td></tr>").join("")+"</table>":'<div class="viz-vacio">(ninguna todavía)</div>',p.salida&&(b+='<div class="viz-tit">Salida</div><pre class="viz-salida">'+m(p.salida)+"</pre>"),p.error&&(b+='<div class="viz-errbox">⚠️ '+m(p.error)+"</div>"),d.truncado&&e===n.length-1&&(b+='<div class="viz-vacio">(traza cortada a '+(n.length-1)+" pasos — código muy largo o bucle grande)</div>"),c.innerHTML=b}i()}function T(t,l){let d="",a="";const n=[];for(const c of l.split(`
`)){const i=c.trim();i.startsWith("P:")?d=i.slice(2).trim():i.startsWith("+ ")?n.push({txt:i.slice(2).trim(),ok:!0}):i.startsWith("- ")?n.push({txt:i.slice(2).trim(),ok:!1}):i.startsWith("> ")&&(a=i.slice(2).trim())}if(!d||!n.length)return;const e=document.createElement("div");e.className="quiz";const r=document.createElement("div");r.className="quiz-q",r.textContent="🤔 "+d;const s=document.createElement("div");s.className="quiz-ops";const o=document.createElement("div");o.className="quiz-expl",o.hidden=!0,o.textContent=a,n.forEach(c=>{const i=document.createElement("button");i.className="quiz-op",i.type="button",i.textContent=c.txt,i.addEventListener("click",()=>{e.classList.contains("resuelto")||(e.classList.add("resuelto"),Array.from(s.children).forEach((p,u)=>{n[u].ok&&p.classList.add("correcta")}),i.classList.add(c.ok?"elegida-ok":"elegida-mal"),a&&(o.hidden=!1))}),s.appendChild(i)}),e.appendChild(r),e.appendChild(s),e.appendChild(o),t.parentNode.replaceChild(e,t)}document.querySelectorAll(".book pre.astro-code").forEach(t=>{const l=(t.getAttribute("data-language")||"").toLowerCase(),d=t.innerText.replace(/\n+$/,"");if(l==="quiz"){T(t,d);return}const a=document.createElement("figure");a.className="cw";const n=document.createElement("div");if(n.className="cw-bar",n.innerHTML='<span class="dots"><i></i><i></i><i></i></span><span class="cw-lang">'+(l||"code")+"</span>",t.parentNode.insertBefore(a,t),a.appendChild(n),l==="python"){const e=document.createElement("div");e.className="cw-edit",a.appendChild(e),t.remove();const r=N({doc:d,parent:e,onRun:()=>_(r.state.doc.toString(),o,c)}),s=document.createElement("span");s.className="cw-hint",s.textContent="✎ editable",n.appendChild(s);const o=document.createElement("div");o.className="cw-out",o.innerHTML='<span class="lbl">SALIDA</span>';const c=document.createElement("button");c.className="cw-run",c.type="button",c.textContent="▶ ejecutar",c.addEventListener("click",()=>_(r.state.doc.toString(),o,c)),n.appendChild(c);const i=document.createElement("button");i.className="cw-run cw-viz-btn",i.type="button",i.textContent="👁️ visualizar",i.title="Ver cómo corre el código paso a paso",i.addEventListener("click",()=>k(r.state.doc.toString(),a,i)),n.appendChild(i),a.appendChild(o)}else a.appendChild(t)});
