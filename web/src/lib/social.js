// social.js — perfiles públicos, amigos e intercambios asíncronos (sobre la API self-hosted).
import { hayApi, auth, apiGet, apiPost, apiDelete } from './api.js';
import { estado } from './coleccion.js';
import { evaluar, contexto } from './logros.js';
const haySupabase = hayApi;

const REGN = { kanto: 'Kanto', johto: 'Johto', hoenn: 'Hoenn', sinnoh: 'Sinnoh', unova: 'Unova', kalos: 'Kalos' };
const done = (slug, id) => localStorage.getItem(`ej:${slug}:${id}:ok`) === '1';

export function snapshotPublico(temas) {
  const st = estado();
  const c = contexto(temas);
  const logros = evaluar(temas).filter((l) => l.cumplido).map((l) => ({ ico: l.ico, nombre: l.nombre, desc: l.desc }));
  const REGORD = ['kanto', 'johto', 'hoenn', 'sinnoh', 'unova', 'kalos'];
  const porReg = {};
  for (const t of temas) (porReg[t.region] ||= []).push(t);
  const regiones = REGORD.filter((r) => porReg[r]).map((r) => {
    const ts = porReg[r];
    const hechas = ts.filter((t) => t.ejercicios.length && t.ejercicios.every((ex) => done(t.slug, ex.id))).length;
    return { region: r, nombre: REGN[r], hechas, total: ts.length, campeon: hechas === ts.length && ts.length > 0 };
  });
  const medallas = regiones.reduce((a, x) => a + x.hechas, 0);
  const titulos = regiones.filter((x) => x.campeon).map((x) => x.nombre);
  return {
    atrapados: st.atrapados,
    shiny: [...st.shiny],
    conteos: { unicos: st.unicos, total: st.total, shinies: st.shiny.size, ejercicios: c.ejHechos },
    medallas, titulos, regiones, logros,
  };
}

const uid = () => (auth.user() ? auth.user().id : null);

export async function miPerfil() { if (!uid()) return null; return apiGet('/perfil/me'); }
export async function guardarPerfil({ handle, nombre, avatar, publico }) {
  return apiPost('/perfil', { handle, nombre: nombre || '', avatar: avatar || 0, publico: publico || {} });
}
export async function actualizarSnapshot(temas) {
  if (!hayApi || !uid()) return;
  const avatar = Number(localStorage.getItem('col:avatar')) || 0;
  try { await apiPost('/perfil/publico', { publico: snapshotPublico(temas), avatar }); } catch {}
}
export async function guardarDescripcion(desc) { await apiPost('/perfil/descripcion', { desc }); }

export async function perfilPublico(handle) { return apiGet(`/perfil/${encodeURIComponent(handle)}`); }
export async function buscar(q) { return apiGet(`/perfiles?q=${encodeURIComponent(q || '')}`); }

export async function solicitar({ handle, codigo }) { await apiPost('/amigos/solicitar', { handle: handle || null, codigo: codigo || null }); }
export async function responder(id, aceptar) { await apiPost(`/amigos/${id}/responder`, { aceptar }); }
export async function quitar(id) { await apiDelete(`/amigos/${id}`); }
export async function amigos() { return apiGet('/amigos'); }
export async function solicitudes() { return apiGet('/amigos/solicitudes'); }
export async function sonAmigos(otroUserId) { const r = await apiGet(`/amigos/son/${otroUserId}`); return !!(r && r.son); }
export async function misRelaciones() {
  try {
    const data = await apiGet('/amigos/relaciones');
    const m = new Map(); (data || []).forEach((r) => m.set(r.handle, r.estado)); return m;
  } catch { return new Map(); }
}

export async function crearOferta(aUserId, doy, pido) { const r = await apiPost('/ofertas', { aId: aUserId, doy, pido }); return r && r.id; }
export async function responderOferta(id, aceptar) { const r = await apiPost(`/ofertas/${id}/responder`, { aceptar }); return r && r.estado; }
export async function cancelarOferta(id) { await apiDelete(`/ofertas/${id}`); }
export async function ofertas() { return apiGet('/ofertas'); }
export async function pendientes() { try { const r = await apiGet('/social/pendientes'); return (r && r.n) || 0; } catch { return 0; } }
export async function listarPerfiles(limite, offset) { return apiGet(`/perfiles/listar?limite=${limite}&offset=${offset}`); }

export { haySupabase };
