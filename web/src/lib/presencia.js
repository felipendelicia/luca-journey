// presencia.js — presencia GLOBAL: un canal único (app-wide) donde cada usuario logueado
// se anuncia. Sirve para ver qué amigos están online (en cualquier página) y para recibir
// invitaciones a intercambiar estés donde estés. Se inicia desde Base.astro.
import { supa, haySupabase } from './supa.js';

let _canal = null;
let _presentes = new Set();      // user_ids online ahora
let _onInvite = null;
let _miId = null;
const _subs = new Set();         // callbacks que se enteran de cambios de presencia

export function iniciarPresencia(userId, handle, onInvitacion) {
  if (!haySupabase || !userId || _canal) return;
  _miId = userId;
  _onInvite = onInvitacion;
  _canal = supa.channel('presencia-global', { config: { presence: { key: userId } } });
  _canal.on('presence', { event: 'sync' }, () => {
    _presentes = new Set(Object.keys(_canal.presenceState()));
    _subs.forEach((fn) => fn(_presentes));
  });
  _canal.on('broadcast', { event: 'invitacion' }, ({ payload }) => {
    if (payload && payload.to === _miId && _onInvite) _onInvite(payload);
  });
  _canal.subscribe((s) => { if (s === 'SUBSCRIBED') _canal.track({ handle: handle || '', at: Date.now() }); });
}

export function estaOnline(userId) { return _presentes.has(userId); }
export function presentes() { return _presentes; }

// Suscribirse a cambios de presencia. Llama fn(set) al toque y en cada sync. Devuelve baja.
export function onPresencia(fn) {
  _subs.add(fn);
  fn(_presentes);
  return () => _subs.delete(fn);
}

// Mandar una invitación de intercambio a un amigo (le llega esté en la página que esté).
export function invitar(toId, codigo, deHandle) {
  if (_canal) _canal.send({ type: 'broadcast', event: 'invitacion', payload: { to: toId, codigo, de: deHandle } });
}

export function detenerPresencia() {
  if (_canal) { supa.removeChannel(_canal); _canal = null; }
  _presentes = new Set();
}

export { haySupabase };
