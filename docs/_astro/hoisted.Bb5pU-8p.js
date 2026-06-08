import{a8 as d,a9 as l,aa as o}from"./hoisted.CUN70WoA.js";const t=e=>document.getElementById(e),n=e=>String(e??"").replace(/[&<>"]/g,a=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"})[a]);async function r(){let e={admin:!1};try{e=await d("/admin/soy")}catch{}if(t("adm-loading").hidden=!0,!e.admin){t("adm-no").hidden=!1;return}t("adm-panel").hidden=!1,await Promise.all([i(),c()])}async function i(){let e=[];try{e=await d("/admin/perfiles")}catch{}t("adm-pn").textContent="("+e.length+")",t("adm-perfiles").innerHTML=e.map(a=>`
        <div class="adm-row${a.baneado?" baneado":""}" data-uid="${n(a.userId)}">
          <div class="adm-info"><b>@${n(a.handle)}</b> <span class="adm-muted">${n(a.nombre)}</span>${a.baneado?' <span class="adm-tag">BANEADO</span>':""}
            ${a.descripcion?`<div class="adm-desc">${n(a.descripcion)}</div>`:""}</div>
          <div class="adm-acc">
            <button class="adm-btn" data-ban="${n(a.userId)}">${a.baneado?"✓ Desbanear":"🚫 Banear"}</button>
            <button class="adm-btn adm-del" data-delp="${n(a.userId)}">🗑️ Borrar perfil</button>
          </div>
        </div>`).join("")||'<p class="adm-muted">Sin perfiles.</p>',t("adm-perfiles").querySelectorAll("[data-ban]").forEach(a=>a.onclick=()=>m(a.dataset.ban,!a.textContent.includes("Desbanear"))),t("adm-perfiles").querySelectorAll("[data-delp]").forEach(a=>a.onclick=()=>p(a.dataset.delp))}async function c(){let e=[];try{e=await d("/admin/desafios")}catch{}t("adm-dn").textContent="("+e.length+")",t("adm-desafios").innerHTML=e.map(a=>`
        <div class="adm-row" data-did="${n(a.id)}">
          <div class="adm-info"><b>${n(a.titulo)}</b> <span class="adm-muted">por @${n(a.autor_handle||"?")}</span>
            ${a.consigna?`<div class="adm-desc">${n(String(a.consigna).slice(0,160))}</div>`:""}</div>
          <div class="adm-acc"><button class="adm-btn adm-del" data-deld="${n(a.id)}">🗑️ Borrar</button></div>
        </div>`).join("")||'<p class="adm-muted">Sin desafíos.</p>',t("adm-desafios").querySelectorAll("[data-deld]").forEach(a=>a.onclick=()=>f(a.dataset.deld))}async function m(e,a){if(!(a&&!confirm("¿Banear a este usuario? Se le borra el perfil y no podrá volver a entrar.")))try{await l("/admin/ban/"+encodeURIComponent(e),{baneado:a}),await i()}catch(s){alert("Error: "+(s.message||s))}}async function p(e){if(confirm("¿Borrar el perfil público de este usuario? (no lo banea)"))try{await o("/admin/perfil/"+encodeURIComponent(e)),await i()}catch(a){alert("Error: "+(a.message||a))}}async function f(e){if(confirm("¿Borrar este desafío?"))try{await o("/admin/desafio/"+encodeURIComponent(e)),await c()}catch(a){alert("Error: "+(a.message||a))}}window.addEventListener("nube:listo",r);setTimeout(r,1500);
