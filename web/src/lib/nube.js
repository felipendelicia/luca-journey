// nube.js — sincroniza el progreso (localStorage) con Supabase cuando hay sesión.
// Modo HÍBRIDO: sin login, todo sigue en localStorage. Al loguearte, FUSIONA tu
// progreso local con el de la nube (no se pierde nada) y mantiene todo al día.
import { supa, haySupabase } from './supa.js';

const PREFIJOS = ['ej:', 'col:'];
let _user = null;
let _ultima = '';        // hash de lo último subido
let _subiendo = false;

// ---- snapshot del progreso en localStorage ----
function snapshot() {
  const o = {};
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (PREFIJOS.some((p) => k.startsWith(p))) o[k] = localStorage.getItem(k);
  }
  return o;
}
function aplicar(o) {
  for (const [k, v] of Object.entries(o)) {
    if (v === null || v === undefined) continue;
    localStorage.setItem(k, v);
  }
}
const serial = (o) => JSON.stringify(Object.keys(o).sort().reduce((a, k) => ((a[k] = o[k]), a), {}));

// ---- fusión local + nube (union-favoring; nada se pierde) ----
const num = (v) => { try { return Number(JSON.parse(v)) || 0; } catch { return 0; } };
const obj = (v) => { try { return JSON.parse(v) || {}; } catch { return {}; } };
const arr = (v) => { try { const a = JSON.parse(v); return Array.isArray(a) ? a : []; } catch { return []; } };
const union = (a, b) => [...new Set([...a, ...b])];

function fusionar(local, nube) {
  const out = { ...nube, ...local };
  const claves = new Set([...Object.keys(local), ...Object.keys(nube)]);
  for (const k of claves) {
    if (k.endsWith(':ok')) out[k] = (local[k] === '1' || nube[k] === '1') ? '1' : (local[k] ?? nube[k]);
  }
  if ('col:balls' in local || 'col:balls' in nube) out['col:balls'] = JSON.stringify(Math.max(num(local['col:balls']), num(nube['col:balls'])));
  if ('col:atrapados' in local || 'col:atrapados' in nube) {
    const a = obj(local['col:atrapados']), b = obj(nube['col:atrapados']), m = { ...b };
    for (const [id, n] of Object.entries(a)) m[id] = Math.max(n, m[id] || 0);
    out['col:atrapados'] = JSON.stringify(m);
  }
  if ('col:shiny' in local || 'col:shiny' in nube) out['col:shiny'] = JSON.stringify(union(arr(local['col:shiny']), arr(nube['col:shiny'])));
  for (const k of ['col:ganados', 'col:hitos']) {
    if (k in local || k in nube) out[k] = JSON.stringify(union(arr(local[k]), arr(nube[k])));
  }
  if (local['col:regalo'] || nube['col:regalo']) out['col:regalo'] = [local['col:regalo'], nube['col:regalo']].filter(Boolean).sort().pop();
  return out;
}

// ---- Supabase I/O ----
async function bajar(userId) {
  const { data, error } = await supa.from('progreso').select('estado').eq('user_id', userId).maybeSingle();
  if (error) { console.warn('[nube] bajar:', error.message); return {}; }
  return (data && data.estado) || {};
}
async function subir(userId, estado) {
  const { error } = await supa.from('progreso').upsert({ user_id: userId, estado }, { onConflict: 'user_id' });
  if (error) console.warn('[nube] subir:', error.message);
  else _ultima = serial(estado);
}

// ---- al iniciar sesión: fusionar + (si hace falta) recargar ----
async function alLoguear(user) {
  const local = snapshot();
  const nube = await bajar(user.id);
  const fusion = fusionar(local, nube);
  const cambioLocal = serial(fusion) !== serial(local);
  const cambioNube = serial(fusion) !== serial(nube);
  if (cambioNube) await subir(user.id, fusion);
  else _ultima = serial(fusion);
  if (cambioLocal) { aplicar(fusion); location.reload(); }   // reflejar lo bajado de la nube
}

// ---- watcher: mientras hay sesión, sube los cambios (debounced) ----
let _t = null;
function vigilar() {
  setInterval(() => {
    if (!_user) return;
    const s = serial(snapshot());
    if (s !== _ultima && !_subiendo) {
      clearTimeout(_t);
      _t = setTimeout(async () => { _subiendo = true; await subir(_user.id, snapshot()); _subiendo = false; }, 1500);
    }
  }, 4000);
  const flush = () => { if (_user && serial(snapshot()) !== _ultima) subir(_user.id, snapshot()); };
  window.addEventListener('pagehide', flush);
  document.addEventListener('visibilitychange', () => { if (document.visibilityState === 'hidden') flush(); });
}

// ---- API pública ----
export function usuario() { return _user; }

export async function loginEmail(email) {
  const destino = window.location.origin + (window.__BASE || '') + '/';
  return supa.auth.signInWithOtp({ email, options: { emailRedirectTo: destino } });
}

export async function logout() {
  sessionStorage.removeItem('nube:fusionado');
  await supa.auth.signOut();
  location.reload();
}

export function init() {
  if (!haySupabase) return;
  let fusionado = sessionStorage.getItem('nube:fusionado') === '1';
  supa.auth.onAuthStateChange((evento, sesion) => {
    _user = (sesion && sesion.user) || null;
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    if (_user && !fusionado) {
      fusionado = true;
      sessionStorage.setItem('nube:fusionado', '1');
      alLoguear(_user);
    } else if (!_user) {
      sessionStorage.removeItem('nube:fusionado');
    }
  });
  vigilar();
}
