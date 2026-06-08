import { Injectable } from '@nestjs/common';
import { Server, Socket } from 'socket.io';
import { ProgresoService } from '../progreso/progreso.service';
import {
  EstadoCombate, Inst, crearCombate, elegirAccion, snapshot, snapshotPara,
  elegirCPU, jugadorDe, rivalDe, activoDe,
} from './motor';
import learnsets from './data/learnsets.json';
import { premiar, Premios, ratingDe } from './insignias';

// Una sala pasa por: seleccion (cada uno elige 3) → combate (motor) → fin.
interface JugadorSala {
  uid: string; nombre: string; socketId: string | null; equipo: Inst[]; listo: boolean;
}
interface Sala {
  id: string; codigo?: string; fase: 'seleccion' | 'combate' | 'fin';
  jugadores: JugadorSala[]; estado?: EstadoCombate;
  graciaTimer?: ReturnType<typeof setTimeout>; graciaDe?: string;
  rondaTimer?: ReturnType<typeof setTimeout>;   // timer 30s de la ronda simultánea / reemplazo
  // sincronización: tras una resolución, esperamos que AMBOS clientes terminen de animar (ack) antes
  // del próximo paso (ronda/reemplazo). Si no, el próximo turno le gana a la animación → desync.
  ackRonda?: Set<string>; siguiente?: () => void; ackTimer?: ReturnType<typeof setTimeout>;
  selTimer?: ReturnType<typeof setTimeout>;   // TTL: si la sala queda en 'seleccion' sin arrancar, se aborta
}
interface EnCola { uid: string; nombre: string; socketId: string; rating: number; ts: number; }

const ROOM = (id: string) => `bsala:${id}`;
const USER = (uid: string) => `bu:${uid}`;
const GRACIA_MS = 30000;
const RONDA_MS = 30000;     // tiempo por ronda (selección de acción) y por reemplazo
const SEL_TTL_MS = 5 * 60 * 1000;   // una sala en 'seleccion' que no arranca en 5 min se aborta (no fugar memoria)
const COLA_TTL_MS = 5 * 60 * 1000;  // una entrada en la cola más vieja que esto se purga
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
  // emite a CADA jugador su snapshot personalizado (oculta los movs del rival). `extra` = campos extra junto a `snap`.
  private emitSnap(sala: Sala, ev: string, extra: any = {}) {
    if (!sala.estado) return;
    for (const j of sala.jugadores) this.emitUid(j.uid, ev, { ...extra, snap: snapshotPara(sala.estado, j.uid) });
  }
  private emitEstado(sala: Sala) {
    if (!sala.estado) return;
    for (const j of sala.jugadores) this.emitUid(j.uid, 'estado', snapshotPara(sala.estado, j.uid));
  }
  // TTL de selección: si la sala no arranca el combate a tiempo, se aborta (libera memoria de invitaciones/códigos colgados).
  private armarSelTimer(sala: Sala) {
    if (sala.selTimer) clearTimeout(sala.selTimer);
    sala.selTimer = setTimeout(() => { if (this.salas.get(sala.id) === sala && sala.fase === 'seleccion') this.abortar(sala); }, SEL_TTL_MS);
  }

  salaDeUid(uid: string): Sala | undefined { const id = this.porUid.get(uid); return id ? this.salas.get(id) : undefined; }

  // ── matchmaking ───────────────────────────────────────────────
  // cola pública: empareja con el rating ELO más cercano; si no hay nadie, encola.
  async buscar(client: Socket, uid: string, nombre: string) {
    if (this.salaDeUid(uid)) return this.emitSock(client.id, 'error', { msg: 'ya-estas-en-sala' });
    // purga: saco mi entrada vieja + cualquiera caducada (socket muerto sin evento de disconnect, etc.).
    const ahora = Date.now();
    this.cola = this.cola.filter((c) => c.uid !== uid && ahora - c.ts < COLA_TTL_MS);
    let rating = 1000; try { rating = ratingDe(await this.progreso.bajar(uid)); } catch {}
    if (this.cola.length) {
      let best = 0, bestD = Infinity;
      this.cola.forEach((c, i) => { const d = Math.abs((c.rating || 1000) - rating); if (d < bestD) { bestD = d; best = i; } });
      const otro = this.cola.splice(best, 1)[0];
      this.crearSeleccion([{ uid: otro.uid, nombre: otro.nombre, socketId: otro.socketId }, { uid, nombre, socketId: client.id }]);
    } else {
      this.cola.push({ uid, nombre, socketId: client.id, rating, ts: ahora });
      this.emitSock(client.id, 'enCola', { ok: true });
    }
  }
  cancelarCola(uid: string) { this.cola = this.cola.filter((c) => c.uid !== uid); }

  // invitar a un amigo: le llega 'invitacion' a su user-room; acepta con el roomId.
  invitar(client: Socket, uid: string, nombre: string, rivalUid: string) {
    if (this.salaDeUid(uid)) return this.emitSock(client.id, 'error', { msg: 'ya-estas-en-sala' });
    const id = rid();
    const sala: Sala = { id, fase: 'seleccion', jugadores: [{ uid, nombre, socketId: client.id, equipo: [], listo: false }] };
    this.salas.set(id, sala); this.porUid.set(uid, id); this.armarSelTimer(sala);
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
    this.salas.set(id, sala); this.codigos.set(code, id); this.porUid.set(uid, id); this.armarSelTimer(sala);
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
    this.salas.set(id, sala); this.armarSelTimer(sala);
    for (const j of js) { this.porUid.set(j.uid, id); this.server.to(j.socketId).socketsJoin(ROOM(id)); }
    this.anunciarEmparejado(sala);
  }

  private anunciarEmparejado(sala: Sala) {
    for (const j of sala.jugadores) {
      // unir el socket ACTUAL de cada jugador a la sala + avisar por la USER-ROOM (no por el socketId, que puede
      // estar viejo si el socket se reconectó mientras esperaba en la cola → si no, el rival no recibe 'emparejado').
      this.server.in(USER(j.uid)).socketsJoin(ROOM(sala.id));
      const rival = sala.jugadores.find((o) => o.uid !== j.uid);
      this.emitUid(j.uid, 'emparejado', { roomId: sala.id, rival: rival ? { uid: rival.uid, nombre: rival.nombre } : null });
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
    if (new Set(iids.map(String)).size !== iids.length) return null;   // sin Pokémon repetido (anti-exploit)
    const estado = await this.progreso.bajar(uid);
    let pc: any[] = [];
    try { pc = JSON.parse((estado as any)['col:pc'] || '[]'); } catch { pc = []; }
    const porIid = new Map(pc.map((m: any) => [String(m.iid), m]));
    const equipo: Inst[] = [];
    for (const iid of iids) {
      const m = porIid.get(String(iid)); if (!m) return null;
      // anti-trampa: solo movimientos del LEARNSET de esa especie (el cliente sube col:pc; podría meter moves ilegales).
      // Si tras filtrar no queda ninguno (dato raro), va [] y movsDe deriva los legales por nivel.
      const legales = new Set(((learnsets as any)[m.id] || []).map((x: any) => x.m));
      const movs = (Array.isArray(m.movs) ? m.movs.map(Number) : []).filter((mid: number) => legales.has(mid));
      equipo.push({ iid: String(m.iid), id: Number(m.id), nivel: Number(m.nivel) || 1, shiny: !!m.shiny, movs });
    }
    return equipo;
  }

  private arrancar(sala: Sala) {
    if (sala.selTimer) { clearTimeout(sala.selTimer); sala.selTimer = undefined; }
    const primero = sala.jugadores[Math.floor(Math.random() * 2)].uid;
    sala.estado = crearCombate(sala.id, sala.jugadores.map((j) => ({ uid: j.uid, nombre: j.nombre, equipo: j.equipo })), primero);
    sala.fase = 'combate';
    this.emitEstado(sala);   // estado inicial (incluye eventos de entrada); por-destinatario (oculta movs del rival)
    this.nuevaRonda(sala);
  }

  // ── ronda simultánea (server-autoritativo) ─────────────────────
  // arranca una ronda fresca de selección: avisa el deadline y arma el timer de auto-move.
  private nuevaRonda(sala: Sala) {
    if (sala.rondaTimer) { clearTimeout(sala.rondaTimer); sala.rondaTimer = undefined; }
    if (!sala.estado || sala.estado.fase !== 'combate') return;   // fin/reemplazo se manejan aparte
    const deadline = Date.now() + RONDA_MS;
    // `dur` = el cliente arma su timer con su propio reloj (sin depender del reloj del server → el rival no ve mal el timer).
    this.emitSnap(sala, 'ronda', { deadline, dur: RONDA_MS });
    sala.rondaTimer = setTimeout(() => this.timeoutRonda(sala), RONDA_MS);
  }

  // cliente elige una acción de la ronda (mover/cambiar/pocion/super/reemplazo/rendirse).
  elegir(client: Socket, uid: string, accion: any) {
    const sala = this.salaDeUid(uid);
    if (!sala || sala.fase !== 'combate' || !sala.estado) return this.emitSock(client.id, 'error', { msg: 'no-en-combate' });
    const fasePrevia = sala.estado.fase;
    const r = elegirAccion(sala.estado, uid, accion);
    if (r.error) return this.emitSock(client.id, 'error', { msg: r.error });

    // avisar al rival que ya elegí (para bloquear su botón "cambiar"); solo útil en fase combate.
    if (fasePrevia === 'combate') this.emitUid(rivalDe(sala.estado, uid).uid, 'rivalListo', { uid });

    // ¿solo se almacenó la elección (ronda NO resuelta)? avisar "esperando" y salir.
    if (r.listo && r.eventos.length === 0) {
      this.emitSock(client.id, 'esperando', {});
      return;
    }

    // la ronda (o el reemplazo) se RESOLVIÓ → publicar resolución + avanzar.
    this.trasResolucion(sala, r.eventos);
  }

  // publica la resolución de una ronda y decide el siguiente paso (fin / reemplazo / nueva ronda).
  private trasResolucion(sala: Sala, eventos: any[]) {
    const e = sala.estado!;
    if (sala.rondaTimer) { clearTimeout(sala.rondaTimer); sala.rondaTimer = undefined; }
    this.emitSnap(sala, 'resolucion', { eventos });
    // esperar a que AMBOS clientes terminen de animar (ack 'listoRonda') antes del próximo paso → sin desync.
    // INCLUIDO el FIN: así el resultado no tapa la animación del golpe que gana (no más "perdió" instantáneo).
    const fin = e.fase === 'fin';
    const reemplazo = e.fase === 'reemplazo';
    const reemplazan = reemplazo ? [...(e.reemplazan || [])] : [];
    this.esperarAck(sala, () => {
      if (!sala.estado) return;
      if (fin) this.finalizar(sala);
      else if (reemplazo) { this.emitSala(sala.id, 'reemplazo', { uids: reemplazan }); this.armarTimerReemplazo(sala); }
      else this.nuevaRonda(sala);
    });
  }

  // espera el ack de animación de ambos jugadores; fallback a los 12s si alguno no avisa (lag/animación colgada).
  private esperarAck(sala: Sala, siguiente: () => void) {
    sala.ackRonda = new Set();
    sala.siguiente = siguiente;
    if (sala.ackTimer) clearTimeout(sala.ackTimer);
    sala.ackTimer = setTimeout(() => this.dispararSiguiente(sala), 12000);
  }

  // un cliente terminó de animar la resolución (evento 'listoRonda'): cuando avisan los dos, avanzamos.
  ackRonda(uid: string) {
    const sala = this.salaDeUid(uid);
    if (!sala || !sala.ackRonda || !sala.siguiente) return;
    sala.ackRonda.add(uid);
    if (sala.jugadores.every((j) => sala.ackRonda!.has(j.uid))) this.dispararSiguiente(sala);
  }

  private dispararSiguiente(sala: Sala) {
    if (sala.ackTimer) { clearTimeout(sala.ackTimer); sala.ackTimer = undefined; }
    const sig = sala.siguiente;
    sala.siguiente = undefined; sala.ackRonda = undefined;
    if (sig) sig();
  }

  // timeout de la ronda: auto-elige (CPU) por cada uid que no eligió; si acumula 3 timeouts, pierde.
  private timeoutRonda(sala: Sala) {
    const e = sala.estado;
    if (!sala || sala.fase !== 'combate' || !e || e.fase !== 'combate') return;
    const eventos: any[] = [];
    for (const j of e.jugadores) {
      if (e.acciones[j.uid] != null) continue;             // ya eligió en tiempo
      const yo = jugadorDe(e, j.uid);
      const mov = elegirCPU(activoDe(yo), activoDe(rivalDe(e, j.uid)));
      const i = activoDe(yo).movs.findIndex((m) => m.id === mov.id);
      const r = elegirAccion(e, j.uid, { tipo: 'mover', i: i < 0 ? 0 : i });
      e.timeouts[j.uid]++;                                   // motor resetea a 0 a quien sí eligió a tiempo
      if (r.eventos.length) eventos.push(...r.eventos);      // la última auto-elección resuelve la ronda
    }

    // ¿alguien llegó a 3 timeouts? → derrota por inactividad (la ronda ya se resolvió arriba)
    const muerto = e.jugadores.find((j) => (e.timeouts[j.uid] || 0) >= 3);
    if (muerto && (e.fase as string) !== 'fin') {
      e.fase = 'fin'; e.ganador = rivalDe(e, muerto.uid).uid;
      e.eventos.push({ t: 'fin', texto: `${muerto.nombre} perdió por inactividad. ¡Gana ${rivalDe(e, muerto.uid).nombre}!` });
    }
    this.trasResolucion(sala, eventos);
  }

  // timer del reemplazo: si tras 30s alguien no eligió, le metemos el primer banca vivo.
  private armarTimerReemplazo(sala: Sala) {
    if (sala.rondaTimer) { clearTimeout(sala.rondaTimer); sala.rondaTimer = undefined; }
    sala.rondaTimer = setTimeout(() => this.timeoutReemplazo(sala), RONDA_MS);
  }

  private timeoutReemplazo(sala: Sala) {
    const e = sala.estado;
    if (!sala || sala.fase !== 'combate' || !e || e.fase !== 'reemplazo') return;
    const eventos: any[] = [];
    for (const uid of [...(e.reemplazan || [])]) {
      const yo = jugadorDe(e, uid);
      const idx = yo.equipo.findIndex((c, k) => c.hp > 0 && k !== yo.activo);
      if (idx < 0) continue;
      const r = elegirAccion(e, uid, { tipo: 'reemplazo', idx });
      if (r.eventos.length) eventos.push(...r.eventos);
    }
    this.trasResolucion(sala, eventos);
  }

  // ── desconexión / reconexión ───────────────────────────────────
  marcarDesconexion(uid: string) {
    const sala = this.salaDeUid(uid);
    if (!sala) { this.cancelarCola(uid); return; }
    if (sala.fase === 'fin') return;
    const yo = sala.jugadores.find((j) => j.uid === uid); if (yo) yo.socketId = null;
    if (sala.fase === 'seleccion') { this.abortar(sala, uid); return; }
    // pausamos el timer de ronda/reemplazo mientras corre la gracia (la gracia decide el desenlace).
    if (sala.rondaTimer) { clearTimeout(sala.rondaTimer); sala.rondaTimer = undefined; }
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
    if (sala.graciaDe === uid && sala.graciaTimer) {
      clearTimeout(sala.graciaTimer); sala.graciaTimer = undefined; sala.graciaDe = undefined;
      this.emitSala(sala.id, 'rivalVolvio', { uid });
      // re-armamos el timer de la fase que estaba en curso (ronda o reemplazo)
      if (sala.fase === 'combate' && sala.estado) {
        if (sala.estado.fase === 'reemplazo') this.armarTimerReemplazo(sala);
        else if (sala.estado.fase === 'combate') this.nuevaRonda(sala);
      }
    }
    if (sala.estado) this.emitSock(client.id, 'estado', snapshotPara(sala.estado, uid));
  }

  private abortar(sala: Sala, culpaUid?: string) {
    if (sala.selTimer) { clearTimeout(sala.selTimer); sala.selTimer = undefined; }
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
    if (sala.rondaTimer) { clearTimeout(sala.rondaTimer); sala.rondaTimer = undefined; }
    if (sala.ackTimer) { clearTimeout(sala.ackTimer); sala.ackTimer = undefined; }
    if (sala.selTimer) { clearTimeout(sala.selTimer); sala.selTimer = undefined; }
    let premios: Record<string, Premios> = {};
    try { premios = await premiar(this.progreso, sala.estado!, abandonoUid); } catch { premios = {}; }
    for (const j of sala.jugadores) {
      // por user-room (no socketId): si el jugador reconectó con otro socket, igual recibe el resultado.
      this.emitUid(j.uid, 'fin', { ganador: sala.estado?.ganador, premios: premios[j.uid] || null });
      if (premios[j.uid]?.estado) this.emitUid(j.uid, 'progreso', premios[j.uid].estado);   // refresca su nube
      this.porUid.delete(j.uid);
    }
    if (sala.codigo) this.codigos.delete(sala.codigo);
    this.salas.delete(sala.id);
  }
}
