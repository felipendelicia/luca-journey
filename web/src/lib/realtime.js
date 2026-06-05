// realtime.js — cliente WebSocket (socket.io) de la API. Topics: `progreso:<uid>` (auto),
// `sala:<id>` y `presencia-global` (join/leave). Eventos del server: 'progreso','sala',
// 'presencia','broadcast'.
import { io } from 'socket.io-client';
import { auth, hayApi } from './api.js';

const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/$/, '');
let socket = null;

export function conectar() {
  if (!hayApi) return null;
  if (socket && socket.connected) return socket;
  if (!socket) {
    socket = io(BASE, { auth: { token: auth.token() }, transports: ['websocket'], autoConnect: true });
  }
  return socket;
}
export function unir(topic) { const s = conectar(); s && s.emit('join', topic); }
export function salir(topic) { socket && socket.emit('leave', topic); }
// registra un handler de un evento del server; devuelve función de baja.
export function on(evento, fn) { const s = conectar(); s && s.on(evento, fn); return () => socket && socket.off(evento, fn); }
export function broadcast(topic, payload) { const s = conectar(); s && s.emit('broadcast', { topic, payload }); }
export function desconectar() { if (socket) { socket.disconnect(); socket = null; } }
