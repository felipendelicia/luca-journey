// batalla.js — motor de combate (puro). Stats por nivel, daño con tipo/STAB, IA, súper por código.
import movimientos from '../data/movimientos.json' with { type: 'json' };
import learnsets from '../data/learnsets.json' with { type: 'json' };
import pokemon from '../data/pokemon.json' with { type: 'json' };
import { tiposDe, efectividad } from './tipos.js';

const NOM = Object.fromEntries(pokemon.map((p) => [p.id, p.nombre]));
const FORCEJEO = { id: 0, nombre: 'Forcejeo', tipo: 'Normal', poder: 40 };

export const hpMax = (nivel) => 40 + nivel * 5;

// movimientos de combate de una instancia: sus 4 activos; si no eligió, los 4 de MAYOR poder
// que tenga desbloqueados (auto-equipo competente).
function movsDe(inst) {
  const ls = learnsets[inst.id] || [];
  let ids = (inst.movs || []).filter(Boolean);
  if (!ids.length) {
    ids = ls.filter((x) => x.n <= inst.nivel)
      .map((x) => ({ m: x.m, p: (movimientos[x.m] || {}).poder || 0 }))
      .sort((a, b) => b.p - a.p).slice(0, 4).map((x) => x.m);
  }
  const movs = ids.map((mid) => ({ id: mid, ...(movimientos[mid] || FORCEJEO) }));
  return movs.length ? movs : [FORCEJEO];
}

// combatiente listo para pelear (a partir de una instancia del PC). atkMod/defMod = etapas de
// stat (1 = normal), que cambian los movimientos de estado (Gruñido, Malicioso, Látigo…).
export function combatiente(inst) {
  return {
    iid: inst.iid, id: inst.id, nombre: inst.mote || NOM[inst.id] || ('Nº ' + inst.id),
    nivel: inst.nivel, shiny: !!inst.shiny, tipos: tiposDe(inst.id),
    movs: movsDe(inst), hpMax: hpMax(inst.nivel), hp: hpMax(inst.nivel), atkMod: 1, defMod: 1,
    estado: null, estadoT: 0,
  };
}

// ¿es un movimiento de estado (sin daño)?
export const esEstado = (mov) => mov.categoria === 'Estado' || !mov.poder;

// daño de un movimiento (atacante → defensor), con tipo, STAB, etapas de stat y quemadura. {dmg, efec, stab}.
export function calcularDano(atacante, mov, defensor, rng = Math.random) {
  const efec = efectividad(mov.tipo, defensor.tipos);
  const stab = atacante.tipos.includes(mov.tipo) ? 1.5 : 1;
  const base = (mov.poder || 40) * 0.18 * (1 + atacante.nivel * 0.03);
  const mod = (atacante.atkMod || 1) / (defensor.defMod || 1);
  const quema = (atacante.estado === 'quemadura' && mov.categoria === 'Físico') ? 0.5 : 1;   // quemado pega menos físico
  const rand = 0.85 + rng() * 0.15;
  return { dmg: Math.max(1, Math.round(base * efec * stab * mod * quema * rand)), efec, stab };
}

// ───────── estados alterados (compartido con el motor del server) ─────────
export const ESTADOS = {
  veneno:    { ico: '☠️', sigla: 'PSN', color: '#9b59c4', nombre: 'Envenenado' },
  quemadura: { ico: '🔥', sigla: 'QMD', color: '#f0803a', nombre: 'Quemado' },
  paralisis: { ico: '⚡', sigla: 'PAR', color: '#e6c52e', nombre: 'Paralizado' },
  sueno:     { ico: '💤', sigla: 'DRM', color: '#8088a8', nombre: 'Dormido' },
  congelado: { ico: '❄️', sigla: 'CNG', color: '#74c7d8', nombre: 'Congelado' },
  confusion: { ico: '💫', sigla: 'CNF', color: '#c060b0', nombre: 'Confuso' },
};
const TXT_AIL = { veneno: 'fue envenenado', quemadura: 'sufrió una quemadura', paralisis: 'fue paralizado', sueno: 'se durmió', congelado: 'se congeló', confusion: 'se confundió' };

// ¿acierta el movimiento? rng*100 < precisión (sin precisión = siempre pega).
export const acierta = (mov, rng = Math.random) => (rng() * 100) < (mov.precision == null ? 100 : mov.precision);

// ¿puede actuar este turno? maneja sueño/congelado/parálisis/confusión (muta c). Devuelve
// { actua, texto, autogolpe? } (autogolpe = HP que se quitó a sí mismo por confusión).
export function puedeActuar(c, rng = Math.random) {
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

// aplica el estado del move al defensor (si corresponde). Un move de Fuego descongela. Devuelve texto|''.
export function aplicarAilment(mov, atacante, defensor, rng = Math.random) {
  if (mov.tipo === 'Fuego' && defensor.estado === 'congelado') defensor.estado = null;
  if (!mov.ailment || defensor.estado || defensor.hp <= 0) return '';
  const chance = mov.ailmentChance || 100;          // 0 (estado puro) = garantizado
  if (rng() * 100 >= chance) return '';
  defensor.estado = mov.ailment;
  if (mov.ailment === 'sueno') defensor.estadoT = 1 + Math.floor(rng() * 3);       // 1-3 turnos
  if (mov.ailment === 'confusion') defensor.estadoT = 1 + Math.floor(rng() * 4);   // 1-4 turnos
  return '¡' + defensor.nombre + ' ' + TXT_AIL[mov.ailment] + '!';
}

// daño por turno de veneno/quemadura (muta c). Devuelve { dmg, texto }.
export function tickEstado(c) {
  if (c.estado === 'veneno' || c.estado === 'quemadura') {
    const dmg = Math.max(1, Math.floor(c.hpMax / 8));
    c.hp = Math.max(0, c.hp - dmg);
    return { dmg, texto: c.nombre + (c.estado === 'veneno' ? ' sufre por el veneno' : ' sufre por la quemadura') + ' (-' + dmg + ')' };
  }
  return { dmg: 0, texto: '' };
}

// aplica un movimiento de ESTADO: lee la descripción y sube/baja Ataque o Defensa. Devuelve texto.
export function aplicarEstado(mov, atacante, defensor) {
  const d = mov.desc || '';
  const baja = /\b(baja|reduce|disminu|debilita)/i.test(d);
  const sube = /\b(sube|aumenta|increment|refuerza|crece|eleva)/i.test(d);
  const stat = /defensa/i.test(d) ? 'def' : /ataque/i.test(d) ? 'atk' : null;
  if (!stat || (!baja && !sube)) return '…pero no tuvo mucho efecto.';
  const target = sube ? atacante : defensor;          // subir = a uno mismo; bajar = al rival
  const key = stat === 'def' ? 'defMod' : 'atkMod';
  target[key] = Math.max(0.4, Math.min(2.2, (target[key] || 1) * (baja ? 0.7 : 1.4)));
  return target.nombre + ': ' + (stat === 'def' ? 'Defensa' : 'Ataque') + (baja ? ' bajó ↓' : ' subió ↑');
}

// SÚPER (código resuelto): golpe grande con el mejor movimiento por tipo. calidad 0..1.
export function danoSuper(atacante, defensor, calidad = 1) {
  const mejor = [...atacante.movs].sort((a, b) => efectividad(b.tipo, defensor.tipos) - efectividad(a.tipo, defensor.tipos))[0] || atacante.movs[0];
  const r = calcularDano(atacante, mejor, defensor);
  return { dmg: Math.round(r.dmg * (2 + calidad * 1.5)), efec: r.efec, mov: mejor };
}

// IA: elige el movimiento de mayor daño esperado (prefiere los de daño sobre los de estado).
export function elegirCPU(atacante, defensor) {
  return [...atacante.movs]
    .map((mv) => ({ mv, e: efectividad(mv.tipo, defensor.tipos) * (mv.poder || 0) }))
    .sort((a, b) => b.e - a.e)[0].mv;
}

// arma un equipo CPU de N instancias “salvajes” a un nivel objetivo, de un pool de especies.
export function equipoCPU(poolIds, n, nivel) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const id = poolIds[Math.floor(Math.random() * poolIds.length)];
    out.push(combatiente({ iid: 'cpu' + i, id, nivel, movs: [], shiny: false }));
  }
  return out;
}
