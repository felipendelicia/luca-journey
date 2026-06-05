// desafios.js — API de los desafíos de la comunidad (RPCs + lecturas).
import { supa, haySupabase } from './supa.js';

// contador local (sincronizado vía col:) para los logros de crear/resolver desafíos.
const bump = (k) => { try { localStorage.setItem(k, String((Number(localStorage.getItem(k)) || 0) + 1)); } catch {} };

export async function crearDesafio(d) {
  const { data, error } = await supa.rpc('crear_desafio', {
    p_titulo: d.titulo, p_consigna: d.consigna, p_func: d.func, p_starter: d.starter,
    p_casos: d.casos, p_dificultad: d.dificultad, p_region: d.region,
  });
  if (error) throw error;
  bump('col:desafios_creados');
  return data; // id
}
export async function leerDesafio(id) {
  const { data, error } = await supa.from('desafios').select('*').eq('id', id).maybeSingle();
  if (error) throw error;
  return data;
}
export async function listarDesafios({ orden = 'recientes', q = '', region = 'todas', limite = 30, offset = 0 } = {}) {
  const { data, error } = await supa.rpc('listar_desafios', {
    p_orden: orden, p_q: q, p_region: region, p_limite: limite, p_offset: offset,
  });
  if (error) throw error;
  return data || [];
}
export async function registrarResolucion(desafioId, codigo) {
  const { data, error } = await supa.rpc('registrar_resolucion', { p_desafio_id: desafioId, p_codigo: codigo });
  if (error) throw error;
  if (data > 0) bump('col:desafios_resueltos'); // primera vez (premio > 0)
  return data; // balls ganadas (0 si ya estaba)
}

// lista de desafíos creados + resueltos por un usuario (sin código, sin spoilers).
export async function desafiosDeUsuario(userId) {
  const { data, error } = await supa.rpc('desafios_de_usuario', { p_user_id: userId });
  if (error) throw error;
  return data || [];
}

// ranking: top creadores y top solvers de la comunidad.
export async function rankingDesafios() {
  const { data, error } = await supa.rpc('ranking_desafios');
  if (error) throw error;
  return data || [];
}
export async function solucionesDe(desafioId) {
  const { data, error } = await supa.rpc('soluciones_de', { p_desafio_id: desafioId });
  if (error) throw error;
  return data || [];
}
export async function votar(resolucionId, on) {
  const { error } = await supa.rpc('votar', { p_resolucion_id: resolucionId, p_on: on });
  if (error) throw error;
}
export async function statsDesafios(userId) {
  const { data, error } = await supa.rpc('stats_desafios', { p_user_id: userId });
  if (error) throw error;
  return Array.isArray(data) ? data[0] : data; // {resueltos, creados}
}
export async function reportarDesafio(desafioId, motivo) {
  const { error } = await supa.rpc('reportar_desafio', { p_desafio_id: desafioId, p_motivo: motivo || '' });
  if (error) throw error;
}
export async function borrarDesafio(desafioId) {
  const { error } = await supa.rpc('borrar_desafio', { p_desafio_id: desafioId });
  if (error) throw error;
}
export { haySupabase };
