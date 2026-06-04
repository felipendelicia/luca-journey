// nube.js — sincroniza el progreso (localStorage) con Supabase cuando hay sesión.
// Modo HÍBRIDO: sin login, todo sigue en localStorage. Al loguearte:
//   - si tu cuenta YA tiene progreso → se importa ese y se descarta el local.
//   - si la cuenta es NUEVA (vacía) → tu progreso local la siembra.
// Después, cada cambio se sube solo.
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

// borra del localStorage todas las claves de progreso (ej:* y col:*)
function limpiarLocal() {
  const claves = [];
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i);
    if (PREFIJOS.some((p) => k.startsWith(p))) claves.push(k);
  }
  claves.forEach((k) => localStorage.removeItem(k));
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

// ---- al iniciar sesión: la cuenta manda (salvo que sea nueva) ----
async function alLoguear(user) {
  const nube = await bajar(user.id);
  const tieneNube = nube && Object.keys(nube).length > 0;
  if (tieneNube) {
    // cuenta existente: importar su progreso y descartar el local
    limpiarLocal();
    aplicar(nube);
    _ultima = serial(nube);
    location.reload();                       // reflejar el progreso importado
  } else {
    // cuenta nueva: el progreso local pasa a ser el de la cuenta
    const local = snapshot();
    if (Object.keys(local).length) await subir(user.id, local);
    else _ultima = serial(local);
  }
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
