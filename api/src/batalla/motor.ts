// motor.ts — PvP server-autoritativo: la MÁQUINA DE ESTADO de la sala (modelo SIMULTÁNEO). Ambos
// jugadores ELIGEN una acción por ronda; cuando los dos eligieron se RESUELVE la ronda en orden
// (cambios → ítems → ataques por prioridad/velocidad → DOT → fin/reemplazo). Las REGLAS (tipos,
// daño, estados, IA, prioridad/orden) viven en el motor COMPARTIDO ./combate-core (réplica de
// web/src/lib/combate-core.ts, copiada por scripts/sync-batalla-data.mjs). Determinista si se le
// pasa un `rng` fijo (los tests lo aprovechan).
// Los .json son copias de web/src/data (Docker buildea solo ./api).
import tiposData from './data/tipos.json';
import movimientos from './data/movimientos.json';
import learnsets from './data/learnsets.json';
import pokemon from './data/pokemon.json';
import estadisticas from './data/estadisticas.json';
import habilidades from './data/habilidades.json';
import {
  combatiente as coreCombatiente,
  esEstado, calcularDano, aplicarEstado, danoSuper, etiquetaEfec, tiraCritico, sinPP, FORCEJEO,
  acierta, puedeActuar, aplicarAilment, tickEstado, habAlEntrar, habAlContacto,
  prioridadMov, ordenLanzadores,
} from './combate-core';
import type { Rng, EstadoAlt, Mov, Inst, Combatiente, DatosCombate } from './combate-core';

// reglas + tipos re-exportados (los usan salas.service y los tests)
export {
  efectividad, etiquetaEfec, hpMax, esEstado, calcularDano, aplicarEstado, danoSuper, elegirCPU,
  ESTADOS, acierta, puedeActuar, aplicarAilment, tickEstado,
} from './combate-core';
export type { Rng, EstadoAlt, Mov, Inst, Combatiente } from './combate-core';

// data del server inyectada al core
const DATOS: DatosCombate = {
  nombres: Object.fromEntries((pokemon as any[]).map((p) => [p.id, p.nombre])),
  tipos: tiposData as any, learnsets: learnsets as any, movimientos: movimientos as any,
  estadisticas: estadisticas as any,
  habilidades: habilidades as any,
};
export const combatiente = (inst: Inst): Combatiente => coreCombatiente(inst, DATOS);

// ───────────────────────── máquina de estado de la sala ─────────────────────────
export type Fase = 'seleccion' | 'combate' | 'reemplazo' | 'fin';
// acción que un jugador elige en una ronda. súper ocupa un slot de ataque (calidad ya resuelta).
export type Accion = { tipo: 'mover' | 'cambiar' | 'pocion' | 'super' | 'reemplazo' | 'rendirse'; i?: number; idx?: number; itemId?: string; calidad?: number };
export interface JugadorEstado {
  uid: string; nombre: string; equipo: Combatiente[]; activo: number; super: number; listo: boolean;
}
export interface Evento { t: string; uid?: string; texto: string; [k: string]: any; }
export interface EstadoCombate {
  roomId: string; jugadores: [JugadorEstado, JugadorEstado];
  fase: Fase; ganador?: string; eventos: Evento[]; turnoN: number;
  acciones: Record<string, Accion | null>;   // elección pendiente de cada uid (null = todavía no eligió)
  timeouts: Record<string, number>;           // ms acumulados de espera por uid (el gateway lo usa)
  reemplazan?: string[];                       // uids que deben elegir reemplazo tras un KO
  // compat snapshot (no usados por la lógica simultánea)
  turno?: string; superDe?: string;
}
export interface AccionRes { estado: EstadoCombate; eventos: Evento[]; listo?: boolean; error?: string; }

export const SUPER_MAX = 100;        // barra llena
const SUPER_GANANCIA = 25;           // por acción de ataque
const POCION_CURA: Record<string, number> = { pocion: 30, superpocion: 70, pocionmax: 9999 };
const CURA_ESTADO: Record<string, EstadoAlt | 'todos'> = { antidoto: 'veneno', antiquemar: 'quemadura', antiparalisis: 'paralisis', despertar: 'sueno', antihielo: 'congelado', curatotal: 'todos' };
const REVIVE: Record<string, number> = { revivir: 0.5 };

// helpers de acceso (exportados: el gateway los usa para armar la acción CPU del timeout)
export const jugadorDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid === uid)!;
export const rivalDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid !== uid)!;
export const vivos = (j: JugadorEstado) => j.equipo.filter((c) => c.hp > 0).length;
export const activoDe = (j: JugadorEstado) => j.equipo[j.activo];

// crea el combate a partir de los equipos elegidos (instancias). fase = combate.
export function crearCombate(roomId: string, jugadores: { uid: string; nombre: string; equipo: Inst[] }[], primero?: string): EstadoCombate {
  const js = jugadores.map((j) => ({
    uid: j.uid, nombre: j.nombre, equipo: j.equipo.slice(0, 3).map((inst) => combatiente(inst)), activo: 0, super: 0, listo: true,
  })) as [JugadorEstado, JugadorEstado];
  const eventos: Evento[] = [];
  // habilidad AL ENTRAR (Intimidación): ambos activos entran a la vez → cada uno intimida al otro
  for (const [a, b] of [[js[0], js[1]], [js[1], js[0]]] as [JugadorEstado, JugadorEstado][]) {
    const te = habAlEntrar(activoDe(a), activoDe(b));
    if (te) eventos.push({ t: 'habilidad', uid: a.uid, texto: te });
  }
  return {
    roomId, jugadores: js, fase: 'combate', eventos, turnoN: 1,
    acciones: { [js[0].uid]: null, [js[1].uid]: null },
    timeouts: { [js[0].uid]: 0, [js[1].uid]: 0 },
  };
}

export function chequearFin(e: EstadoCombate): string | null {
  for (const j of e.jugadores) if (vivos(j) === 0) return rivalDe(e, j.uid).uid;
  return null;
}

type Push = (t: string, texto: string, extra?: any) => void;

// ejecuta el ATAQUE de `yo` contra `rival` (move o súper). Reúsa la lógica de daño/estado/contacto
// del modelo viejo. Cada evento lleva uid = yo.uid. Si el activo de `yo` ya cayó (golpe previo del
// rival más rápido en la misma ronda), no actúa.
function ejecutarAtaque(e: EstadoCombate, yo: JugadorEstado, rival: JugadorEstado, acc: Accion, push: Push, rng: Rng): void {
  const atk = activoDe(yo), def = activoDe(rival);
  if (atk.hp <= 0) return;   // cayó al golpe del rival más rápido en esta ronda

  if (acc.tipo === 'super') {
    const cal = Math.max(0, Math.min(1, acc.calidad ?? 0));
    const r = danoSuper(atk, def, cal, rng);
    def.hp = Math.max(0, def.hp - r.dmg);
    yo.super = 0;
    push('super', `⚡ ¡SÚPER de ${atk.nombre}! ${r.mov.nombre} causa ${r.dmg} de daño.`, { uid: yo.uid, dmg: r.dmg, objetivo: rival.uid, hpRest: def.hp, hpMax: def.hpMax });
    return;
  }

  // move normal (idéntico al case 'mover' del modelo viejo)
  let mov = atk.movs[acc.i ?? 0]; if (!mov) return;
  if ((mov.pp ?? 1) <= 0) {
    if (sinPP(atk)) mov = { ...FORCEJEO, pp: 1, ppMax: 1 };   // sin PP en ninguno → Forcejeo
    else { push('fallo', `${atk.nombre} no tiene PP en ese movimiento.`, { uid: yo.uid }); return; }
  }
  const pa = puedeActuar(atk, rng);                       // sueño/cong/para/confusión
  if (pa.texto) push('estado', pa.texto, { uid: yo.uid, ...(pa.autogolpe ? { autogolpe: pa.autogolpe } : {}) });
  if (pa.actua) {
    if (mov.id && (mov.pp ?? 0) > 0) mov.pp!--;           // consume PP (Forcejeo id 0 no gasta)
    if (!acierta(mov, rng, atk)) {
      push('fallo', `${atk.nombre} usó ${mov.nombre}, ¡pero falló!`, { uid: yo.uid, mov: mov.id });
    } else if (esEstado(mov)) {
      push('estado', `${atk.nombre} usó ${mov.nombre}. ` + aplicarEstado(mov, atk, def), { uid: yo.uid, mov: mov.id });
      const ta = aplicarAilment(mov, atk, def, rng); if (ta) push('ailment', ta, { uid: yo.uid });
    } else {
      const crit = tiraCritico(rng);
      const r = calcularDano(atk, mov, def, rng, crit);
      def.hp = Math.max(0, def.hp - r.dmg);
      const ef = etiquetaEfec(r.efec);
      const msg = r.efec === 0
        ? `${atk.nombre} usó ${mov.nombre}… ¡pero no afecta a ${def.nombre}!`
        : `${atk.nombre} usó ${mov.nombre}: ${r.dmg} de daño.${r.crit ? ' ¡Golpe crítico!' : ''}${ef ? ' ' + ef : ''}`;
      push('mover', msg, { uid: yo.uid, dmg: r.dmg, efec: r.efec, crit: r.crit, mov: mov.id, objetivo: rival.uid, hpRest: def.hp, hpMax: def.hpMax });
      if (def.hp > 0) { const ta = aplicarAilment(mov, atk, def, rng); if (ta) push('ailment', ta, { uid: yo.uid }); }
      if (def.hp > 0) { const tc = habAlContacto(def, atk, mov, rng); if (tc) push('habilidad', tc, { uid: yo.uid }); }
    }
    yo.super = Math.min(SUPER_MAX, yo.super + SUPER_GANANCIA);
  }
  // ¿cayó el rival a este golpe? aviso de debilitamiento. uid = el dueño del que CAYÓ (rival), para que la
  // animación de muerte salga en el sprite correcto (antes iba el del atacante → caía el Pokémon equivocado).
  if (activoDe(rival).hp <= 0) push('debilitado', `¡${activoDe(rival).nombre} se debilitó!`, { uid: rival.uid });
}

// valida + almacena la acción de `uid`. Si ambos eligieron, resuelve la ronda.
export function elegirAccion(
  e: EstadoCombate, uid: string, accion: Accion, rng: Rng = Math.random,
): AccionRes {
  const eventos: Evento[] = [];
  const push: Push = (t, texto, extra = {}) => { const ev = { t, uid, texto, ...extra }; eventos.push(ev); e.eventos.push(ev); };
  const err = (msg: string): AccionRes => ({ estado: e, eventos: [], error: msg });

  if (e.fase === 'fin') return err('combate-terminado');
  const yo = jugadorDe(e, uid); if (!yo) return err('jugador-desconocido');
  const rival = rivalDe(e, uid);

  // rendirse: válido siempre, gana el rival
  if (accion.tipo === 'rendirse') {
    e.fase = 'fin'; e.ganador = rival.uid;
    push('rendirse', `${yo.nombre} se rindió. ¡Gana ${rival.nombre}!`);
    return { estado: e, eventos };
  }

  // fase REEMPLAZO: solo aceptamos de quien debe reemplazar, una elección de banca viva
  if (e.fase === 'reemplazo') {
    if (!e.reemplazan?.includes(uid)) return err('no-debes-reemplazar');
    if (accion.tipo !== 'reemplazo') return err('esperando-reemplazo');
    const idx = accion.idx ?? -1;
    if (idx < 0 || idx >= yo.equipo.length || idx === yo.activo) return err('reemplazo-invalido');
    if (yo.equipo[idx].hp <= 0) return err('debilitado');
    yo.activo = idx;
    push('entra', `${yo.nombre} envió a ${activoDe(yo).nombre}.`, { uid: yo.uid, idx, hpRest: activoDe(yo).hp, hpMax: activoDe(yo).hpMax });
    { const te = habAlEntrar(activoDe(yo), activoDe(rival)); if (te) push('habilidad', te); }
    e.reemplazan = e.reemplazan.filter((u) => u !== uid);
    if (e.reemplazan.length === 0) {
      e.fase = 'combate';
      e.acciones[e.jugadores[0].uid] = null; e.acciones[e.jugadores[1].uid] = null;
      e.turnoN += 1;
    }
    return { estado: e, eventos };
  }

  if (e.fase !== 'combate') return err('no-en-combate');

  // ── validación de la acción (sin mutar estado todavía) ──
  const atk = activoDe(yo);
  switch (accion.tipo) {
    case 'mover': {
      if (atk.hp <= 0) return err('debilitado');
      const mov = atk.movs[accion.i ?? 0]; if (!mov) return err('mov-invalido');
      break;
    }
    case 'super': {
      if (yo.super < SUPER_MAX) return err('super-no-listo');
      if (atk.hp <= 0) return err('debilitado');
      break;
    }
    case 'cambiar': {
      const idx = accion.idx ?? -1;
      if (idx < 0 || idx >= yo.equipo.length || idx === yo.activo) return err('cambio-invalido');
      if (yo.equipo[idx].hp <= 0) return err('debilitado');
      break;
    }
    case 'pocion':
      // PvP NO permite items: el server no valida inventario, así que aceptarlos habilitaba curas/revivir
      // infinitos. La UI online tampoco los ofrece. (En práctica/CPU sí hay items, pero eso corre en el cliente.)
      return err('items-no-permitidos');
    default:
      return err('accion-desconocida');
  }

  // almacenar la elección (re-pick permitido mientras la ronda no se resolvió)
  e.acciones[uid] = accion; e.timeouts[uid] = 0;
  if (e.acciones[e.jugadores[0].uid] && e.acciones[e.jugadores[1].uid]) {
    return resolverRonda(e, rng);
  }
  return { estado: e, eventos: [], listo: true };
}

// resuelve la ronda cuando AMBOS eligieron: cambios → ítems → ataques (prioridad/velocidad) → DOT.
function resolverRonda(e: EstadoCombate, rng: Rng): AccionRes {
  const eventos: Evento[] = [];
  const push: Push = (t, texto, extra = {}) => { const ev = { t, texto, ...extra }; eventos.push(ev); e.eventos.push(ev); };

  const accDe = (j: JugadorEstado) => e.acciones[j.uid]!;

  // 1) CAMBIOS de ambos (se aplican antes de los ataques)
  for (const j of e.jugadores) {
    const acc = accDe(j);
    if (acc.tipo !== 'cambiar') continue;
    const idx = acc.idx!;
    j.activo = idx;
    push('cambiar', `${j.nombre} cambió a ${activoDe(j).nombre}.`, { uid: j.uid, idx, hpRest: activoDe(j).hp, hpMax: activoDe(j).hpMax });
    const te = habAlEntrar(activoDe(j), activoDe(rivalDe(e, j.uid))); if (te) push('habilidad', te, { uid: j.uid });
  }

  // 2) POCIONES/ÍTEMS de ambos
  for (const j of e.jugadores) {
    const acc = accDe(j);
    if (acc.tipo !== 'pocion') continue;
    const itemId = acc.itemId || 'pocion';
    const obj = activoDe(j);
    if (POCION_CURA[itemId] != null) {
      const c = Math.min(obj.hpMax - obj.hp, POCION_CURA[itemId]); obj.hp += c;
      push('pocion', `${j.nombre} curó a ${obj.nombre} (+${c} HP).`, { uid: j.uid, cura: c });
    } else if (CURA_ESTADO[itemId]) {
      obj.estado = null; obj.estadoT = 0;
      push('pocion', `${j.nombre} curó el estado de ${obj.nombre}.`, { uid: j.uid });
    } else if (REVIVE[itemId] != null) {
      const ko = j.equipo.find((c) => c.hp <= 0);
      if (ko) { ko.hp = Math.max(1, Math.round(ko.hpMax * REVIVE[itemId])); ko.estado = null; ko.estadoT = 0;
        push('pocion', `¡${ko.nombre} revivió con ${ko.hp} HP!`, { uid: j.uid }); }
    }
  }

  // 3) ATAQUES (mover/super) en orden de prioridad → velocidad → desempate rng
  const atacantes = e.jugadores.filter((j) => { const a = accDe(j); return a.tipo === 'mover' || a.tipo === 'super'; });
  const prioDe = (j: JugadorEstado) => {
    const a = accDe(j);
    if (a.tipo === 'super') return 0;
    return prioridadMov(activoDe(j).movs[a.i ?? 0] || FORCEJEO);
  };
  if (atacantes.length === 2) {
    atacantes.sort((x, y) => ordenLanzadores(
      { prio: prioDe(x), spe: activoDe(x).spe },
      { prio: prioDe(y), spe: activoDe(y).spe },
      rng,
    ));
  }
  for (const j of atacantes) ejecutarAtaque(e, j, rivalDe(e, j.uid), accDe(j), push, rng);

  // 4) DOT (veneno/quemadura) de cada activo que siga en pie
  for (const j of e.jugadores) {
    const a = activoDe(j);
    if (a.hp <= 0) continue;
    const tk = tickEstado(a);
    if (tk.dmg) {
      push('dot', tk.texto, { uid: j.uid, dmg: tk.dmg, objetivo: j.uid, hpRest: a.hp, hpMax: a.hpMax });
      if (a.hp <= 0) push('debilitado', `¡${a.nombre} se debilitó!`, { uid: j.uid });
    }
  }

  // 5) ¿se terminó el combate?
  const fin = chequearFin(e);
  if (fin) {
    e.fase = 'fin'; e.ganador = fin;
    push('fin', `¡Gana ${jugadorDe(e, fin).nombre}!`);
    return { estado: e, eventos };
  }

  // 6) ¿alguien tiene el activo debilitado pero con banca viva? → fase reemplazo
  e.reemplazan = e.jugadores.filter((j) => activoDe(j).hp <= 0 && vivos(j) > 0).map((j) => j.uid);
  if (e.reemplazan.length) {
    e.fase = 'reemplazo';   // NO limpiamos acciones ni avanzamos: el gateway pide el reemplazo
    return { estado: e, eventos };
  }

  // 7) ronda limpia → siguiente ronda
  e.acciones[e.jugadores[0].uid] = null; e.acciones[e.jugadores[1].uid] = null;
  e.turnoN += 1;
  return { estado: e, eventos };
}

// snapshot público (sin lógica interna): lo que se emite a ambos clientes. NO revela la acción
// elegida por el rival (anti-info-leak): solo expone QUIÉN ya eligió.
export function snapshot(e: EstadoCombate) {
  const [a, b] = e.jugadores;
  return {
    roomId: e.roomId, fase: e.fase, turnoN: e.turnoN, ganador: e.ganador,
    reemplazan: e.reemplazan,
    elegidos: { [a.uid]: !!e.acciones[a.uid], [b.uid]: !!e.acciones[b.uid] },
    jugadores: e.jugadores.map((j) => ({
      uid: j.uid, nombre: j.nombre, activo: j.activo, super: j.super,
      equipo: j.equipo.map((c) => ({ iid: c.iid, id: c.id, nombre: c.nombre, nivel: c.nivel, shiny: c.shiny, tipos: c.tipos, hp: c.hp, hpMax: c.hpMax, movs: c.movs, estado: c.estado })),
    })),
    eventos: e.eventos.slice(-12),
  };
}

// snapshot por DESTINATARIO: oculta los movimientos del RIVAL (anti info-leak — el cliente solo usa los movs
// propios; el equipo/movs completos del rival no se deben revelar). El jugador `paraUid` ve su equipo intacto.
export function snapshotPara(e: EstadoCombate, paraUid: string): any {
  const s: any = snapshot(e);
  s.jugadores = s.jugadores.map((j: any) =>
    j.uid === paraUid ? j : { ...j, equipo: j.equipo.map((c: any) => ({ ...c, movs: undefined })) },
  );
  return s;
}

// compat: salas.service todavía llama aplicarAccion (Task 3 lo migra a elegirAccion). Wrapper fino.
export function aplicarAccion(e: EstadoCombate, uid: string, accion: Accion, rng: Rng = Math.random): AccionRes {
  return elegirAccion(e, uid, accion, rng);
}
