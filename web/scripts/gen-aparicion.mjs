// gen-aparicion.mjs — peso de APARICIÓN con datos REALES de la PokéAPI.
// Criterio: rareza por VALOR del Pokémon → total de stats base (BST) + legendario/mítico.
//   más fuerte = más raro (aparece menos); legendarios/míticos = rarísimos.
// Trae /pokemon/{id} (stats → BST) y /pokemon-species/{id} (is_legendary, is_mythical).
// Salida: src/data/aparicion.json { id: peso }. Más peso = aparece más seguido.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'aparicion.json');

const N = 1025;
const LOTE = 20;
const MIN_BST = 200, MAX_BST = 720;   // rango aprox. de BST en gen 1-6
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

async function jget(url) {
  for (let i = 0; i < 3; i++) {
    try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {}
  }
  return null;
}

function pesoDe(bst, legendario) {
  const t = clamp((bst - MIN_BST) / (MAX_BST - MIN_BST), 0, 1);   // 0 débil … 1 fuerte
  let w = Math.round(6 + (255 - 6) * Math.pow(1 - t, 1.9));        // débil→~255, fuerte→~6
  if (legendario) w = Math.min(w, 5);                             // legendario/mítico: piso bajo
  return Math.max(3, w);
}

const peso = {};
const ids = Array.from({ length: N }, (_, i) => i + 1);
for (let i = 0; i < ids.length; i += LOTE) {
  await Promise.all(ids.slice(i, i + LOTE).map(async (id) => {
    const [poke, spec] = await Promise.all([
      jget(`https://pokeapi.co/api/v2/pokemon/${id}`),
      jget(`https://pokeapi.co/api/v2/pokemon-species/${id}`),
    ]);
    const bst = poke && Array.isArray(poke.stats)
      ? poke.stats.reduce((a, s) => a + (s.base_stat || 0), 0) : 450;
    const leg = !!(spec && (spec.is_legendary || spec.is_mythical));
    peso[id] = pesoDe(bst, leg);
  }));
  process.stdout.write('.');
}

fs.writeFileSync(OUT, JSON.stringify(peso));
console.log(`\n✓ aparicion.json: ${Object.keys(peso).length} pesos (BST + legendario, PokéAPI)`);
