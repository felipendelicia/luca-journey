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
  const logros = evaluar(temas).filter((l) => l.cumplido).map((l) => ({ ico: l.ico, nombre: l.nombre }));
  let medallas = 0;
  for (const t of temas) if (t.ejercicios.length && t.ejercicios.every((ex) => done(t.slug, ex.id))) medallas++;
  const titulos = Object.entries(c.reg).filter(([, v]) => v).map(([r]) => REGN[r] || r);
  return {
    atrapados: st.atrapados,
    shiny: [...st.shiny],
    conteos: { unicos: st.unicos, total: st.total, shinies: st.shiny.size, ejercicios: c.ejHechos },
    medallas, titulos, logros,
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
  try { await supa.rpc('actualizar_publico', { p_publico: snapshotPublico(temas) }); } catch {}
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

export { haySupabase };
