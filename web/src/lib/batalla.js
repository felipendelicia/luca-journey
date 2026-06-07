// batalla.js — adaptador de la PRÁCTICA al motor compartido. Las reglas (tipos, daño, estados, IA)
// viven en combate-core.ts; acá solo se inyecta la data del front y se arman combatientes/equipo CPU.
import movimientos from '../data/movimientos.json' with { type: 'json' };
import learnsets from '../data/learnsets.json' with { type: 'json' };
import pokemon from '../data/pokemon.json' with { type: 'json' };
import tipos from '../data/tipos.json' with { type: 'json' };
import estadisticas from '../data/estadisticas.json' with { type: 'json' };
import habilidades from '../data/habilidades.json' with { type: 'json' };
import { combatiente as coreCombatiente } from './combate-core.ts';

// reglas puras: se re-exportan tal cual (única fuente de verdad)
export {
  hpMax, esEstado, calcularDano, aplicarEstado, danoSuper, elegirCPU, tiraCritico,
  ESTADOS, acierta, puedeActuar, aplicarAilment, tickEstado, efectividad, etiquetaEfec,
  FORCEJEO, sinPP, habAlEntrar, habAlContacto,
} from './combate-core.ts';

// data del front inyectada al core
const DATOS = {
  nombres: Object.fromEntries(pokemon.map((p) => [p.id, p.nombre])),
  tipos, learnsets, movimientos, estadisticas, habilidades,
};

// combatiente a partir de una instancia del PC (usa la data del front)
export const combatiente = (inst) => coreCombatiente(inst, DATOS);

// equipo CPU de N instancias “salvajes” a un nivel objetivo, de un pool de especies.
export function equipoCPU(poolIds, n, nivel) {
  const out = [];
  for (let i = 0; i < n; i++) {
    const id = poolIds[Math.floor(Math.random() * poolIds.length)];
    out.push(combatiente({ iid: 'cpu' + i, id, nivel, movs: [], shiny: false }));
  }
  return out;
}
