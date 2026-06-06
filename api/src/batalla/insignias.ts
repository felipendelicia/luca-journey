// insignias.ts — premios y logros del PvP (server-autoritativo). Al `fin` de un combate:
// ganador → caramelos de las familias que pelearon; perdedor → Pokébolas; ambos → insignias por
// hitos; se persiste en el `progreso` (mismo blob que sincroniza el front: valores string).
import { ProgresoService } from '../progreso/progreso.service';
import { EstadoCombate, JugadorEstado } from './motor';
import evoData from './data/evoluciones.json';

const familiaDe = (id: number): number => ((evoData as any)[id] && (evoData as any)[id].familia) || Number(id);

// legendarios (dex 1–721) — para la insignia `mata-legendario`.
const LEGENDARIOS = new Set([
  144, 145, 146, 150, 151, 243, 244, 245, 249, 250, 251, 377, 378, 379, 380, 381, 382, 383, 384,
  385, 386, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 494, 638, 639,
  640, 641, 642, 643, 644, 645, 646, 647, 648, 649, 716, 717, 718, 719, 720, 721,
]);

const CARAMELOS_GANADOR = 3;          // por familia que peleó
const BALLS_GANADOR = 5;              // el ganador también se lleva Pokébolas (premiar ganar)
const BALLS_PERDEDOR = 10;            // consuelo para el que pierde
const RATING_DEF = 1000, K = 32;      // ELO: rating inicial y factor K

export const ratingDe = (est: any): number => { try { return Number(JSON.parse(est['col:pvp'] || '{}').rating) || RATING_DEF; } catch { return RATING_DEF; } };
// ELO zero-sum: el ganador suma dG, el perdedor resta dG (según la diferencia de rating).
function elo(rG: number, rP: number) {
  const esperadoG = 1 / (1 + Math.pow(10, (rP - rG) / 400));
  const dG = Math.max(1, Math.round(K * (1 - esperadoG)));
  return { ng: rG + dG, np: Math.max(100, rP - dG), dG };
}

export interface Premios {
  gano: boolean; caramelos?: Record<number, number>; balls?: number; insignias?: string[];
  rating?: number; delta?: number;    // ELO nuevo y cuánto cambió
  estado?: Record<string, any>;       // blob actualizado para emitir al cliente (refresca su nube)
}

// helpers sobre el blob de progreso (valores serializados, igual que localStorage del front)
const pObj = (e: any, k: string, def: any) => { try { return JSON.parse(e[k] ?? JSON.stringify(def)); } catch { return def; } };
const pNum = (e: any, k: string) => Number(e[k] ?? '0') || 0;
const setObj = (e: any, k: string, v: any) => { e[k] = JSON.stringify(v); };

const vivos = (j: JugadorEstado) => j.equipo.filter((c) => c.hp > 0).length;

// otorga premios + insignias a ambos, persiste, y devuelve {uid: Premios}.
export async function premiar(
  progreso: ProgresoService, estado: EstadoCombate, abandonoUid?: string,
): Promise<Record<string, Premios>> {
  const ganadorUid = estado.ganador;
  const out: Record<string, Premios> = {};
  if (!ganadorUid) return out;
  const ganador = estado.jugadores.find((j) => j.uid === ganadorUid)!;
  const perdedor = estado.jugadores.find((j) => j.uid !== ganadorUid)!;

  // ELO: leer ratings actuales de ambos y calcular el nuevo
  const rG = ratingDe(await progreso.bajar(ganador.uid));
  const rP = ratingDe(await progreso.bajar(perdedor.uid));
  const { ng, np, dG } = elo(rG, rP);

  out[ganador.uid] = await aplicarUno(progreso, ganador, perdedor, true, false, ng, dG);
  out[perdedor.uid] = await aplicarUno(progreso, perdedor, ganador, false, abandonoUid === perdedor.uid, np, -dG);
  return out;
}

async function aplicarUno(
  progreso: ProgresoService, yo: JugadorEstado, rival: JugadorEstado, gano: boolean, abandono: boolean,
  nuevoRating: number, deltaRating: number,
): Promise<Premios> {
  const estado = await progreso.bajar(yo.uid) as Record<string, any>;
  const premios: Premios = { gano };

  // recompensa material
  if (gano) {
    const car: Record<number, number> = {};
    for (const c of yo.equipo) car[familiaDe(c.id)] = (car[familiaDe(c.id)] || 0) + CARAMELOS_GANADOR;
    const acum = pObj(estado, 'col:caramelos', {});
    for (const f in car) acum[f] = (acum[f] || 0) + car[f];
    setObj(estado, 'col:caramelos', acum);
    estado['col:balls'] = String(pNum(estado, 'col:balls') + BALLS_GANADOR);
    premios.caramelos = car; premios.balls = BALLS_GANADOR;
  } else {
    estado['col:balls'] = String(pNum(estado, 'col:balls') + BALLS_PERDEDOR);
    premios.balls = BALLS_PERDEDOR;
  }

  // stats PvP + insignias
  const st = pObj(estado, 'col:pvp', { jugados: 0, victorias: 0, racha: 0, abandonos: 0 });
  st.jugados += 1;
  if (gano) { st.victorias += 1; st.racha += 1; } else { st.racha = 0; }
  if (abandono) st.abandonos += 1;
  st.rating = nuevoRating;   // ELO
  // historial (últimos 10 duelos)
  const hist = pObj(estado, 'col:pvp_hist', []);
  hist.unshift({ t: Date.now(), rival: rival.nombre, gano, rating: nuevoRating, delta: deltaRating });
  setObj(estado, 'col:pvp_hist', hist.slice(0, 10));
  premios.rating = nuevoRating; premios.delta = deltaRating;

  const tengo: string[] = pObj(estado, 'col:insignias', []);
  const set = new Set(tengo);
  const nuevas: string[] = [];
  const dar = (id: string, cond: boolean) => { if (cond && !set.has(id)) { set.add(id); nuevas.push(id); } };

  dar('primer-duelo', st.jugados >= 1);
  dar('primera-victoria', st.victorias >= 1);
  dar('racha-3', st.racha >= 3);
  dar('racha-10', st.racha >= 10);
  dar('10-victorias', st.victorias >= 10);
  dar('mata-legendario', gano && rival.equipo.some((c) => LEGENDARIOS.has(c.id)));
  dar('remontada', gano && vivos(yo) === 1);

  setObj(estado, 'col:pvp', st);
  setObj(estado, 'col:insignias', [...set]);
  premios.insignias = nuevas;
  premios.estado = estado;

  await progreso.subir(yo.uid, estado);
  return premios;
}
