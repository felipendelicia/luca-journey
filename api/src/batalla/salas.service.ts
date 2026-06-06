import { Injectable } from '@nestjs/common';
import { Server, Socket } from 'socket.io';
import { ProgresoService } from '../progreso/progreso.service';
import {
  EstadoCombate, Inst, crearCombate, aplicarAccion, snapshot,
} from './motor';
import { premiar, Premios, ratingDe } from './insignias';

// Una sala pasa por: seleccion (cada uno elige 3) → combate (motor) → fin.
interface JugadorSala {
  uid: string; nombre: string; socketId: string | null; equipo: Inst[]; listo: boolean;
}
interface Sala {
  id: string; codigo?: string; fase: 'seleccion' | 'combate' | 'fin';
  jugadores: JugadorSala[]; estado?: EstadoCombate;
  graciaTimer?: ReturnType<typeof setTimeout>; graciaDe?: string;
}
interface EnCola { uid: string; nombre: string; socketId: string; rating: number; }

const ROOM = (id: string) => `bsala:${id}`;
const USER = (uid: string) => `bu:${uid}`;
const GRACIA_MS = 30000;
const rid = () => Math.random().toString(36).slice(2, 10);
const code6 = () => Math.random().toString(36).slice(2, 6).toUpperCase() + Math.floor(10 + Math.random() * 90);

@Injectable()
export class SalasService {
  server!: Server;                                   // lo setea el gateway en afterInit
  private salas = new Map<string, Sala>();
  private cola: EnCola[] = [];
  private codigos = new Map<string, string>();       // code → roomId (sala en selección, falta rival)
  private porUid = new Map<string, string>();        // uid → roomId (su sala activa)

  constructor(private progreso: ProgresoService) {}

  private emitSala(id: string, ev: string, payload: any) { this.server.to(ROOM(id)).emit(ev, payload); }
  private emitUid(uid: string, ev: string, payload: any) { this.server.to(USER(uid)).emit(ev, payload); }
  private emitSock(socketId: string | null, ev: string, payload: any) { if (socketId) this.server.to(socketId).emit(ev, payload); }

  salaDeUid(uid: string): Sala | undefined { const id = this.porUid.get(uid); return id ? this.salas.get(id) : undefined; }

  // ── matchmaking ───────────────────────────────────────────────
  // cola pública: empareja con el rating ELO más cercano; si no hay nadie, encola.
  async buscar(client: Socket, uid: string, nombre: string) {
    if (this.salaDeUid(uid)) return this.emitSock(client.id, 'error', { msg: 'ya-estas-en-sala' });
    this.cola = this.cola.filter((c) => c.uid !== uid);
    let rating = 1000; try { rating = ratingDe(await this.progreso.bajar(uid)); } catch {}
    if (this.cola.length) {
      let best = 0, bestD = Infinity;
      this.cola.forEach((c, i) => { const d = Math.abs((c.rating || 1000) - rating); if (d < bestD) { bestD = d; best = i; } });
      const otro = this.cola.splice(best, 1)[0];
      this.crearSeleccion([{ uid: otro.uid, nombre: otro.nombre, socketId: otro.socketId }, { uid, nombre, socketId: client.id }]);
    } else {
      this.cola.push({ uid, nombre, socketId: client.id, rating });
      this.emitSock(client.id, 'enCola', { ok: true });
    }
  }
  cancelarCola(uid: string) { this.cola = this.cola.filter((c) => c.uid !== uid); }

  // invitar a un amigo: le llega 'invitacion' a su user-room; acepta con el roomId.
  invitar(client: Socket, uid: string, nombre: string, rivalUid: string) {
    if (this.salaDeUid(uid)) return this.emitSock(client.id, 'error', { msg: 'ya-estas-en-sala' });
    const id = rid();
    const sala: Sala = { id, fase: 'seleccion', jugadores: [{ uid, nombre, socketId: client.id, equipo: [], listo: false }] };
    this.salas.set(id, sala); this.porUid.set(uid, id);
    client.join(ROOM(id));
    this.emitUid(rivalUid, 'invitacion', { roomId: id, de: nombre, deUid: uid });
    this.emitSock(client.id, 'invitado', { roomId: id });
  }

  aceptar(client: Socket, uid: string, nombre: string, roomId: string) {
    const sala = this.salas.get(roomId);
    if (!sala || sala.fase !== 'seleccion' || sala.jugadores.length >= 2) return this.emitSock(client.id, 'error', { msg: 'sala-no-disponible' });
    sala.jugadores.push({ uid, nombre, socketId: client.id, equipo: [], listo: false });
    this.porUid.set(uid, roomId); client.join(ROOM(roomId));
    this.anunciarEmparejado(sala);
  }

  // código privado: host crea (queda esperando); el rival se une con el código.
  crearCodigo(client: Socket, uid: string, nombre: string) {
    if (this.salaDeUid(uid)) return this.emitSock(client.id, 'error', { msg: 'ya-estas-en-sala' });
    const id = rid(); const code = code6();
    const sala: Sala = { id, codigo: code, fase: 'seleccion', jugadores: [{ uid, nombre, socketId: client.id, equipo: [], listo: false }] };
    this.salas.set(id, sala); this.codigos.set(code, id); this.porUid.set(uid, id);
    client.join(ROOM(id));
    this.emitSock(client.id, 'codigoCreado', { roomId: id, codigo: code });
  }

  unirseCodigo(client: Socket, uid: string, nombre: string, code: string) {
    const id = this.codigos.get((code || '').toUpperCase().trim());
    const sala = id ? this.salas.get(id) : undefined;
    if (!sala || sala.jugadores.length >= 2) return this.emitSock(client.id, 'error', { msg: 'codigo-invalido' });
    sala.jugadores.push({ uid, nombre, socketId: client.id, equipo: [], listo: false });
    this.codigos.delete(sala.codigo!); sala.codigo = undefined;
    this.porUid.set(uid, id!); client.join(ROOM(id!));
    this.anunciarEmparejado(sala);
  }

  private crearSeleccion(js: { uid: string; nombre: string; socketId: string }[]) {
    const id = rid();
    const sala: Sala = { id, fase: 'seleccion', jugadores: js.map((j) => ({ ...j, equipo: [], listo: false })) };
    this.salas.set(id, sala);
    for (const j of js) { this.porUid.set(j.uid, id); this.server.to(j.socketId).socketsJoin(ROOM(id)); }
    this.anunciarEmparejado(sala);
  }

  private anunciarEmparejado(sala: Sala) {
    for (const j of sala.jugadores) {
      const rival = sala.jugadores.find((o) => o.uid !== j.uid);
      this.emitSock(j.socketId, 'emparejado', { roomId: sala.id, rival: rival ? { uid: rival.uid, nombre: rival.nombre } : null });
    }
  }

  // ── selección de equipo (anti-trampa contra la DB) ─────────────
  async elegirEquipo(client: Socket, uid: string, iids: string[]) {
    const sala = this.salaDeUid(uid);
    if (!sala || sala.fase !== 'seleccion') return this.emitSock(client.id, 'error', { msg: 'no-en-seleccion' });
    const yo = sala.jugadores.find((j) => j.uid === uid); if (!yo) return;
    const equipo = await this.validarEquipo(uid, iids);
    if (!equipo) return this.emitSock(client.id, 'error', { msg: 'equipo-invalido' });
    yo.equipo = equipo; yo.listo = true;
    this.emitSala(sala.id, 'seleccion', { listos: sala.jugadores.map((j) => ({ uid: j.uid, listo: j.listo })) });
    if (sala.jugadores.length === 2 && sala.jugadores.every((j) => j.listo)) this.arrancar(sala);
  }

  // valida que el uid REALMENTE tiene esas instancias (carga col:pc de su progreso en DB).
  private async validarEquipo(uid: string, iids: string[]): Promise<Inst[] | null> {
    if (!Array.isArray(iids) || iids.length < 1 || iids.length > 3) return null;
    const estado = await this.progreso.bajar(uid);
    let pc: any[] = [];
    try { pc = JSON.parse((estado as any)['col:pc'] || '[]'); } catch { pc = []; }
    const porIid = new Map(pc.map((m: any) => [String(m.iid), m]));
    const equipo: Inst[] = [];
    for (const iid of iids) {
      const m = porIid.get(String(iid)); if (!m) return null;
      equipo.push({ iid: String(m.iid), id: Number(m.id), nivel: Number(m.nivel) || 1, shiny: !!m.shiny, movs: Array.isArray(m.movs) ? m.movs.map(Number) : [] });
    }
    return equipo;
  }

  private arrancar(sala: Sala) {
    const primero = sala.jugadores[Math.floor(Math.random() * 2)].uid;
    sala.estado = crearCombate(sala.id, sala.jugadores.map((j) => ({ uid: j.uid, nombre: j.nombre, equipo: j.equipo })), primero);
    sala.fase = 'combate';
    this.emitSala(sala.id, 'estado', snapshot(sala.estado));
    this.emitSala(sala.id, 'tuTurno', { uid: sala.estado.turno });
  }

  // ── acciones de combate (server-autoritativo) ──────────────────
  accion(client: Socket, uid: string, accion: any) {
    const sala = this.salaDeUid(uid);
    if (!sala || sala.fase !== 'combate' || !sala.estado) return this.emitSock(client.id, 'error', { msg: 'no-en-combate' });
    const r = aplicarAccion(sala.estado, uid, accion);
    if (r.error) return this.emitSock(client.id, 'error', { msg: r.error });
    this.emitSala(sala.id, 'estado', snapshot(sala.estado));
    if (sala.estado.fase === 'super') {
      this.emitUid(sala.estado.superDe!, 'retoSuper', { roomId: sala.id });
      return;
    }
    if (sala.estado.fase === 'fin') return void this.finalizar(sala);
    this.emitSala(sala.id, 'tuTurno', { uid: sala.estado.turno });
  }

  // ── desconexión / reconexión ───────────────────────────────────
  marcarDesconexion(uid: string) {
    const sala = this.salaDeUid(uid);
    if (!sala) { this.cancelarCola(uid); return; }
    if (sala.fase === 'fin') return;
    const yo = sala.jugadores.find((j) => j.uid === uid); if (yo) yo.socketId = null;
    if (sala.fase === 'seleccion') { this.abortar(sala, uid); return; }
    sala.graciaDe = uid;
    this.emitSala(sala.id, 'rivalDesconectado', { uid, graciaSeg: GRACIA_MS / 1000 });
    sala.graciaTimer = setTimeout(() => {
      const otro = sala.jugadores.find((j) => j.uid !== uid);
      if (sala.estado && otro) { sala.estado.fase = 'fin'; sala.estado.ganador = otro.uid; }
      this.finalizar(sala, uid);
    }, GRACIA_MS);
  }

  reconectar(client: Socket, uid: string) {
    const sala = this.salaDeUid(uid); if (!sala) return;
    const yo = sala.jugadores.find((j) => j.uid === uid); if (!yo) return;
    yo.socketId = client.id; client.join(ROOM(sala.id));
    if (sala.graciaDe === uid && sala.graciaTimer) { clearTimeout(sala.graciaTimer); sala.graciaTimer = undefined; sala.graciaDe = undefined; this.emitSala(sala.id, 'rivalVolvio', { uid }); }
    if (sala.estado) this.emitSock(client.id, 'estado', snapshot(sala.estado));
  }

  private abortar(sala: Sala, culpaUid?: string) {
    this.emitSala(sala.id, 'abortado', { motivo: 'rival-salio' });
    for (const j of sala.jugadores) this.porUid.delete(j.uid);
    if (sala.codigo) this.codigos.delete(sala.codigo);
    this.salas.delete(sala.id);
  }

  // fin: declara ganador, reparte premios (insignias.ts), persiste, limpia.
  private async finalizar(sala: Sala, abandonoUid?: string) {
    if (sala.fase === 'fin') return;
    sala.fase = 'fin';
    if (sala.graciaTimer) { clearTimeout(sala.graciaTimer); sala.graciaTimer = undefined; }
    let premios: Record<string, Premios> = {};
    try { premios = await premiar(this.progreso, sala.estado!, abandonoUid); } catch { premios = {}; }
    for (const j of sala.jugadores) {
      this.emitSock(j.socketId, 'fin', { ganador: sala.estado?.ganador, premios: premios[j.uid] || null });
      if (premios[j.uid]?.estado) this.emitUid(j.uid, 'progreso', premios[j.uid].estado);   // refresca su nube
      this.porUid.delete(j.uid);
    }
    if (sala.codigo) this.codigos.delete(sala.codigo);
    this.salas.delete(sala.id);
  }
}
