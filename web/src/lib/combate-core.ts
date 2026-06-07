// combate-core.ts — REGLAS de combate puras: tipos, daño, estados alterados e IA. SIN DOM, SIN red,
// SIN data hardcodeada (la data tipos/movimientos/learnsets/pokemon se INYECTA). Es la ÚNICA fuente
// de verdad compartida por la práctica (web: batalla.js) y el PvP (server: motor.ts).
// ⚠️ Vive en web/src/lib/; `api/scripts/sync-batalla-data.mjs` copia una réplica a api/src/batalla/.
// La orquestación NO va acá: el cliente anima en batalla.astro; el server tiene su máquina de salas.

export type Rng = () => number;
export type EstadoAlt = null | 'veneno' | 'quemadura' | 'paralisis' | 'sueno' | 'congelado' | 'confusion';
export interface Mov { id: number; nombre: string; tipo: string; poder?: number; categoria?: string; desc?: string; precision?: number | null; ailment?: EstadoAlt; ailmentChance?: number; pp?: number; ppMax?: number; }
export interface Inst { iid: string; id: number; nivel: number; shiny?: boolean; mote?: string; movs?: number[];
  ivs?: number[]; nat?: number; hab?: string; gen?: 'm' | 'f' | null; evs?: number[]; }
export interface Combatiente {
  iid: string; id: number; nombre: string; nivel: number; shiny: boolean; tipos: string[];
  movs: Mov[]; hpMax: number; hp: number; atkMod: number; defMod: number; estado: EstadoAlt; estadoT: number;
  atk: number; def: number; spa: number; spd: number; spe: number;   // stats EFECTIVAS (con IV/EV/naturaleza)
  hab?: string | null; gen?: 'm' | 'f' | null;
}
// data que cada lado inyecta (con sus propios JSON) para construir combatientes
export interface DatosCombate {
  nombres: Record<number, string>;
  tipos: Record<string, string[]>;
  learnsets: Record<string, { m: number; n: number }[]>;
  movimientos: Record<string, any>;
  estadisticas?: Record<string, number[]>;   // [hp, atk, def, spa, spd, spe] por id
  habilidades?: { especies: Record<string, { key: string; hidden: boolean }[]>; genero: Record<string, number>; meta: Record<string, { nombre: string; desc: string; efecto: boolean }> };
}

// ───────────────────────── tipos / efectividad ─────────────────────────
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

// ───────────────────────── identidad: naturalezas / IVs / género / habilidad ─────────────────────────
// stat index: 1=Atk 2=Def 3=SpA 4=SpD 5=Vel (HP=0 nunca lo afecta la naturaleza).
export interface Naturaleza { nombre: string; sube: number | null; baja: number | null; }
export const NATURALEZAS: Naturaleza[] = [
  { nombre: 'Fuerte',  sube: null, baja: null },      // 0 neutra
  { nombre: 'Huraña',  sube: 1, baja: 2 }, { nombre: 'Audaz',   sube: 1, baja: 5 },
  { nombre: 'Firme',   sube: 1, baja: 3 }, { nombre: 'Pícara',  sube: 1, baja: 4 },
  { nombre: 'Osada',   sube: 2, baja: 1 }, { nombre: 'Dócil',   sube: null, baja: null }, // 6 neutra
  { nombre: 'Plácida', sube: 2, baja: 5 }, { nombre: 'Agitada', sube: 2, baja: 3 },
  { nombre: 'Floja',   sube: 2, baja: 4 }, { nombre: 'Miedosa', sube: 5, baja: 1 },
  { nombre: 'Activa',  sube: 5, baja: 2 }, { nombre: 'Seria',   sube: null, baja: null }, // 12 neutra
  { nombre: 'Alegre',  sube: 5, baja: 3 }, { nombre: 'Ingenua', sube: 5, baja: 4 },
  { nombre: 'Modesta', sube: 3, baja: 1 }, { nombre: 'Afable',  sube: 3, baja: 2 },
  { nombre: 'Mansa',   sube: 3, baja: 5 }, { nombre: 'Cándida', sube: null, baja: null }, // 18 neutra
  { nombre: 'Alocada', sube: 3, baja: 4 }, { nombre: 'Serena',  sube: 4, baja: 1 },
  { nombre: 'Amable',  sube: 4, baja: 2 }, { nombre: 'Grosera', sube: 4, baja: 5 },
  { nombre: 'Cauta',   sube: 4, baja: 3 }, { nombre: 'Rara',    sube: null, baja: null }, // 24 neutra
];

// hash estable string→uint32 (FNV-1a)
export function semilla(iid: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < iid.length; i++) { h ^= iid.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return h >>> 0;
}
// PRNG determinista (mulberry32)
function prng(seed: number): Rng {
  let a = seed >>> 0;
  return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

type Ident = { ivs: number[]; nat: number; hab: string | null; gen: 'm' | 'f' | null };

// rolea una identidad nueva (captura). rng por defecto = Math.random.
export function rolarIdentidad(id: number, habData: DatosCombate['habilidades'], rng: Rng = Math.random): Ident {
  const ivs = [0, 0, 0, 0, 0, 0].map(() => Math.floor(rng() * 32));
  const nat = Math.floor(rng() * 25);
  const pool = (habData?.especies || {})[String(id)] || [];
  const normals = pool.filter((a) => !a.hidden), hiddens = pool.filter((a) => a.hidden);
  const hidR = rng();
  const hab = (hidR < 0.05 && hiddens.length) ? hiddens[0].key
    : (normals.length ? normals[Math.floor(rng() * normals.length)].key : (pool[0]?.key || null));
  const rate = (habData?.genero || {})[String(id)];
  const gen: 'm' | 'f' | null = (rate == null || rate < 0) ? null : (rng() < rate / 8 ? 'f' : 'm');
  return { ivs, nat, hab, gen };
}

// identidad de una instancia: campos explícitos si están; si no, derivada del iid (estable, sin migración).
export function identidad(inst: Inst, d: DatosCombate): Ident {
  if (inst.ivs && inst.nat != null) return { ivs: inst.ivs, nat: inst.nat, hab: inst.hab ?? null, gen: inst.gen ?? null };
  return rolarIdentidad(inst.id, d.habilidades, prng(semilla(inst.iid)));
}

// ───────────────────────── combatientes (data inyectada) ─────────────────────────
export const FORCEJEO: Mov = { id: 0, nombre: 'Forcejeo', tipo: 'Normal', poder: 40 };
export const hpMax = (nivel: number): number => 40 + nivel * 5;   // fallback si no hay stats base
export const tiposDe = (id: number, tipos: Record<string, string[]>): string[] => tipos[String(id)] || ['Normal'];

// stats efectivas estilo Gen 3 con IV (0-31), EV (0-252) y multiplicador de naturaleza (1.1/0.9/1).
export const statEf = (base: number, nivel: number, iv = 0, ev = 0, natMult = 1): number =>
  Math.floor((Math.floor((2 * (base || 60) + iv + Math.floor(ev / 4)) * nivel / 100) + 5) * natMult);
export const hpEf = (baseHp: number, nivel: number, iv = 0, ev = 0): number =>
  Math.floor((2 * (baseHp || 60) + iv + Math.floor(ev / 4)) * nivel / 100) + nivel + 10;
// críticos: 1/16 como en Gen 3, daño ×2 (lo tira el orquestador y lo pasa a calcularDano).
export const CRIT_CHANCE = 1 / 16;
export const tiraCritico = (rng: Rng = Math.random): boolean => rng() < CRIT_CHANCE;
// split físico/especial: usa la categoría del move; si falta, por tipo (como en Gen 3).
const TIPOS_FISICOS = ['Normal', 'Lucha', 'Volador', 'Tierra', 'Roca', 'Bicho', 'Fantasma', 'Veneno', 'Acero'];
export const esFisico = (mov: Mov): boolean => mov.categoria ? mov.categoria === 'Físico' : TIPOS_FISICOS.includes(mov.tipo);

// 4 movimientos de combate de una instancia: sus activos; si no eligió, los 4 de mayor poder desbloqueados.
export function movsDe(inst: Inst, learnsets: DatosCombate['learnsets'], movimientos: DatosCombate['movimientos']): Mov[] {
  const ls = (learnsets as any)[inst.id] || [];
  let ids = (inst.movs || []).filter(Boolean);
  if (!ids.length) {
    ids = ls.filter((x: any) => x.n <= inst.nivel)
      .map((x: any) => ({ m: x.m, p: ((movimientos as any)[x.m] || {}).poder || 0 }))
      .sort((a: any, b: any) => b.p - a.p).slice(0, 4).map((x: any) => x.m);
  }
  const movs = ids.map((mid: number) => {
    const base = (movimientos as any)[mid] || FORCEJEO;
    const ppm = base.pp || 20;                                   // PP máximo del move (Gen 3)
    return { id: mid, ...base, pp: ppm, ppMax: ppm } as Mov;     // pp = usos restantes (arranca lleno)
  });
  return movs.length ? movs : [{ ...FORCEJEO }];
}

// ¿se quedó sin PP en todos los movimientos? (entonces solo le queda Forcejeo)
export const sinPP = (c: Combatiente): boolean => c.movs.every((m) => (m.pp ?? 1) <= 0);

// combatiente listo para pelear a partir de una instancia del PC + la data inyectada.
export function combatiente(inst: Inst, d: DatosCombate): Combatiente {
  const st = (d.estadisticas || {})[String(inst.id)];   // [hp, atk, def, spa, spd, spe] base
  const idn = identidad(inst, d);
  const ev = inst.evs || [0, 0, 0, 0, 0, 0];
  const nat = NATURALEZAS[idn.nat] || NATURALEZAS[0];
  const nm = (k: number) => nat.sube === k ? 1.1 : nat.baja === k ? 0.9 : 1;
  const hpM = st ? hpEf(st[0], inst.nivel, idn.ivs[0], ev[0]) : hpMax(inst.nivel);
  return {
    iid: inst.iid, id: inst.id, nombre: inst.mote || d.nombres[inst.id] || ('Nº ' + inst.id),
    nivel: inst.nivel, shiny: !!inst.shiny, tipos: tiposDe(inst.id, d.tipos),
    movs: movsDe(inst, d.learnsets, d.movimientos), hpMax: hpM, hp: hpM,
    atk: st ? statEf(st[1], inst.nivel, idn.ivs[1], ev[1], nm(1)) : 60,
    def: st ? statEf(st[2], inst.nivel, idn.ivs[2], ev[2], nm(2)) : 60,
    spa: st ? statEf(st[3], inst.nivel, idn.ivs[3], ev[3], nm(3)) : 60,
    spd: st ? statEf(st[4], inst.nivel, idn.ivs[4], ev[4], nm(4)) : 60,
    spe: st ? statEf(st[5], inst.nivel, idn.ivs[5], ev[5], nm(5)) : 60,
    atkMod: 1, defMod: 1, estado: null, estadoT: 0,
    hab: idn.hab, gen: idn.gen,
  };
}

// ───────────────────────── habilidades (core-contained) ─────────────────────────
const BOOST_TIPO: Record<string, string> = { overgrow: 'Planta', blaze: 'Fuego', torrent: 'Agua' };
const ABSORBE_TIPO: Record<string, string> = { levitate: 'Tierra', 'water-absorb': 'Agua', 'flash-fire': 'Fuego' };
const NO_ESTADO: Record<string, EstadoAlt> = { immunity: 'veneno', insomnia: 'sueno', 'magma-armor': 'congelado' };

// ¿la habilidad del defensor lo hace inmune a este tipo de movimiento?
export const habInmuneTipo = (c: Combatiente, tipoMov: string): boolean => !!c.hab && ABSORBE_TIPO[c.hab] === tipoMov;
// multiplicador de daño por habilidad del ATACANTE (Espesura/Mar Llamas/Torrente, Agallas).
export function habModDano(atacante: Combatiente, mov: Mov): number {
  let m = 1;
  if (atacante.hab && BOOST_TIPO[atacante.hab] === mov.tipo && atacante.hp / atacante.hpMax < 1 / 3) m *= 1.5;
  if (atacante.hab === 'guts' && atacante.estado && esFisico(mov)) m *= 1.5;
  return m;
}
// ¿la habilidad del defensor bloquea este estado?
export const habNoEstado = (c: Combatiente, estado: EstadoAlt): boolean => !!c.hab && NO_ESTADO[c.hab] === estado;
// multiplicador de precisión por habilidad del atacante (Ojo Compuesto).
export const habModPrecision = (c: Combatiente | undefined): number => (c && c.hab === 'compound-eyes') ? 1.3 : 1;

// AL ENTRAR a pista (Intimidación). Muta al rival. Devuelve texto|''.
export function habAlEntrar(self: Combatiente, rival: Combatiente): string {
  if (self.hab !== 'intimidate' || !rival || rival.hp <= 0) return '';
  rival.atkMod = Math.max(0.4, (rival.atkMod || 1) * 0.7);
  return '¡Intimidación de ' + self.nombre + '! El Ataque de ' + rival.nombre + ' bajó ↓';
}
// AL RECIBIR un golpe de CONTACTO (físico) — Estática/Cuerpo Llama. Muta al atacante. Devuelve texto|''.
export function habAlContacto(self: Combatiente, atacante: Combatiente, mov: Mov, rng: Rng = Math.random): string {
  if (!esFisico(mov) || atacante.hp <= 0 || atacante.estado) return '';
  if (self.hab === 'static' && rng() < 0.3) { atacante.estado = 'paralisis'; return '¡Estática de ' + self.nombre + ' paralizó a ' + atacante.nombre + '!'; }
  if (self.hab === 'flame-body' && rng() < 0.3 && !atacante.tipos.includes('Fuego')) { atacante.estado = 'quemadura'; return '¡Cuerpo Llama de ' + self.nombre + ' quemó a ' + atacante.nombre + '!'; }
  return '';
}

// ───────────────────────── daño ─────────────────────────
export const esEstado = (mov: Mov): boolean => mov.categoria === 'Estado' || !mov.poder;

export interface ResultadoDano { dmg: number; efec: number; stab: number; crit: boolean; inmuneHab?: string | null; sturdy?: boolean; }
export function calcularDano(atacante: Combatiente, mov: Mov, defensor: Combatiente, rng: Rng = Math.random, crit = false): ResultadoDano {
  const efec = efectividad(mov.tipo, defensor.tipos);
  if (habInmuneTipo(defensor, mov.tipo)) return { dmg: 0, efec: 0, stab: 1, crit: false, inmuneHab: defensor.hab };   // habilidad anula el tipo
  if (efec === 0) return { dmg: 0, efec, stab: 1, crit: false };   // inmune: no afecta
  const fisico = esFisico(mov);
  const stab = atacante.tipos.includes(mov.tipo) ? 1.5 : 1;
  const A = (fisico ? atacante.atk : atacante.spa) * (atacante.atkMod || 1);   // ya efectiva
  const D = (fisico ? defensor.def : defensor.spd) * (defensor.defMod || 1);
  const baseDmg = Math.floor(Math.floor((2 * atacante.nivel / 5 + 2) * (mov.poder || 40) * A / D) / 50) + 2;   // fórmula estilo Gen 3
  const quema = (atacante.estado === 'quemadura' && fisico) ? 0.5 : 1;   // quemado pega menos físico
  const rand = 0.85 + rng() * 0.15;
  let dmg = Math.max(1, Math.round(baseDmg * stab * efec * quema * (crit ? 2 : 1) * rand * habModDano(atacante, mov)));
  let sturdy = false;
  if (defensor.hab === 'sturdy' && defensor.hp === defensor.hpMax && dmg >= defensor.hp) { dmg = defensor.hp - 1; sturdy = true; }   // Robustez: aguanta a 1 HP desde full
  return { dmg, efec, stab, crit, sturdy };
}

// movimiento de ESTADO: lee la descripción y sube/baja Ataque o Defensa. Devuelve texto.
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

// SÚPER (código resuelto): golpe grande con el mejor movimiento por tipo. calidad 0..1.
export function danoSuper(atacante: Combatiente, defensor: Combatiente, calidad = 1, rng: Rng = Math.random) {
  const mejor = [...atacante.movs].sort((a, b) => efectividad(b.tipo, defensor.tipos) - efectividad(a.tipo, defensor.tipos))[0] || atacante.movs[0];
  const r = calcularDano(atacante, mejor, defensor, rng);
  return { dmg: Math.round(r.dmg * (2 + calidad * 1.5)), efec: r.efec, mov: mejor };
}

// IA: elige el movimiento de mayor daño esperado.
export function elegirCPU(atacante: Combatiente, defensor: Combatiente): Mov {
  const usables = atacante.movs.filter((m) => (m.pp ?? 1) > 0);
  const pool = usables.length ? usables : [{ ...FORCEJEO }];   // sin PP → Forcejeo
  return [...pool]
    .map((mv) => ({ mv, e: efectividad(mv.tipo, defensor.tipos) * (mv.poder || 0) }))
    .sort((a, b) => b.e - a.e)[0].mv;
}

// ───────────────────────── estados alterados ─────────────────────────
export const ESTADOS: Record<string, { ico: string; sigla: string; color: string; nombre: string }> = {
  veneno:    { ico: '☠️', sigla: 'PSN', color: '#9b59c4', nombre: 'Envenenado' },
  quemadura: { ico: '🔥', sigla: 'QMD', color: '#f0803a', nombre: 'Quemado' },
  paralisis: { ico: '⚡', sigla: 'PAR', color: '#e6c52e', nombre: 'Paralizado' },
  sueno:     { ico: '💤', sigla: 'DRM', color: '#8088a8', nombre: 'Dormido' },
  congelado: { ico: '❄️', sigla: 'CNG', color: '#74c7d8', nombre: 'Congelado' },
  confusion: { ico: '💫', sigla: 'CNF', color: '#c060b0', nombre: 'Confuso' },
};
const TXT_AIL: Record<string, string> = { veneno: 'fue envenenado', quemadura: 'sufrió una quemadura', paralisis: 'fue paralizado', sueno: 'se durmió', congelado: 'se congeló', confusion: 'se confundió' };
// inmunidad de estado por tipo (Gen 3): Fuego no se quema, Hielo no se congela, Veneno/Acero no se envenenan.
const INMUNE_AIL: Record<string, string[]> = { quemadura: ['Fuego'], congelado: ['Hielo'], veneno: ['Veneno', 'Acero'] };

export const acierta = (mov: Mov, rng: Rng = Math.random, atacante?: Combatiente): boolean =>
  (rng() * 100) < (mov.precision == null ? 100 : mov.precision * habModPrecision(atacante));

// ¿puede actuar este turno? maneja sueño/congelado/parálisis/confusión (muta c).
export function puedeActuar(c: Combatiente, rng: Rng = Math.random): { actua: boolean; texto: string; autogolpe?: number } {
  if (c.estado === 'congelado') {
    if (rng() < 0.2) { c.estado = null; return { actua: true, texto: '¡' + c.nombre + ' se descongeló!' }; }
    return { actua: false, texto: c.nombre + ' está congelado y no puede moverse.' };
  }
  if (c.estado === 'sueno') {
    c.estadoT = (c.estadoT || 1) - 1;
    if (c.estadoT <= 0) { c.estado = null; return { actua: true, texto: '¡' + c.nombre + ' se despertó!' }; }
    return { actua: false, texto: c.nombre + ' está profundamente dormido…' };
  }
  if (c.estado === 'paralisis' && rng() < 0.25) {
    return { actua: false, texto: '¡' + c.nombre + ' está paralizado! No puede moverse.' };
  }
  if (c.estado === 'confusion') {
    c.estadoT = (c.estadoT || 1) - 1;
    if (c.estadoT <= 0) { c.estado = null; return { actua: true, texto: '¡' + c.nombre + ' salió de la confusión!' }; }
    if (rng() < 0.33) {
      const dmg = Math.max(1, Math.round(c.hpMax * 0.08));
      c.hp = Math.max(0, c.hp - dmg);
      return { actua: false, texto: c.nombre + ' está confuso… ¡se golpeó a sí mismo!', autogolpe: dmg };
    }
  }
  return { actua: true, texto: '' };
}

// aplica el estado del move al defensor (si corresponde). Fuego descongela. Devuelve texto|''.
export function aplicarAilment(mov: Mov, atacante: Combatiente, defensor: Combatiente, rng: Rng = Math.random): string {
  if (mov.tipo === 'Fuego' && defensor.estado === 'congelado') defensor.estado = null;
  if (!mov.ailment || defensor.estado || defensor.hp <= 0) return '';
  if ((INMUNE_AIL[mov.ailment] || []).some((t) => defensor.tipos.includes(t))) return '';   // inmune por tipo
  if (habNoEstado(defensor, mov.ailment)) return '';   // habilidad bloquea el estado
  const chance = mov.ailmentChance || 100;
  if (rng() * 100 >= chance) return '';
  defensor.estado = mov.ailment;
  if (mov.ailment === 'sueno') defensor.estadoT = 1 + Math.floor(rng() * 3);
  if (mov.ailment === 'confusion') defensor.estadoT = 1 + Math.floor(rng() * 4);
  return '¡' + defensor.nombre + ' ' + TXT_AIL[mov.ailment] + '!';
}

// daño por turno de veneno/quemadura (muta c).
export function tickEstado(c: Combatiente): { dmg: number; texto: string } {
  if (c.hp <= 0) return { dmg: 0, texto: '' };
  if (c.estado === 'veneno' || c.estado === 'quemadura') {
    const dmg = Math.max(1, Math.floor(c.hpMax / 8));
    c.hp = Math.max(0, c.hp - dmg);
    return { dmg, texto: c.nombre + (c.estado === 'veneno' ? ' sufre por el veneno' : ' sufre por la quemadura') + ' (-' + dmg + ')' };
  }
  return { dmg: 0, texto: '' };
}
