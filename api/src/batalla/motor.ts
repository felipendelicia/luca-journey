// motor.ts — PvP server-autoritativo: la MÁQUINA DE ESTADO de la sala (turnos, acciones, súper en
// pausa, fin). Las REGLAS (tipos, daño, estados, IA) viven en el motor COMPARTIDO ./combate-core
// (réplica de web/src/lib/combate-core.ts, copiada por scripts/sync-batalla-data.mjs). Determinista
// si se le pasa un `rng` fijo (los tests lo aprovechan).
// Los .json son copias de web/src/data (Docker buildea solo ./api).
import tiposData from './data/tipos.json';
import movimientos from './data/movimientos.json';
import learnsets from './data/learnsets.json';
import pokemon from './data/pokemon.json';
import estadisticas from './data/estadisticas.json';
import {
  combatiente as coreCombatiente,
  esEstado, calcularDano, aplicarEstado, danoSuper, etiquetaEfec, tiraCritico,
  acierta, puedeActuar, aplicarAilment, tickEstado,
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
};
export const combatiente = (inst: Inst): Combatiente => coreCombatiente(inst, DATOS);

// ───────────────────────── máquina de estado de la sala ─────────────────────────
export type Fase = 'seleccion' | 'combate' | 'super' | 'fin';
export interface JugadorEstado {
  uid: string; nombre: string; equipo: Combatiente[]; activo: number; super: number; listo: boolean;
}
export interface Evento { t: string; uid?: string; texto: string; [k: string]: any; }
export interface EstadoCombate {
  roomId: string; jugadores: [JugadorEstado, JugadorEstado];
  turno: string; fase: Fase; ganador?: string; superDe?: string; eventos: Evento[]; turnoN: number;
}
export interface AccionRes { estado: EstadoCombate; eventos: Evento[]; error?: string; }

export const SUPER_MAX = 100;        // barra llena
const SUPER_GANANCIA = 25;           // por acción de ataque
const POCION_CURA: Record<string, number> = { pocion: 30, superpocion: 70, pocionmax: 9999 };
const CURA_ESTADO: Record<string, EstadoAlt | 'todos'> = { antidoto: 'veneno', antiquemar: 'quemadura', antiparalisis: 'paralisis', despertar: 'sueno', antihielo: 'congelado', curatotal: 'todos' };
const REVIVE: Record<string, number> = { revivir: 0.5 };

const jugadorDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid === uid);
const rivalDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid !== uid)!;
const vivos = (j: JugadorEstado) => j.equipo.filter((c) => c.hp > 0).length;
const activoDe = (j: JugadorEstado) => j.equipo[j.activo];

// crea el combate a partir de los equipos elegidos (instancias). fase = combate.
export function crearCombate(roomId: string, jugadores: { uid: string; nombre: string; equipo: Inst[] }[], primero?: string): EstadoCombate {
  const js = jugadores.map((j) => ({
    uid: j.uid, nombre: j.nombre, equipo: j.equipo.slice(0, 3).map((inst) => combatiente(inst)), activo: 0, super: 0, listo: true,
  })) as [JugadorEstado, JugadorEstado];
  return {
    roomId, jugadores: js, turno: primero || js[0].uid, fase: 'combate', eventos: [], turnoN: 1,
  };
}

// avanza al siguiente Pokémon vivo del jugador (tras un debilitamiento). true si encontró uno.
function autoSwitch(j: JugadorEstado): boolean {
  if (activoDe(j).hp > 0) return true;
  const i = j.equipo.findIndex((c) => c.hp > 0);
  if (i < 0) return false;
  j.activo = i; return true;
}

function pasarTurno(e: EstadoCombate, deUid: string) {
  e.turno = rivalDe(e, deUid).uid;
  e.turnoN += 1;
}

export function chequearFin(e: EstadoCombate): string | null {
  for (const j of e.jugadores) if (vivos(j) === 0) return rivalDe(e, j.uid).uid;
  return null;
}

// aplica una acción de `uid`. Valida turno/propiedad. Devuelve el nuevo estado + eventos.
export function aplicarAccion(
  e: EstadoCombate, uid: string,
  accion: { tipo: 'mover' | 'cambiar' | 'pocion' | 'super' | 'superResuelto' | 'rendirse'; i?: number; idx?: number; itemId?: string; calidad?: number },
  rng: Rng = Math.random,
): AccionRes {
  const eventos: Evento[] = [];
  const push = (t: string, texto: string, extra: any = {}) => { const ev = { t, uid, texto, ...extra }; eventos.push(ev); e.eventos.push(ev); };
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

  // súper en pausa: solo el dueño del reto puede resolverlo
  if (e.fase === 'super') {
    if (accion.tipo !== 'superResuelto') return err('esperando-super');
    if (e.superDe !== uid) return err('no-es-tu-super');
    const cal = Math.max(0, Math.min(1, accion.calidad ?? 0));
    const atk = activoDe(yo), def = activoDe(rival);
    const r = danoSuper(atk, def, cal, rng);
    def.hp = Math.max(0, def.hp - r.dmg);
    yo.super = 0; e.fase = 'combate'; e.superDe = undefined;
    push('super', `⚡ ¡SÚPER de ${atk.nombre}! ${r.mov.nombre} causa ${r.dmg} de daño.`, { dmg: r.dmg });
    if (postGolpe(e, rival, push)) return { estado: e, eventos };
    const tk = tickEstado(atk); if (tk.dmg) push('dot', tk.texto, { dmg: tk.dmg });
    if (postGolpe(e, yo, push)) return { estado: e, eventos };
    pasarTurno(e, uid);
    return { estado: e, eventos };
  }

  // fuera de turno
  if (e.turno !== uid) return err('no-es-tu-turno');
  const atk = activoDe(yo), def = activoDe(rival);

  switch (accion.tipo) {
    case 'mover': {
      const mov = atk.movs[accion.i ?? 0]; if (!mov) return err('mov-invalido');
      const pa = puedeActuar(atk, rng);                       // sueño/cong/para/confusión
      if (pa.texto) push('estado', pa.texto, pa.autogolpe ? { autogolpe: pa.autogolpe } : {});
      if (pa.actua) {
        if (!acierta(mov, rng)) {
          push('fallo', `${atk.nombre} usó ${mov.nombre}, ¡pero falló!`, { mov: mov.id });
        } else if (esEstado(mov)) {
          push('estado', `${atk.nombre} usó ${mov.nombre}. ` + aplicarEstado(mov, atk, def), { mov: mov.id });
          const ta = aplicarAilment(mov, atk, def, rng); if (ta) push('ailment', ta);
        } else {
          const crit = tiraCritico(rng);
          const r = calcularDano(atk, mov, def, rng, crit);
          def.hp = Math.max(0, def.hp - r.dmg);
          const ef = etiquetaEfec(r.efec);
          const msg = r.efec === 0
            ? `${atk.nombre} usó ${mov.nombre}… ¡pero no afecta a ${def.nombre}!`
            : `${atk.nombre} usó ${mov.nombre}: ${r.dmg} de daño.${r.crit ? ' ¡Golpe crítico!' : ''}${ef ? ' ' + ef : ''}`;
          push('mover', msg, { dmg: r.dmg, efec: r.efec, crit: r.crit, mov: mov.id });
          if (def.hp > 0) { const ta = aplicarAilment(mov, atk, def, rng); if (ta) push('ailment', ta); }
        }
        yo.super = Math.min(SUPER_MAX, yo.super + SUPER_GANANCIA);
      }
      if (postGolpe(e, rival, push)) return { estado: e, eventos };   // ¿cayó el rival?
      const tk = tickEstado(atk); if (tk.dmg) push('dot', tk.texto, { dmg: tk.dmg });   // veneno/quemadura del que actuó
      if (postGolpe(e, yo, push)) return { estado: e, eventos };      // ¿cayó el actor (DOT/confusión)?
      pasarTurno(e, uid);
      return { estado: e, eventos };
    }
    case 'cambiar': {
      const idx = accion.idx ?? -1;
      if (idx < 0 || idx >= yo.equipo.length || idx === yo.activo) return err('cambio-invalido');
      if (yo.equipo[idx].hp <= 0) return err('debilitado');
      yo.activo = idx;
      push('cambiar', `${yo.nombre} cambió a ${activoDe(yo).nombre}.`, { idx });
      pasarTurno(e, uid);
      return { estado: e, eventos };
    }
    case 'pocion': {
      const itemId = accion.itemId || 'pocion';
      if (POCION_CURA[itemId] != null) {                       // poción de HP
        if (atk.hp >= atk.hpMax) return err('hp-lleno');
        const c = Math.min(atk.hpMax - atk.hp, POCION_CURA[itemId]); atk.hp += c;
        push('pocion', `${yo.nombre} curó a ${atk.nombre} (+${c} HP).`, { cura: c });
      } else if (CURA_ESTADO[itemId]) {                        // cura de estado
        const cura = CURA_ESTADO[itemId];
        const aplica = cura === 'todos' ? !!atk.estado : atk.estado === cura;
        if (!aplica) return err('no-aplica');
        atk.estado = null; atk.estadoT = 0;
        push('pocion', `${yo.nombre} curó el estado de ${atk.nombre}.`);
      } else if (REVIVE[itemId] != null) {                     // revivir un debilitado
        const ko = yo.equipo.find((c) => c.hp <= 0);
        if (!ko) return err('sin-debilitado');
        ko.hp = Math.max(1, Math.round(ko.hpMax * REVIVE[itemId])); ko.estado = null; ko.estadoT = 0;
        push('pocion', `¡${ko.nombre} revivió con ${ko.hp} HP!`);
      } else return err('item-invalido');
      pasarTurno(e, uid);
      return { estado: e, eventos };
    }
    case 'super': {
      if (yo.super < SUPER_MAX) return err('super-no-listo');
      e.fase = 'super'; e.superDe = uid;
      push('retoSuper', `⚡ ${yo.nombre} desató el SÚPER: resolvé tu reto de código.`);
      return { estado: e, eventos };
    }
    default:
      return err('accion-desconocida');
  }
}

// tras un golpe: si el activo del jugador cayó, auto-switch o fin. Devuelve true si el combate terminó.
function postGolpe(e: EstadoCombate, rival: JugadorEstado, push: (t: string, texto: string, extra?: any) => void): boolean {
  if (activoDe(rival).hp > 0) return false;
  push('debilitado', `¡${activoDe(rival).nombre} se debilitó!`);
  if (!autoSwitch(rival)) {
    e.fase = 'fin'; e.ganador = rivalDe(e, rival.uid).uid;
    push('fin', `¡Gana ${rivalDe(e, rival.uid).nombre}!`);
    return true;
  }
  push('entra', `${rival.nombre} envió a ${activoDe(rival).nombre}.`);
  return false;
}

// snapshot público (sin lógica interna): lo que se emite a ambos clientes.
export function snapshot(e: EstadoCombate) {
  return {
    roomId: e.roomId, fase: e.fase, turno: e.turno, turnoN: e.turnoN, ganador: e.ganador, superDe: e.superDe,
    jugadores: e.jugadores.map((j) => ({
      uid: j.uid, nombre: j.nombre, activo: j.activo, super: j.super,
      equipo: j.equipo.map((c) => ({ iid: c.iid, id: c.id, nombre: c.nombre, nivel: c.nivel, shiny: c.shiny, tipos: c.tipos, hp: c.hp, hpMax: c.hpMax, movs: c.movs, estado: c.estado })),
    })),
    eventos: e.eventos.slice(-12),
  };
}
