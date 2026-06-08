import{e as z,r as N,a as _}from"./editor.D60dbama.js";import{t as A}from"./errores.CzSJvCsS.js";import"./hoisted.KRZauTwm.js";const S=`# trazador.py — traza la ejecución del código PASO A PASO para el visualizador del libro.
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
`,m=e=>String(e??"").replace(/[&<>]/g,t=>({"&":"&amp;","<":"&lt;",">":"&gt;"})[t]);let E=null;async function T(e){return E||(e.innerHTML='<span class="lbl">SALIDA</span><span class="py-load"><span class="py-ball"></span>Preparando Python… la primera vez tarda ~15s; después es <b>instantáneo</b> ⚡</span>',E=window.loadPyodide()),E}const I=1e4;let y=null;function C(){return y||(y=_("",[],"",()=>{},6e4).catch(e=>{throw y=null,e})),y}function M(e){const t=[];return/\bnumpy\b|\bnp\./.test(e)&&t.push("numpy"),/\bpandas\b|\bpd\./.test(e)&&t.push("pandas"),/\bmatplotlib\b|\bplt\./.test(e)&&t.push("matplotlib"),/\bimport sqlite3\b|\bsqlite3\./.test(e)&&t.push("sqlite3"),/\bfrom sklearn\b|\bimport sklearn\b|\bsklearn\./.test(e)&&t.push("scikit-learn"),/\bflask\b|\bFlask\(/.test(e)&&t.push("micropip"),t}function P(e,t){const a=A(e);if(a){const n=document.createElement("div");n.className="cw-errfix",n.innerHTML=a.ico+" <b>"+m(a.titulo)+"</b>"+(a.linea?" (línea "+a.linea+")":"")+" — "+m(a.causa)+"<br>💡 "+m(a.fix),t.appendChild(n)}const s=document.createElement("span");s.className="err",s.textContent=`
`+e,t.appendChild(s)}async function x(e,t,a){t.classList.add("show"),t.innerHTML='<span class="lbl">SALIDA</span>',a.disabled=!0;try{/\binput\s*\(/.test(e)?await H(e,t):await q(e,t)}catch(s){P(s&&s.message?s.message:String(s),t)}finally{a.disabled=!1}}async function q(e,t){const a=M(e),n=/\bflask\b|\bFlask\(/.test(e)?`import micropip
await micropip.install('flask')`:"";t.innerHTML='<span class="lbl">SALIDA</span><span class="py-load"><span class="py-ball"></span>Preparando Python… la primera vez tarda ~15s; después es <b>instantáneo</b> ⚡</span>',await C(),t.innerHTML='<span class="lbl">SALIDA</span>';const i=await _(n,a,e,(r,c)=>{if(c){const o=document.createElement("span");o.className="err",o.textContent=r,t.appendChild(o)}else t.appendChild(document.createTextNode(r))},I);if(i){const r=document.createElement("img");r.className="cw-img",r.src="data:image/png;base64,"+i,t.appendChild(r)}}async function H(e,t){const a=await T(t),s=[];/\bnumpy\b|\bnp\./.test(e)&&s.push("numpy"),/\bpandas\b|\bpd\./.test(e)&&s.push("pandas");const n=/\bmatplotlib\b|\bplt\./.test(e);n&&s.push("matplotlib"),/\bimport sqlite3\b|\bsqlite3\./.test(e)&&s.push("sqlite3"),/\bfrom sklearn\b|\bimport sklearn\b|\bsklearn\./.test(e)&&s.push("scikit-learn");const i=/\bflask\b|\bFlask\(/.test(e);if(i&&s.push("micropip"),s.length&&(t.innerHTML='<span class="lbl">SALIDA</span>⏳ cargando librerías…',await a.loadPackage(s)),i&&await a.runPythonAsync(`import micropip
await micropip.install('flask')`),t.innerHTML='<span class="lbl">SALIDA</span>',a.setStdout({batched:r=>t.appendChild(document.createTextNode(r+`
`))}),a.setStderr({batched:r=>{const c=document.createElement("span");c.className="err",c.textContent=r+`
`,t.appendChild(c)}}),a.setStdin({stdin:()=>{const r=window.prompt("input():");return r===null?"":r}}),n&&await a.runPythonAsync("import matplotlib; matplotlib.use('AGG')"),await a.runPythonAsync(e),n){const r=await a.runPythonAsync(`import io,base64,matplotlib.pyplot as _p
_b=''
if _p.get_fignums():
    _f=io.BytesIO(); _p.gcf().savefig(_f,format='png',bbox_inches='tight',dpi=110); _p.close('all'); _b=base64.b64encode(_f.getvalue()).decode()
_b`);if(r){const c=document.createElement("img");c.className="cw-img",c.src="data:image/png;base64,"+r,t.appendChild(c)}}}async function F(e,t,a){a.disabled=!0;const s=t.querySelector(".cw-viz");s&&s.remove();const n=document.createElement("div");n.className="cw-viz",n.innerHTML='<span class="lbl">VISUALIZADOR</span> ⏳ Cargando Python (~15s la primera vez)…',t.appendChild(n);try{await C();const i=JSON.parse(await N(S,[],"trazar",[e],15e3));D(n,e,i)}catch(i){n.innerHTML='<span class="lbl">VISUALIZADOR</span><span class="err"> '+m(i&&i.message||i)+"</span>"}finally{a.disabled=!1}}function D(e,t,a){const s=t.split(`
`),n=a.pasos||[];if(!n.length){e.innerHTML='<span class="lbl">VISUALIZADOR</span> Sin pasos para mostrar.';return}let i=0;e.innerHTML="";const r=document.createElement("div");r.className="viz-head";const c=document.createElement("div");c.className="viz-cuerpo";const o=document.createElement("pre");o.className="viz-code";const p=document.createElement("div");p.className="viz-lado",c.appendChild(o),c.appendChild(p),e.appendChild(r),e.appendChild(c);function l(){const d=n[i];r.innerHTML="";const u=document.createElement("button");u.className="viz-btn",u.textContent="◀ atrás",u.disabled=i===0;const b=document.createElement("button");b.className="viz-btn",b.textContent="siguiente ▶",b.disabled=i===n.length-1;const g=document.createElement("span");g.className="viz-paso",g.textContent="👁️ Paso "+(i+1)+"/"+n.length+(d.fin?" · final":d.linea?" · línea "+d.linea:"");const h=document.createElement("button");h.className="viz-btn cerrar",h.textContent="✕",h.addEventListener("click",()=>e.remove()),u.addEventListener("click",()=>{i>0&&(i--,l())}),b.addEventListener("click",()=>{i<n.length-1&&(i++,l())}),r.appendChild(u),r.appendChild(b),r.appendChild(g),r.appendChild(h),o.innerHTML=s.map((v,w)=>'<span class="viz-ln'+(d.linea===w+1?" activa":"")+'">'+m(v===""?" ":v)+"</span>").join(`
`);const k=d.vars||{},L=Object.keys(k);let f='<div class="viz-tit">Variables</div>';f+=L.length?'<table class="viz-vars">'+L.map(v=>'<tr><td class="vn">'+m(v)+'</td><td class="vv">'+m(k[v])+"</td></tr>").join("")+"</table>":'<div class="viz-vacio">(ninguna todavía)</div>',d.salida&&(f+='<div class="viz-tit">Salida</div><pre class="viz-salida">'+m(d.salida)+"</pre>"),d.error&&(f+='<div class="viz-errbox">⚠️ '+m(d.error)+"</div>"),a.truncado&&i===n.length-1&&(f+='<div class="viz-vacio">(traza cortada a '+(n.length-1)+" pasos — código muy largo o bucle grande)</div>"),p.innerHTML=f}l()}function O(e,t){let a="",s="";const n=[];for(const p of t.split(`
`)){const l=p.trim();l.startsWith("P:")?a=l.slice(2).trim():l.startsWith("+ ")?n.push({txt:l.slice(2).trim(),ok:!0}):l.startsWith("- ")?n.push({txt:l.slice(2).trim(),ok:!1}):l.startsWith("> ")&&(s=l.slice(2).trim())}if(!a||!n.length)return;const i=document.createElement("div");i.className="quiz";const r=document.createElement("div");r.className="quiz-q",r.textContent="🤔 "+a;const c=document.createElement("div");c.className="quiz-ops";const o=document.createElement("div");o.className="quiz-expl",o.hidden=!0,o.textContent=s,n.forEach(p=>{const l=document.createElement("button");l.className="quiz-op",l.type="button",l.textContent=p.txt,l.addEventListener("click",()=>{i.classList.contains("resuelto")||(i.classList.add("resuelto"),Array.from(c.children).forEach((d,u)=>{n[u].ok&&d.classList.add("correcta")}),l.classList.add(p.ok?"elegida-ok":"elegida-mal"),s&&(o.hidden=!1))}),c.appendChild(l)}),i.appendChild(r),i.appendChild(c),i.appendChild(o),e.parentNode.replaceChild(i,e)}document.querySelectorAll(".book pre.astro-code").forEach(e=>{const t=(e.getAttribute("data-language")||"").toLowerCase(),a=e.innerText.replace(/\n+$/,"");if(t==="quiz"||/^\s*P:\s/.test(a)){O(e,a);return}const s=document.createElement("figure");s.className="cw";const n=document.createElement("div");if(n.className="cw-bar",n.innerHTML='<span class="dots"><i></i><i></i><i></i></span><span class="cw-lang">'+(t||"code")+"</span>",e.parentNode.insertBefore(s,e),s.appendChild(n),t==="python"){const i=document.createElement("div");i.className="cw-edit",s.appendChild(i),e.remove();const r=z({doc:a,parent:i,onRun:()=>x(r.state.doc.toString(),o,p)}),c=document.createElement("span");c.className="cw-hint",c.textContent="✎ editable",n.appendChild(c);const o=document.createElement("div");o.className="cw-out",o.setAttribute("role","status"),o.setAttribute("aria-live","polite"),o.innerHTML='<span class="lbl">SALIDA</span>';const p=document.createElement("button");p.className="cw-run",p.type="button",p.textContent="▶ ejecutar",p.addEventListener("click",()=>x(r.state.doc.toString(),o,p)),n.appendChild(p);const l=document.createElement("button");l.className="cw-run cw-viz-btn",l.type="button",l.textContent="👁️ visualizar",l.title="Ver cómo corre el código paso a paso",l.addEventListener("click",()=>F(r.state.doc.toString(),s,l)),n.appendChild(l),s.appendChild(o)}else s.appendChild(e)});(window.requestIdleCallback||(e=>setTimeout(e,1800)))(()=>{C().catch(()=>{})});
