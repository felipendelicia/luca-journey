// motor.ts — motor de combate PvP, server-autoritativo. Port en TS de web/src/lib/batalla.js +
// tipos.js, MÁS la máquina de estado de la sala (turnos, acciones, súper en pausa, fin).
// Puro (sin DOM, sin red): el gateway lo usa para resolver cada acción. Determinista si se le pasa
// un `rng` fijo (los tests lo aprovechan).
//
// Los .json son copias de web/src/data (Docker buildea solo ./api). Regenerar con
// `node scripts/sync-batalla-data.mjs` cuando cambien los datos del front.
import tiposData from './data/tipos.json';
import movimientos from './data/movimientos.json';
import learnsets from './data/learnsets.json';
import pokemon from './data/pokemon.json';

// ───────────────────────── tipos / efectividad ─────────────────────────
const NOM: Record<number, string> = Object.fromEntries((pokemon as any[]).map((p) => [p.id, p.nombre]));
export const tiposDe = (id: number): string[] => (tiposData as any)[String(id)] || ['Normal'];

const TABLA: Record<string, { x2: string[]; x05: string[]; x0: string[] }> = {
  Normal: { x2: [], x05: ['Roca', 'Acero'], x0: ['Fantasma'] },
  Fuego: { x2: ['Planta', 'Hielo', 'Bicho', 'Acero'], x05: ['Fuego', 'Agua', 'Roca', 'Dragón'], x0: [] },
  Agua: { x2: ['Fuego', 'Tierra', 'Roca'], x05: ['Agua', 'Planta', 'Dragón'], x0: [] },
  Planta: { x2: ['Agua', 'Tierra', 'Roca'], x05: ['Fuego', 'Planta', 'Veneno', 'Volador', 'Bicho', 'Dragón', 'Acero'], x0: [] },
  Eléctrico: { x2: ['Agua', 'Volador'], x05: ['Eléctrico', 'Planta', 'Dragón'], x0: ['Tierra'] },
  Hielo: { x2: ['Planta', 'Tierra', 'Volador', 'Dragón'], x05: ['Fuego', 'Agua', 'Hielo', 'Acero'], x0: [] },
  Lucha: { x2: ['Normal', 'Hielo', 'Roca', 'Siniestro', 'Acero'], x05: ['Veneno', 'Volador', 'Psíquico', 'Bicho', 'Hada'], x0: ['Fantasma'] },
  Veneno: { x2: ['Planta', 'Hada'], x05: ['Veneno', 'Tierra', 'Roca', 'Fantasma'], x0: ['Acero'] },
  Tierra: { x2: ['Fuego', 'Eléctrico', 'Veneno', 'Roca', 'Acero'], x05: ['Planta', 'Bicho'], x0: ['Volador'] },
  Volador: { x2: ['Planta', 'Lucha', 'Bicho'], x05: ['Eléctrico', 'Roca', 'Acero'], x0: [] },
  Psíquico: { x2: ['Lucha', 'Veneno'], x05: ['Psíquico', 'Acero'], x0: ['Siniestro'] },
  Bicho: { x2: ['Planta', 'Psíquico', 'Siniestro'], x05: ['Fuego', 'Lucha', 'Veneno', 'Volador', 'Fantasma', 'Acero', 'Hada'], x0: [] },
  Roca: { x2: ['Fuego', 'Hielo', 'Volador', 'Bicho'], x05: ['Lucha', 'Tierra', 'Acero'], x0: [] },
  Fantasma: { x2: ['Psíquico', 'Fantasma'], x05: ['Siniestro'], x0: ['Normal'] },
  Dragón: { x2: ['Dragón'], x05: ['Acero'], x0: ['Hada'] },
  Siniestro: { x2: ['Psíquico', 'Fantasma'], x05: ['Lucha', 'Siniestro', 'Hada'], x0: [] },
  Acero: { x2: ['Hielo', 'Roca', 'Hada'], x05: ['Fuego', 'Agua', 'Eléctrico', 'Acero'], x0: [] },
  Hada: { x2: ['Lucha', 'Dragón', 'Siniestro'], x05: ['Fuego', 'Veneno', 'Acero'], x0: [] },
};
function unoContra(atk: string, def: string): number {
  const t = TABLA[atk]; if (!t) return 1;
  if (t.x0.includes(def)) return 0;
  if (t.x2.includes(def)) return 2;
  if (t.x05.includes(def)) return 0.5;
  return 1;
}
export function efectividad(tipoAtaque: string, tiposDefensor: string[]): number {
  return (tiposDefensor || []).reduce((m, d) => m * unoContra(tipoAtaque, d), 1);
}
export function etiquetaEfec(mult: number): string {
  if (mult === 0) return 'No afecta…';
  if (mult >= 2) return '¡Es muy eficaz!';
  if (mult <= 0.5) return 'No es muy eficaz…';
  return '';
}

// ───────────────────────── combatientes ─────────────────────────
export type Rng = () => number;
export interface Mov { id: number; nombre: string; tipo: string; poder?: number; categoria?: string; desc?: string; }
export interface Inst { iid: string; id: number; nivel: number; shiny?: boolean; mote?: string; movs?: number[]; }
export interface Combatiente {
  iid: string; id: number; nombre: string; nivel: number; shiny: boolean; tipos: string[];
  movs: Mov[]; hpMax: number; hp: number; atkMod: number; defMod: number;
}

const FORCEJEO: Mov = { id: 0, nombre: 'Forcejeo', tipo: 'Normal', poder: 40 };
export const hpMax = (nivel: number): number => 40 + nivel * 5;

function movsDe(inst: Inst): Mov[] {
  const ls: { m: number; n: number }[] = (learnsets as any)[inst.id] || [];
  let ids = (inst.movs || []).filter(Boolean);
  if (!ids.length) {
    ids = ls.filter((x) => x.n <= inst.nivel)
      .map((x) => ({ m: x.m, p: ((movimientos as any)[x.m] || {}).poder || 0 }))
      .sort((a, b) => b.p - a.p).slice(0, 4).map((x) => x.m);
  }
  const movs = ids.map((mid) => ({ id: mid, ...((movimientos as any)[mid] || FORCEJEO) } as Mov));
  return movs.length ? movs : [FORCEJEO];
}

export function combatiente(inst: Inst): Combatiente {
  return {
    iid: inst.iid, id: inst.id, nombre: inst.mote || NOM[inst.id] || ('Nº ' + inst.id),
    nivel: inst.nivel, shiny: !!inst.shiny, tipos: tiposDe(inst.id),
    movs: movsDe(inst), hpMax: hpMax(inst.nivel), hp: hpMax(inst.nivel), atkMod: 1, defMod: 1,
  };
}

export const esEstado = (mov: Mov): boolean => mov.categoria === 'Estado' || !mov.poder;

export function calcularDano(atacante: Combatiente, mov: Mov, defensor: Combatiente, rng: Rng = Math.random) {
  const efec = efectividad(mov.tipo, defensor.tipos);
  const stab = atacante.tipos.includes(mov.tipo) ? 1.5 : 1;
  const base = (mov.poder || 40) * 0.18 * (1 + atacante.nivel * 0.03);
  const mod = (atacante.atkMod || 1) / (defensor.defMod || 1);
  const rand = 0.85 + rng() * 0.15;
  return { dmg: Math.max(1, Math.round(base * efec * stab * mod * rand)), efec, stab };
}

export function aplicarEstado(mov: Mov, atacante: Combatiente, defensor: Combatiente): string {
  const d = mov.desc || '';
  const baja = /\b(baja|reduce|disminu|debilita)/i.test(d);
  const sube = /\b(sube|aumenta|increment|refuerza|crece|eleva)/i.test(d);
  const stat = /defensa/i.test(d) ? 'def' : /ataque/i.test(d) ? 'atk' : null;
  if (!stat || (!baja && !sube)) return '…pero no tuvo mucho efecto.';
  const target = sube ? atacante : defensor;
  const key = stat === 'def' ? 'defMod' : 'atkMod';
  (target as any)[key] = Math.max(0.4, Math.min(2.2, ((target as any)[key] || 1) * (baja ? 0.7 : 1.4)));
  return target.nombre + ': ' + (stat === 'def' ? 'Defensa' : 'Ataque') + (baja ? ' bajó ↓' : ' subió ↑');
}

export function danoSuper(atacante: Combatiente, defensor: Combatiente, calidad = 1, rng: Rng = Math.random) {
  const mejor = [...atacante.movs].sort((a, b) => efectividad(b.tipo, defensor.tipos) - efectividad(a.tipo, defensor.tipos))[0] || atacante.movs[0];
  const r = calcularDano(atacante, mejor, defensor, rng);
  return { dmg: Math.round(r.dmg * (2 + calidad * 1.5)), efec: r.efec, mov: mejor };
}

export function elegirCPU(atacante: Combatiente, defensor: Combatiente): Mov {
  return [...atacante.movs]
    .map((mv) => ({ mv, e: efectividad(mv.tipo, defensor.tipos) * (mv.poder || 0) }))
    .sort((a, b) => b.e - a.e)[0].mv;
}

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

const jugadorDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid === uid);
const rivalDe = (e: EstadoCombate, uid: string) => e.jugadores.find((j) => j.uid !== uid)!;
const vivos = (j: JugadorEstado) => j.equipo.filter((c) => c.hp > 0).length;
const activoDe = (j: JugadorEstado) => j.equipo[j.activo];

// crea el combate a partir de los equipos elegidos (instancias). fase = combate.
export function crearCombate(roomId: string, jugadores: { uid: string; nombre: string; equipo: Inst[] }[], primero?: string): EstadoCombate {
  const js = jugadores.map((j) => ({
    uid: j.uid, nombre: j.nombre, equipo: j.equipo.slice(0, 3).map(combatiente), activo: 0, super: 0, listo: true,
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
    const fin1 = postGolpe(e, rival, push); if (fin1) return { estado: e, eventos };
    pasarTurno(e, uid);
    return { estado: e, eventos };
  }

  // fuera de turno
  if (e.turno !== uid) return err('no-es-tu-turno');
  const atk = activoDe(yo), def = activoDe(rival);

  switch (accion.tipo) {
    case 'mover': {
      const mov = atk.movs[accion.i ?? 0]; if (!mov) return err('mov-invalido');
      if (esEstado(mov)) {
        push('estado', `${atk.nombre} usó ${mov.nombre}. ` + aplicarEstado(mov, atk, def), { mov: mov.id });
      } else {
        const r = calcularDano(atk, mov, def, rng);
        def.hp = Math.max(0, def.hp - r.dmg);
        const ef = etiquetaEfec(r.efec);
        push('mover', `${atk.nombre} usó ${mov.nombre}: ${r.dmg} de daño.${ef ? ' ' + ef : ''}`, { dmg: r.dmg, efec: r.efec, mov: mov.id });
      }
      yo.super = Math.min(SUPER_MAX, yo.super + SUPER_GANANCIA);
      const fin = postGolpe(e, rival, push); if (fin) return { estado: e, eventos };
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
      const cura = POCION_CURA[accion.itemId || 'pocion'] ?? 30;
      const antes = atk.hp; atk.hp = Math.min(atk.hpMax, atk.hp + cura);
      push('pocion', `${yo.nombre} curó a ${atk.nombre} (+${atk.hp - antes} HP).`, { cura: atk.hp - antes });
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

// tras un golpe: si el rival activo cayó, auto-switch o fin. Devuelve true si el combate terminó.
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
      equipo: j.equipo.map((c) => ({ iid: c.iid, id: c.id, nombre: c.nombre, nivel: c.nivel, shiny: c.shiny, tipos: c.tipos, hp: c.hp, hpMax: c.hpMax, movs: c.movs })),
    })),
    eventos: e.eventos.slice(-12),
  };
}
