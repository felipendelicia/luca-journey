// presencia.js — presencia GLOBAL (canal 'presencia-global'): quién está online + recibir
// invitaciones a intercambiar. Se inicia desde Base.astro.
import { hayApi } from './api.js';
import * as rt from './realtime.js';
const haySupabase = hayApi;

let _iniciado = false;
let _presentes = new Set();
let _onInvite = null;
let _miId = null;
const _subs = new Set();

export function iniciarPresencia(userId, handle, onInvitacion) {
  if (!hayApi || !userId || _iniciado) return;
  _iniciado = true; _miId = userId; _onInvite = onInvitacion;
  rt.unir('presencia-global');
  rt.on('presencia', (p) => {
    if (!p || p.topic !== 'presencia-global') return;
    _presentes = new Set(p.ids || []);
    _subs.forEach((fn) => fn(_presentes));
  });
  rt.on('broadcast', (payload) => { if (payload && payload.to === _miId && _onInvite) _onInvite(payload); });
}

export function estaOnline(userId) { return _presentes.has(userId); }
export function presentes() { return _presentes; }

export function onPresencia(fn) { _subs.add(fn); fn(_presentes); return () => _subs.delete(fn); }

export function invitar(toId, codigo, deHandle) {
  rt.broadcast('presencia-global', { to: toId, codigo, de: deHandle });
}

export function detenerPresencia() { rt.salir('presencia-global'); _presentes = new Set(); _iniciado = false; }

export { haySupabase };
