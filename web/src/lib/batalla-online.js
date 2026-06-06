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
// selección + combate
export const elegirEquipo = (iids) => emit('elegirEquipo', iids);
export const mover = (i) => emit('mover', i);
export const cambiar = (idx) => emit('cambiar', idx);
export const usarPocion = (id) => emit('pocion', id);
export const lanzarSuper = () => emit('super');
export const resolverSuper = (calidad) => emit('superResuelto', calidad);
export const rendirse = () => emit('rendirse');

export function desconectarBatalla() { if (socket) { socket.disconnect(); socket = null; } }
export const miUid = () => (auth.user() || {}).id;
export const hayOnline = hayApi;
