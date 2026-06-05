// api.js — cliente HTTP de la API self-hosted + sesión por JWT.
// Reemplaza a supa.js. La URL viene de PUBLIC_API_URL (Astro la expone al navegador).
// Si falta, hayApi=false y la app corre en modo solo-localStorage (igual que antes sin Supabase).
const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/$/, '');
export const hayApi = Boolean(BASE);
export { hayApi as haySupabase };   // alias de compatibilidad

const TOKEN_KEY = 'api:token';
const getToken = () => { try { return localStorage.getItem(TOKEN_KEY) || ''; } catch { return ''; } };
const setToken = (t) => { try { t ? localStorage.setItem(TOKEN_KEY, t) : localStorage.removeItem(TOKEN_KEY); } catch {} };

const b64 = (s) => { try { return JSON.parse(atob(s.replace(/-/g, '+').replace(/_/g, '/'))); } catch { return null; } };
const payload = (t) => (t ? b64(t.split('.')[1] || '') : null);
const vigente = (p) => p && (!p.exp || p.exp * 1000 > Date.now());

export function usuarioActual() {
  const p = payload(getToken());
  return vigente(p) ? { id: p.sub, email: p.email } : null;
}

const listeners = new Set();
const emitir = () => { const u = usuarioActual(); listeners.forEach((fn) => fn(u)); };

export const auth = {
  onChange(fn) { listeners.add(fn); return () => listeners.delete(fn); },
  loginGoogle() { window.location.href = `${BASE}/auth/google`; },
  logout() { setToken(''); emitir(); },
  token: getToken,
  user: usuarioActual,
};

// Captura el #token=... del callback OAuth y limpia el hash.
(function capturar() {
  if (typeof location === 'undefined' || !location.hash) return;
  const m = new URLSearchParams(location.hash.slice(1));
  const t = m.get('token');
  if (t) { setToken(t); history.replaceState(null, '', location.pathname + location.search); }
})();

async function req(method, path, body) {
  const headers = { 'Content-Type': 'application/json' };
  const t = getToken(); if (t) headers.Authorization = `Bearer ${t}`;
  const res = await fetch(BASE + path, { method, headers, body: body != null ? JSON.stringify(body) : undefined });
  if (!res.ok) {
    let msg = res.statusText;
    try { const j = await res.json(); msg = j.message || msg; } catch {}
    const e = new Error(Array.isArray(msg) ? msg.join(', ') : msg); e.status = res.status; throw e;
  }
  if (res.status === 204) return null;
  const txt = await res.text(); return txt ? JSON.parse(txt) : null;
}
export const apiGet = (p) => req('GET', p);
export const apiPost = (p, b) => req('POST', p, b);
export const apiPut = (p, b) => req('PUT', p, b);
export const apiDelete = (p) => req('DELETE', p);
