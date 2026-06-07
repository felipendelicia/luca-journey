// social.js — perfiles públicos, amigos e intercambios asíncronos (sobre la API self-hosted).
import { hayApi, auth, apiGet, apiPost, apiDelete } from './api.js';
import { estado, pc } from './coleccion.js';
import { evaluar, contexto } from './logros.js';
import { REGION_IDS, nombreDe } from './regiones.mjs';
const haySupabase = hayApi;

const REGN = Object.fromEntries(REGION_IDS.map((id) => [id, nombreDe(id)]));
const done = (slug, id) => localStorage.getItem(`ej:${slug}:${id}:ok`) === '1';

export function snapshotPublico(temas) {
  const st = estado();
  const c = contexto(temas);
  const logros = evaluar(temas).filter((l) => l.cumplido).map((l) => ({ ico: l.ico, nombre: l.nombre, desc: l.desc }));
  const REGORD = REGION_IDS;
  const porReg = {};
  for (const t of temas) (porReg[t.region] ||= []).push(t);
  // una MEDALLA = el hito 'tema:slug' otorgado (ejercicios completos + proyecto/hito), igual que la Liga y
  // coleccion.sincronizar. Antes acá se contaba solo por ejercicios → sobre-contaba y descuadraba el rango.
  const hitos = (() => { try { return new Set(JSON.parse(localStorage.getItem('col:hitos')) || []); } catch { return new Set(); } })();
  const regiones = REGORD.filter((r) => porReg[r]).map((r) => {
    const ts = porReg[r];
    const hechas = ts.filter((t) => hitos.has('tema:' + t.slug)).length;
    return { region: r, nombre: REGN[r], hechas, total: ts.length, campeon: hechas === ts.length && ts.length > 0 };
  });
  const medallas = regiones.reduce((a, x) => a + x.hechas, 0);
  const titulos = regiones.filter((x) => x.campeon).map((x) => x.nombre);

  // ── campos sociales nuevos (todos viven en localStorage; van en el blob público) ──
  const ls = (k, def) => { try { const v = JSON.parse(localStorage.getItem(k)); return v == null ? def : v; } catch { return def; } };
  const pcArr = pc();
  // instancia "slim" para publicar: incluye la IDENTIDAD (IVs/nat/hab/género/tamaño/alfa) si la tiene,
  // así perfil/intercambio pueden mostrarla (no solo nivel/shiny).
  const slim = (m) => ({ iid: m.iid, id: m.id, nivel: m.nivel, shiny: !!m.shiny, mote: m.mote || '',
    ...(m.ivs ? { ivs: m.ivs, nat: m.nat, hab: m.hab, gen: m.gen } : {}),
    ...(m.tam ? { tam: m.tam } : {}), ...(m.alfa ? { alfa: true } : {}) });
  const porIid = Object.fromEntries(pcArr.map((m) => [m.iid, m]));
  const equipo = (ls('col:equipo', [])).map((iid) => porIid[iid]).filter(Boolean).map(slim);
  const pvpRaw = ls('col:pvp', {});
  const rachaRaw = ls('col:racha', { dias: 0 });

  return {
    atrapados: st.atrapados,
    shiny: [...st.shiny],
    // instancias del PC para el intercambio por INSTANCIA (id/nivel/shiny/mote + identidad por iid)
    pcPub: pcArr.map(slim),
    conteos: { unicos: st.unicos, total: st.total, shinies: st.shiny.size, ejercicios: c.ejHechos },
    medallas, titulos, regiones, logros,
    equipo,
    pvp: { rating: Number(pvpRaw.rating) || 1000, victorias: pvpRaw.victorias || 0, jugados: pvpRaw.jugados || 0 },
    racha: rachaRaw.dias || 0,
    buscando: ls('col:buscando', []),
    ofrezco: ls('col:ofrezco', []),
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
// instancias del PC de un amigo, EN VIVO (no del snapshot público, que puede estar viejo) — para ofertas
export async function pcDeUsuario(userId) { return apiGet(`/usuarios/${encodeURIComponent(userId)}/pc`); }
export async function rankingPvp() { return apiGet('/pvp/ranking'); }   // leaderboard ELO
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
