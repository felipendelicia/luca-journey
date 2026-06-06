// nube.js — la NUBE (API self-hosted) es la única fuente de verdad. Login obligatorio.
// localStorage es cache descartable; en cada boot la nube manda; escrituras write-through;
// los cambios externos (intercambios) llegan por realtime.
import { hayApi, auth, apiGet, apiPut } from './api.js';
import * as rt from './realtime.js';
import { reconciliarPC } from './coleccion.js';

const haySupabase = hayApi;            // alias interno
const PREFIJOS = ['ej:', 'col:', 'proy:'];
let _user = null;
let _ultima = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
let _subiendo = false;
function setUltima(s) { _ultima = s; try { localStorage.setItem('nube:ultima', s); } catch {} }

function snapshot() {
  const o = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (PREFIJOS.some((p) => k.startsWith(p))) o[k] = localStorage.getItem(k);
  }
  return o;
}
function aplicar(o) {
  for (const [k, v] of Object.entries(o)) { if (v === null || v === undefined) continue; localStorage.setItem(k, v); }
}
const serial = (o) => JSON.stringify(Object.keys(o).sort().reduce((a, k) => ((a[k] = o[k]), a), {}));
function limpiarLocal() {
  const claves = [];
  for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (PREFIJOS.some((p) => k.startsWith(p))) claves.push(k); }
  claves.forEach((k) => localStorage.removeItem(k));
}
function aplicarNube(estado) { limpiarLocal(); aplicar(estado); setUltima(serial(snapshot())); }

async function bajar() {
  try { const r = await apiGet('/progreso'); return (r && r.estado) || {}; }
  catch (e) { console.warn('[nube] bajar:', e.message); return {}; }
}
async function subir(estado) {
  try { await apiPut('/progreso', { estado }); setUltima(serial(estado)); }
  catch (e) { console.warn('[nube] subir:', e.message); }
}

let _booteado = false;
async function boot() {
  if (_booteado || !_user) return;
  _booteado = true;
  const yaHidratado = sessionStorage.getItem('nube:hidratado') === '1';
  const persistida = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
  const localSerial = serial(snapshot());
  const hayLocal = Object.keys(snapshot()).length > 0;
  const cloud = await bajar();
  const hayCloud = cloud && Object.keys(cloud).length > 0;
  const cloudSerial = hayCloud ? serial(cloud) : '';

  if (!hayCloud) {
    if (hayLocal) await subir(snapshot()); else setUltima(localSerial);
  } else if (hayLocal && localSerial !== persistida && cloudSerial === persistida) {
    await subir(snapshot());
  } else {
    aplicarNube(cloud);
    const cambio = localSerial !== serial(snapshot());
    if (cambio && !yaHidratado) { sessionStorage.setItem('nube:hidratado', '1'); location.reload(); return; }
    if (cambio) window.dispatchEvent(new CustomEvent('nube:sincronizado'));
  }
  sessionStorage.setItem('nube:hidratado', '1');
  window.dispatchEvent(new CustomEvent('nube:listo'));
}

let _t = null;
function vigilar() {
  setInterval(() => {
    if (!_user) return;
    const s = serial(snapshot());
    if (s !== _ultima && !_subiendo) {
      clearTimeout(_t);
      _t = setTimeout(async () => { _subiendo = true; await subir(snapshot()); _subiendo = false; }, 600);
    }
  }, 2000);
  const flush = () => { if (_user && serial(snapshot()) !== _ultima) subir(snapshot()); };
  window.addEventListener('pagehide', flush);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); });
}

export function usuario() { return _user; }

export async function refrescarDesdeNube() {
  if (!haySupabase || !_user) return false;
  const nube = await bajar();
  if (nube && Object.keys(nube).length) aplicarNube(nube);
  return true;
}

function toast(msg) {
  try {
    const d = document.createElement('div');
    d.textContent = msg;
    d.style.cssText = 'position:fixed;left:50%;bottom:24px;transform:translateX(-50%);max-width:90%;'
      + 'background:#0c1713;color:#cdebd2;border:1px solid #2b5b41;border-radius:12px;padding:10px 16px;'
      + 'z-index:9999;box-shadow:0 12px 34px rgba(0,0,0,.45);font:600 14px system-ui,sans-serif;text-align:center';
    document.body.appendChild(d);
    setTimeout(() => { d.style.transition = 'opacity .5s'; d.style.opacity = '0'; setTimeout(() => d.remove(), 500); }, 3800);
  } catch {}
}

let _offProg = null;
function suscribirProgreso() {
  if (_offProg) { _offProg(); _offProg = null; }
  _offProg = rt.on('progreso', (estado) => {
    if (!estado) return;
    if (serial(estado) === _ultima) return;
    aplicarNube(estado);
    // un trade (resuelto por el server sobre conteos) cambió mi colección → reconciliar el PC
    // de instancias con los conteos nuevos, sin perder los niveles de lo que ya tenía.
    try {
      reconciliarPC(JSON.parse(estado['col:atrapados'] || '{}'), JSON.parse(estado['col:shiny'] || '[]'));
    } catch {}
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    window.dispatchEvent(new CustomEvent('nube:sincronizado'));
    toast('🔄 Tu colección se actualizó (intercambio)');
  });
}

export async function loginGoogle() { auth.loginGoogle(); return {}; }

export async function logout() {
  sessionStorage.removeItem('nube:hidratado');
  sessionStorage.removeItem('nube:fusionado');
  _booteado = false;
  auth.logout();
  location.reload();
}

let _inicializado = false;
export function init() {
  if (!haySupabase || _inicializado) return;
  _inicializado = true;
  const aplicarSesion = (user) => {
    _user = user || null;
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    if (_user) { rt.conectar(); suscribirProgreso(); boot(); }
    else {
      sessionStorage.removeItem('nube:hidratado');
      if (_offProg) { _offProg(); _offProg = null; }
      window.dispatchEvent(new CustomEvent('nube:sinsesion'));
    }
  };
  auth.onChange(aplicarSesion);
  // Diferir el estado inicial: init() corre ANTES de que Base.astro registre sus
  // listeners de 'nube:cambio'/'nube:sinsesion'. Si emitimos sincrónico, el overlay
  // se queda en el loader (nunca muestra el login). setTimeout(0) los deja registrarse.
  setTimeout(() => aplicarSesion(auth.user()), 0);
  vigilar();
}
