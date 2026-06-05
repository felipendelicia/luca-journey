// trades.js — intercambios en vivo: REST + realtime (sala:<id>) + presencia de sala.
import { hayApi, apiGet, apiPost, apiDelete } from './api.js';
import * as rt from './realtime.js';
const haySupabase = hayApi;
const nombreLocal = () => localStorage.getItem('liga:nombre') || 'Entrenador/a';

export async function crear() { return apiPost('/trades', { nombre: nombreLocal() }); }
export async function unirse(codigo) {
  const r = await apiPost('/trades/join', { codigo: codigo.trim().toUpperCase(), nombre: nombreLocal() });
  return r && r.id;
}
export async function ponerLote(id, lote) { await apiPost(`/trades/${id}/lote`, { lote }); }
export async function confirmar(id) { const r = await apiPost(`/trades/${id}/confirm`); return r && r.estado; }
export async function cancelar(id) { await apiDelete(`/trades/${id}`); }
export async function leerSala(id) { return apiGet(`/trades/${id}`); }
export async function coleccionOtro(id) { return apiGet(`/trades/${id}/otro`); }
export async function ponerPedido(id, pedido) { await apiPost(`/trades/${id}/pedido`, { pedido }); }

export function suscribir(id, miId, { onCambio, onPresencia }) {
  rt.unir(`sala:${id}`);
  const off1 = rt.on('sala', (row) => { if (row && row.id === id && onCambio) onCambio(row); });
  const off2 = rt.on('presencia', (p) => {
    if (p && p.topic === `sala:${id}` && onPresencia) onPresencia((p.ids || []).filter((k) => k !== miId).length > 0);
  });
  return () => { rt.salir(`sala:${id}`); off1(); off2(); };
}

export { haySupabase };
