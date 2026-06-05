// desafios.js — API de los desafíos de la comunidad (sobre la API self-hosted).
import { hayApi, apiGet, apiPost, apiDelete } from './api.js';
const haySupabase = hayApi;
const bump = (k) => { try { localStorage.setItem(k, String((Number(localStorage.getItem(k)) || 0) + 1)); } catch {} };

export async function crearDesafio(d) {
  const r = await apiPost('/desafios', {
    titulo: d.titulo, consigna: d.consigna, func: d.func, starter: d.starter,
    casos: d.casos, dificultad: d.dificultad, region: d.region,
  });
  bump('col:desafios_creados');
  return r && r.id;
}
export async function leerDesafio(id) { return apiGet(`/desafios/${id}`); }
export async function listarDesafios({ orden = 'recientes', q = '', region = 'todas', limite = 30, offset = 0 } = {}) {
  const qs = new URLSearchParams({ orden, q, region, limite: String(limite), offset: String(offset) });
  return apiGet(`/desafios?${qs.toString()}`);
}
export async function registrarResolucion(desafioId, codigo) {
  const r = await apiPost(`/desafios/${desafioId}/resolver`, { codigo });
  const balls = (r && r.balls) || 0;
  if (balls > 0) bump('col:desafios_resueltos');
  return balls;
}
export async function desafiosDeUsuario(userId) { return apiGet(`/usuarios/${userId}/desafios`); }
export async function rankingDesafios() { return apiGet('/desafios/ranking'); }
export async function solucionesDe(desafioId) { return apiGet(`/desafios/${desafioId}/soluciones`); }
export async function votar(resolucionId, on) { await apiPost(`/resoluciones/${resolucionId}/votar`, { on }); }
export async function statsDesafios(userId) { return apiGet(`/usuarios/${userId}/stats`); }
export async function reportarDesafio(desafioId, motivo) { await apiPost(`/desafios/${desafioId}/reportar`, { motivo: motivo || '' }); }
export async function borrarDesafio(desafioId) { await apiDelete(`/desafios/${desafioId}`); }
export { haySupabase };
