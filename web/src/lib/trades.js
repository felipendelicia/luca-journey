// trades.js — API de intercambios: RPCs + suscripción Realtime + presencia.
import { supa, haySupabase } from './supa.js';

const nombreLocal = () => localStorage.getItem('liga:nombre') || 'Entrenador/a';

export async function crear() {
  const { data, error } = await supa.rpc('crear_intercambio', { mi_nombre: nombreLocal() });
  if (error) throw error;
  return data[0]; // { id, codigo }
}
export async function unirse(codigo) {
  const { data, error } = await supa.rpc('unirse', { p_codigo: codigo.trim().toUpperCase(), mi_nombre: nombreLocal() });
  if (error) throw error;
  return data; // id
}
export async function ponerLote(id, lote) {
  const { error } = await supa.rpc('poner_lote', { p_id: id, p_lote: lote });
  if (error) throw error;
}
export async function confirmar(id) {
  const { data, error } = await supa.rpc('confirmar', { p_id: id });
  if (error) throw error;
  return data; // 'abierta' | 'completada'
}
export async function cancelar(id) {
  const { error } = await supa.rpc('cancelar', { p_id: id });
  if (error) throw error;
}
export async function leerSala(id) {
  const { data, error } = await supa.from('intercambios').select('*').eq('id', id).maybeSingle();
  if (error) throw error;
  return data;
}

// Suscribe a los cambios de la sala (postgres_changes) + presencia del otro.
// onCambio(row) cada vez que cambia la fila; onPresencia(hayOtro) cuando entra/sale.
// Devuelve una función para desuscribir.
export function suscribir(id, miId, { onCambio, onPresencia }) {
  const canal = supa.channel(`sala:${id}`, { config: { presence: { key: miId } } });
  canal.on('postgres_changes', { event: 'UPDATE', schema: 'public', table: 'intercambios', filter: `id=eq.${id}` },
    (payload) => onCambio && onCambio(payload.new));
  canal.on('presence', { event: 'sync' }, () => {
    const estado = canal.presenceState();
    const otros = Object.keys(estado).filter((k) => k !== miId).length;
    onPresencia && onPresencia(otros > 0);
  });
  canal.subscribe((status) => { if (status === 'SUBSCRIBED') canal.track({ at: Date.now() }); });
  return () => supa.removeChannel(canal);
}

export { haySupabase };
