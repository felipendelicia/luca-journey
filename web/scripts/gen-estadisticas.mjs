// gen-estadisticas.mjs — stats base de cada Pokémon (gen 1-721) desde PokeAPI.
// Salida: src/data/estadisticas.json = { "<id>": [hp, atk, def, spa, spd, spe] }
// En la app se escalan por nivel (ver pokedex.astro). Correr una vez (o si cambian datos).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'estadisticas.json');
const N = 1025;
const ORDEN = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'];

async function jget(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} } return null; }

const out = {};
const ids = Array.from({ length: N }, (_, i) => i + 1);
for (let i = 0; i < ids.length; i += 20) {
  await Promise.all(ids.slice(i, i + 20).map(async (id) => {
    const p = await jget(`https://pokeapi.co/api/v2/pokemon/${id}`);
    if (!p) return;
    const m = {}; for (const s of p.stats || []) m[s.stat.name] = s.base_stat;
    out[id] = ORDEN.map((k) => m[k] ?? 0);
  }));
  process.stdout.write('.');
}
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`\n✓ estadisticas.json: ${Object.keys(out).length} Pokémon (hp/atk/def/spa/spd/spe)`);
