
let _pyReady = null;
async function _getPy(estado){
  if(!_pyReady){
    if(estado){ estado.textContent = "⏳ Cargando Python en el navegador (la primera vez tarda ~10-20s)…"; }
    _pyReady = loadPyodide();
  }
  return _pyReady;
}
async function _correr(codigo, outEl, btn, estado){
  outEl.classList.add("show");
  outEl.innerHTML = '<span class="out-label">SALIDA</span>';
  if(btn){ btn.disabled = true; }
  try{
    const py = await _getPy(estado || outEl);
    if(estado){ estado.textContent = ""; }
    py.setStdout({ batched: (s) => { outEl.appendChild(document.createTextNode(s)); } });
    py.setStderr({ batched: (s) => { const e=document.createElement("span"); e.className="err"; e.textContent=s; outEl.appendChild(e); } });
    py.setStdin({ stdin: () => { const v = window.prompt("input():"); return v === null ? "" : v; } });
    await py.runPythonAsync(codigo);
  }catch(err){
    const e=document.createElement("span"); e.className="err";
    e.textContent = "\n" + (err && err.message ? err.message : err);
    outEl.appendChild(e);
  }finally{
    if(btn){ btn.disabled = false; }
  }
}
document.addEventListener("DOMContentLoaded", function(){
  document.querySelectorAll("figure.code").forEach(function(fig){
    const langEl = fig.querySelector(".code-lang");
    const lang = (langEl ? langEl.textContent : "").trim().toLowerCase();
    if(lang !== "python") return;
    const bar = fig.querySelector(".code-bar");
    const pre = fig.querySelector("pre");
    if(!bar || !pre) return;
    const out = document.createElement("div"); out.className = "code-out";
    fig.appendChild(out);
    const btn = document.createElement("button");
    btn.className = "run-btn"; btn.type = "button"; btn.textContent = "▶ ejecutar";
    btn.addEventListener("click", function(){ _correr(pre.innerText, out, btn); });
    bar.appendChild(btn);
  });
  const pgRun = document.getElementById("pg-run");
  if(pgRun){
    const code = document.getElementById("pg-code");
    const out = document.getElementById("pg-out");
    const estado = document.getElementById("pg-status");
    pgRun.addEventListener("click", function(){ _correr(code.value, out, pgRun, estado); });
    document.querySelectorAll(".pg-ej").forEach(function(b){
      b.addEventListener("click", function(){ code.value = b.getAttribute("data-code"); code.focus(); });
    });
  }
});
