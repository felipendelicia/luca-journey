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
// reemplaza el progreso local por el de la nube (y marca _ultima para no re-subir lo viejo)
function aplicarNube(estado) {
  limpiarLocal();
  aplicar(estado);
  _ultima = serial(estado);
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
    // la nube manda: importar su progreso y descartar el local
    const cambia = serial(nube) !== serial(snapshot());
    aplicarNube(nube);
    if (cambia) location.reload();           // reflejar lo importado (termina: tras aplicar, local == nube)
  } else {
    // cuenta nueva: el progreso local siembra la cuenta
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

// Baja el progreso de la nube y lo aplica a localStorage (úsalo cuando la nube cambió
// por fuera, ej: un intercambio). Devuelve true si había sesión y se aplicó.
export async function refrescarDesdeNube() {
  if (!haySupabase || !_user) return false;
  const nube = await bajar(_user.id);
  if (nube && Object.keys(nube).length) aplicarNube(nube);
  return true;
}

// Aviso flotante (toast) breve.
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

// Suscribe a cambios EXTERNOS de tu propia fila de progreso (ej: un intercambio async
// hecho por el otro). Los aplica al localStorage sin necesidad de re-loguear.
let _canalProg = null;
function suscribirProgreso(userId) {
  if (_canalProg) { supa.removeChannel(_canalProg); _canalProg = null; }
  _canalProg = supa
    .channel(`prog:${userId}`)
    .on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'progreso', filter: `user_id=eq.${userId}` },
      (payload) => {
        const nuevo = payload.new && payload.new.estado;
        if (!nuevo) return;
        if (serial(nuevo) === _ultima) return;        // eco de mi propia subida → ignorar
        aplicarNube(nuevo);                            // cambio externo (intercambio) → aplicar
        window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
        window.dispatchEvent(new CustomEvent('nube:sincronizado'));
        toast('🔄 Tu colección se actualizó (intercambio)');
      })
    .subscribe();
}

// URL a la que vuelve el usuario tras autenticarse. __BASE ya trae '/' final en prod
// ('/luca-journey/') y en dev ('/'); normalizamos para no generar '//'.
function redirectURL() {
  const base = window.__BASE || '/';
  return window.location.origin + (base.endsWith('/') ? base : base + '/');
}

export async function loginGoogle() {
  return supa.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: redirectURL() } });
}

export async function logout() {
  sessionStorage.removeItem('nube:fusionado');
  await supa.auth.signOut();
  location.reload();
}

export function init() {
  if (!haySupabase) return;
  let cargado = false;   // Opción 2: la nube manda — baja y aplica una vez por carga de página
  supa.auth.onAuthStateChange((evento, sesion) => {
    _user = (sesion && sesion.user) || null;
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    if (_user) {
      if (!cargado) { cargado = true; alLoguear(_user); }
      suscribirProgreso(_user.id);     // escuchar cambios externos (intercambios)
    } else {
      cargado = false;
      if (_canalProg) { supa.removeChannel(_canalProg); _canalProg = null; }
    }
  });
  vigilar();
}
