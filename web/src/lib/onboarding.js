// onboarding.js — al PRIMER login (sin handle), sugiere un nombre de usuario (saltable) ANTES del tutorial.
// Coordina con el tutorial vía el evento 'onboarding:listo': el tutorial (index) espera a que esto resuelva,
// así nunca se pisan. La sugerencia sale del local-part del email (el backend no guarda el nombre de Google).
import { usuario } from './nube.js';
import { miPerfil, guardarPerfil, normHandle, haySupabase } from './social.js';

let _corrio = false;

function avisarListo() {
  try { localStorage.setItem('onboard:visto', '1'); } catch {}
  try { window.dispatchEvent(new Event('onboarding:listo')); } catch {}
}

function sugerir(u) {
  const base = (u && u.email) ? String(u.email).split('@')[0] : '';
  return normHandle(base) || 'entrenador';
}

async function yaTieneHandle() {
  try { if (localStorage.getItem('liga:nombre')) return true; } catch {}
  try { const p = await miPerfil(); return !!(p && p.handle); } catch { return false; }
}

export async function iniciarOnboarding() {
  if (_corrio) return;
  if (!haySupabase) return;                                   // modo solo-local: no hay handles
  try { if (localStorage.getItem('onboard:visto') === '1') return; } catch {}
  const u = usuario(); if (!u) return;                        // sin sesión todavía → corre al loguear
  _corrio = true;
  if (await yaTieneHandle()) { avisarListo(); return; }       // ya tiene perfil → no molestar (sigue el tutorial)
  abrirModal(sugerir(u));
}

function abrirModal(sug) {
  const ov = document.createElement('div');
  ov.className = 'onb-modal';
  ov.setAttribute('role', 'dialog'); ov.setAttribute('aria-modal', 'true'); ov.setAttribute('aria-label', 'Elegí tu nombre de usuario');
  ov.innerHTML =
    '<div class="onb-card">' +
      '<div class="onb-ico">🎴</div>' +
      '<h2>Elegí tu nombre de usuario</h2>' +
      '<p>Así te encuentran tus amigos para intercambiar y pelear. Podés cambiarlo cuando quieras.</p>' +
      '<div class="onb-row"><span class="onb-at">@</span><input id="onb-input" maxlength="20" autocomplete="off" spellcheck="false" aria-label="Nombre de usuario" /></div>' +
      '<p class="onb-msg" id="onb-msg"></p>' +
      '<div class="onb-acc"><button class="onb-skip" id="onb-skip" type="button">Saltar por ahora</button><button class="onb-save" id="onb-save" type="button">Guardar</button></div>' +
    '</div>';
  document.body.appendChild(ov);
  const inp = ov.querySelector('#onb-input'), msg = ov.querySelector('#onb-msg'), save = ov.querySelector('#onb-save');
  inp.value = sug; setTimeout(() => { try { inp.focus(); inp.select(); } catch {} }, 40);

  const cerrar = () => { ov.remove(); avisarListo(); };
  ov.querySelector('#onb-skip').addEventListener('click', cerrar);
  ov.addEventListener('keydown', (e) => { if (e.key === 'Escape') cerrar(); });
  inp.addEventListener('keydown', (e) => { if (e.key === 'Enter') save.click(); });

  let intento = 0;
  save.addEventListener('click', async () => {
    const handle = normHandle(inp.value);
    if (handle.length < 3) { msg.textContent = '⚠️ Mínimo 3 caracteres (minúsculas, números o _).'; return; }
    save.disabled = true; msg.textContent = 'Creando…';
    const avatar = Number(localStorage.getItem('col:avatar')) || 0;
    try {
      await guardarPerfil({ handle, nombre: handle, avatar, publico: {} });
      try { localStorage.setItem('liga:nombre', handle); } catch {}
      ov.remove(); avisarListo();
    } catch (e) {
      save.disabled = false;
      const m = String((e && e.message) || e).toLowerCase();
      if (/ocupad|exist|taken|duplicate|unico|único|unique|409|ya existe/.test(m) && intento < 3) {
        intento++; const nuevo = (handle + Math.floor(2 + Math.random() * 97)).slice(0, 20);
        inp.value = nuevo; msg.textContent = '⚠️ "@' + handle + '" ya está en uso. Probá con "@' + nuevo + '".';
      } else { msg.textContent = '⚠️ ' + ((e && e.message) || 'No se pudo guardar.'); }
    }
  });
}

if (typeof window !== 'undefined') {
  window.addEventListener('nube:listo', iniciarOnboarding);
  window.addEventListener('nube:cambio', iniciarOnboarding);
  setTimeout(iniciarOnboarding, 1800);   // fallback: si ya estaba logueado al cargar
}
