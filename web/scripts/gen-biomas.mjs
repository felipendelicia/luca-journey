// gen-biomas.mjs — mapea cada especie a un bioma (hierba/agua/cueva) por su habitat en PokeAPI.
// Salida: web/src/data/biomas.json {id: "hierba"|"agua"|"cueva"}. Correr: node scripts/gen-biomas.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'biomas.json');
const MAX = 1025;
const get = async (u) => {
  for (let i = 0; i < 4; i++) { try { const r = await fetch(u); if (r.ok) return r.json(); } catch {} await new Promise((s) => setTimeout(s, 400 * (i + 1))); }
  throw new Error('fallo ' + u);
};
const BIOMA = (hab) => hab === 'waters-edge' || hab === 'sea' ? 'agua' : hab === 'cave' ? 'cueva' : 'hierba';

const out = {};
for (let id = 1; id <= MAX; id++) {
  const sp = await get(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
  out[id] = BIOMA(sp.habitat && sp.habitat.name);
  if (id % 50 === 0) console.log('… biomas', id);
}
fs.writeFileSync(OUT, JSON.stringify(out));
const c = Object.values(out).reduce((a, b) => ((a[b] = (a[b] || 0) + 1), a), {});
console.log('✓ biomas.json', Object.keys(out).length, 'especies', JSON.stringify(c));
