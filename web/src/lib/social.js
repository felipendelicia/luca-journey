// social.js — perfiles públicos, amigos e intercambios asíncronos (sobre Supabase).
import { supa, haySupabase } from './supa.js';
import { estado } from './coleccion.js';
import { evaluar, contexto } from './logros.js';

const REGN = { kanto: 'Kanto', johto: 'Johto', hoenn: 'Hoenn', sinnoh: 'Sinnoh', unova: 'Unova', kalos: 'Kalos' };
const done = (slug, id) => localStorage.getItem(`ej:${slug}:${id}:ok`) === '1';

// Arma el snapshot público (lo que se muestra en el perfil) desde el progreso local.
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

async function uid() {
  const { data } = await supa.auth.getUser();
  return data && data.user ? data.user.id : null;
}

// ---- perfil propio ----
export async function miPerfil() {
  const id = await uid();
  if (!id) return null;
  const { data } = await supa.from('perfiles').select('*').eq('user_id', id).maybeSingle();
  return data;
}
export async function guardarPerfil({ handle, nombre, avatar, publico }) {
  const { data, error } = await supa.rpc('guardar_perfil', {
    p_handle: handle, p_nombre: nombre || '', p_avatar: avatar || 0, p_publico: publico || {},
  });
  if (error) throw error;
  return Array.isArray(data) ? data[0] : data;
}
// Actualiza solo el snapshot público (no-op si todavía no tenés perfil).
export async function actualizarSnapshot(temas) {
  if (!haySupabase || !(await uid())) return;
  const avatar = Number(localStorage.getItem('col:avatar')) || 0;
  try { await supa.rpc('actualizar_publico', { p_publico: snapshotPublico(temas), p_avatar: avatar }); } catch {}
}
export async function guardarDescripcion(desc) {
  const { error } = await supa.rpc('actualizar_descripcion', { p_desc: desc });
  if (error) throw error;
}

// ---- perfiles públicos / búsqueda ----
export async function perfilPublico(handle) {
  const { data, error } = await supa.rpc('perfil_publico', { p_handle: handle });
  if (error) throw error;
  return Array.isArray(data) ? data[0] : data;
}
export async function buscar(q) {
  const { data, error } = await supa.rpc('buscar_perfiles', { q });
  if (error) throw error;
  return data || [];
}

// ---- amigos ----
export async function solicitar({ handle, codigo }) {
  const { error } = await supa.rpc('solicitar_amistad', { p_handle: handle || null, p_codigo: codigo || null });
  if (error) throw error;
}
export async function responder(id, aceptar) {
  const { error } = await supa.rpc('responder_amistad', { p_id: id, p_aceptar: aceptar });
  if (error) throw error;
}
export async function quitar(id) {
  const { error } = await supa.rpc('quitar_amigo', { p_id: id });
  if (error) throw error;
}
export async function amigos() {
  const { data, error } = await supa.rpc('mis_amigos');
  if (error) throw error;
  return data || [];
}
export async function solicitudes() {
  const { data, error } = await supa.rpc('solicitudes_entrantes');
  if (error) throw error;
  return data || [];
}
export async function sonAmigos(otroUserId) {
  const { data, error } = await supa.rpc('son_amigos', { p_otro: otroUserId });
  if (error) throw error;
  return !!data;
}
// Map(handle del otro -> estado) de todas tus relaciones (aceptada | pendiente).
export async function misRelaciones() {
  const { data, error } = await supa.rpc('mis_relaciones');
  if (error) return new Map();
  const m = new Map();
  (data || []).forEach((r) => m.set(r.handle, r.estado));
  return m;
}

// ---- intercambios asíncronos (ofertas) ----
export async function crearOferta(aUserId, doy, pido) {
  const { data, error } = await supa.rpc('crear_oferta', { p_a_id: aUserId, p_doy: doy, p_pido: pido });
  if (error) throw error;
  return data;
}
export async function responderOferta(id, aceptar) {
  const { data, error } = await supa.rpc('responder_oferta', { p_id: id, p_aceptar: aceptar });
  if (error) throw error;
  return data;
}
export async function cancelarOferta(id) {
  const { error } = await supa.rpc('cancelar_oferta', { p_id: id });
  if (error) throw error;
}
export async function ofertas() {
  const { data, error } = await supa.rpc('mis_ofertas');
  if (error) throw error;
  return data || [];
}
export async function pendientes() {
  const { data, error } = await supa.rpc('social_pendientes');
  if (error) return 0;
  return data || 0;
}
export async function listarPerfiles(limite, offset) {
  const { data, error } = await supa.rpc('listar_perfiles', { p_limite: limite, p_offset: offset });
  if (error) throw error;
  return data || [];
}

export { haySupabase };
