// nube.js — la NUBE es la única fuente de verdad. Login obligatorio.
//   - Boot: al cargar (logueado) se hidrata el cache (localStorage) desde la nube ANTES de
//     mostrar la app. localStorage es solo un cache descartable: en cada boot la nube manda.
//   - Escrituras: write-through (el watcher sube cada cambio).
//   - Realtime: cambios externos (intercambios) entran en vivo.
//   - Sin sesión: la app no entra (Base muestra la pantalla de login).
import { supa, haySupabase } from './supa.js';

const PREFIJOS = ['ej:', 'col:', 'proy:'];
let _user = null;
// hash de lo último sincronizado. Se persiste para saber, entre cargas de página, si el
// local tiene cambios sin subir (y NO pisarlos con la nube en el boot).
let _ultima = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
let _subiendo = false;
function setUltima(s) { _ultima = s; try { localStorage.setItem('nube:ultima', s); } catch {} }

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
// reemplaza el progreso local por el de la nube. _ultima se toma del CACHE real (post-aplicar),
// no del crudo de la nube → evita la asimetría (claves null) que causaba reloads infinitos.
function aplicarNube(estado) {
  limpiarLocal();
  aplicar(estado);
  setUltima(serial(snapshot()));
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
  else setUltima(serial(estado));
}

// ---- boot: la NUBE manda. Hidrata el cache desde la nube una vez por carga de página. ----
let _booteado = false;
async function boot() {
  if (_booteado || !_user) return;
  _booteado = true;
  const yaHidratado = sessionStorage.getItem('nube:hidratado') === '1';
  const persistida = (() => { try { return localStorage.getItem('nube:ultima') || ''; } catch { return ''; } })();
  const localSerial = serial(snapshot());
  const hayLocal = Object.keys(snapshot()).length > 0;
  const cloud = await bajar(_user.id);
  const hayCloud = cloud && Object.keys(cloud).length > 0;
  const cloudSerial = hayCloud ? serial(cloud) : '';

  if (!hayCloud) {
    // cuenta nueva: el cache local siembra la cuenta
    if (hayLocal) await subir(_user.id, snapshot()); else setUltima(localSerial);
  } else if (hayLocal && localSerial !== persistida && cloudSerial === persistida) {
    // cambios locales SIN subir y la nube no cambió → subirlos (no perder lo local)
    await subir(_user.id, snapshot());
  } else {
    // la nube manda (sin cambios locales pendientes, o conflicto raro → gana la nube)
    aplicarNube(cloud);
    const cambio = localSerial !== serial(snapshot());
    if (cambio && !yaHidratado) {
      sessionStorage.setItem('nube:hidratado', '1');
      location.reload();                       // reflejar lo importado; acotado (no loopea)
      return;
    }
    if (cambio) window.dispatchEvent(new CustomEvent('nube:sincronizado'));  // refrescar la UI
  }
  sessionStorage.setItem('nube:hidratado', '1');
  window.dispatchEvent(new CustomEvent('nube:listo'));
}

// ---- watcher: mientras hay sesión, sube los cambios (debounced) ----
let _t = null;
function vigilar() {
  setInterval(() => {
    if (!_user) return;
    const s = serial(snapshot());
    if (s !== _ultima && !_subiendo) {
      clearTimeout(_t);
      _t = setTimeout(async () => { _subiendo = true; await subir(_user.id, snapshot()); _subiendo = false; }, 600);
    }
  }, 2000);
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
  sessionStorage.removeItem('nube:hidratado');
  sessionStorage.removeItem('nube:fusionado');
  _booteado = false;
  await supa.auth.signOut();
  location.reload();
}

let _inicializado = false;
export function init() {
  if (!haySupabase || _inicializado) return;
  _inicializado = true;
  supa.auth.onAuthStateChange((evento, sesion) => {
    _user = (sesion && sesion.user) || null;
    window.dispatchEvent(new CustomEvent('nube:cambio', { detail: { user: _user } }));
    if (_user) {
      suscribirProgreso(_user.id);     // cambios externos (intercambios) en vivo
      boot();                          // la nube manda: hidratar el cache
    } else {
      sessionStorage.removeItem('nube:hidratado');
      if (_canalProg) { supa.removeChannel(_canalProg); _canalProg = null; }
      window.dispatchEvent(new CustomEvent('nube:sinsesion'));
    }
  });
  vigilar();
}
