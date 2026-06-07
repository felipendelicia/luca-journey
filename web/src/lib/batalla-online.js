// batalla-online.js — cliente del PvP en vivo (namespace /batalla del gateway NestJS).
// El server es la fuente de verdad: acá solo se mandan acciones y se reciben snapshots de estado.
import { io } from 'socket.io-client';
import { auth, hayApi } from './api.js';

const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/$/, '');
let socket = null;

export function conectarBatalla(nombre) {
  if (!hayApi) return null;
  if (socket && socket.connected) return socket;
  if (!socket) {
    socket = io(BASE + '/batalla', { auth: { token: auth.token(), nombre: nombre || '' }, transports: ['websocket'], autoConnect: true });
  }
  return socket;
}
// registra un handler de un evento server→cliente; devuelve función de baja.
export function onBatalla(ev, fn) { const s = conectarBatalla(); if (s) s.on(ev, fn); return () => { if (socket) socket.off(ev, fn); }; }
const emit = (ev, p) => { const s = conectarBatalla(); if (s) s.emit(ev, p); };

// matchmaking
export const buscar = () => emit('buscar');
export const cancelarCola = () => emit('cancelarCola');
export const invitar = (uid) => emit('invitar', uid);
export const aceptar = (roomId) => emit('aceptar', roomId);
export const crearCodigo = () => emit('crearCodigo');
export const unirseCodigo = (code) => emit('unirseCodigo', code);
// selección
export const elegirEquipo = (iids) => emit('elegirEquipo', iids);
// acción unificada del modelo simultáneo: {tipo, i?, idx?, itemId?, calidad?}
export const elegir = (accion) => emit('elegir', accion);
export const elegirReemplazo = (idx) => emit('elegir', { tipo: 'reemplazo', idx });
// wrappers de conveniencia (construyen la acción)
export const mover = (i) => elegir({ tipo: 'mover', i });
export const cambiar = (idx) => elegir({ tipo: 'cambiar', idx });
export const usarPocion = (itemId) => elegir({ tipo: 'pocion', itemId });
export const lanzarSuper = (calidad) => elegir({ tipo: 'super', calidad });
export const rendirse = () => elegir({ tipo: 'rendirse' });
// aviso al server de que terminé de animar la resolución (sincroniza el arranque de la próxima ronda).
export const ackRonda = () => emit('listoRonda');

export function desconectarBatalla() { if (socket) { socket.disconnect(); socket = null; } }
export const miUid = () => (auth.user() || {}).id;
export const hayOnline = hayApi;
