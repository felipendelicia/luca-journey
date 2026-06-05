// desafios.js — API de los desafíos de la comunidad (RPCs + lecturas).
import { supa, haySupabase } from './supa.js';

export async function crearDesafio(d) {
  const { data, error } = await supa.rpc('crear_desafio', {
    p_titulo: d.titulo, p_consigna: d.consigna, p_func: d.func, p_starter: d.starter,
    p_casos: d.casos, p_dificultad: d.dificultad, p_region: d.region,
  });
  if (error) throw error;
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
  return data; // balls ganadas (0 si ya estaba)
}
export { haySupabase };
