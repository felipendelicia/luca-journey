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
  };
}

// ¿es un movimiento de estado (sin daño)?
export const esEstado = (mov) => mov.categoria === 'Estado' || !mov.poder;

// daño de un movimiento (atacante → defensor), con tipo, STAB y las etapas de stat. {dmg, efec, stab}.
export function calcularDano(atacante, mov, defensor) {
  const efec = efectividad(mov.tipo, defensor.tipos);
  const stab = atacante.tipos.includes(mov.tipo) ? 1.5 : 1;
  const base = (mov.poder || 40) * 0.18 * (1 + atacante.nivel * 0.03);
  const mod = (atacante.atkMod || 1) / (defensor.defMod || 1);
  const rand = 0.85 + Math.random() * 0.15;
  return { dmg: Math.max(1, Math.round(base * efec * stab * mod * rand)), efec, stab };
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
