// gen-yields.mjs — baja el effort yield (EVs que da derrotar la especie) de PokeAPI.
// Salida: web/src/data/yields.json {id:[h,a,d,sa,sd,sp]}. Correr: node scripts/gen-yields.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'yields.json');
const MAX = 721;
const ORD = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'];
const get = async (u) => {
  for (let intento = 0; intento < 4; intento++) {
    try { const r = await fetch(u); if (r.ok) return r.json(); } catch (e) { /* reintenta */ }
    await new Promise((res) => setTimeout(res, 400 * (intento + 1)));
  }
  throw new Error('fallo ' + u);
};

const out = {};
for (let id = 1; id <= MAX; id++) {
  const p = await get(`https://pokeapi.co/api/v2/pokemon/${id}`);
  const m = {}; p.stats.forEach((s) => { m[s.stat.name] = s.effort; });
  out[id] = ORD.map((k) => m[k] || 0);
  if (id % 50 === 0) console.log('… yields', id);
}
fs.writeFileSync(OUT, JSON.stringify(out));
console.log('✓ yields.json', Object.keys(out).length, 'especies');
