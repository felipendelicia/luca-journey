// gen-tipos.mjs — tipo(s) de cada Pokémon (1..721) desde PokeAPI. Salida tipos.json:
//   { "<id>": ["Fuego"], "<id>": ["Agua","Volador"], ... }  (en español)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'tipos.json');
const N = 1025;
const TIPO_ES = {
  normal: 'Normal', fighting: 'Lucha', flying: 'Volador', poison: 'Veneno', ground: 'Tierra',
  rock: 'Roca', bug: 'Bicho', ghost: 'Fantasma', steel: 'Acero', fire: 'Fuego', water: 'Agua',
  grass: 'Planta', electric: 'Eléctrico', psychic: 'Psíquico', ice: 'Hielo', dragon: 'Dragón',
  dark: 'Siniestro', fairy: 'Hada',
};
async function jget(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} } return null; }

const out = {};
const ids = Array.from({ length: N }, (_, i) => i + 1);
for (let i = 0; i < ids.length; i += 20) {
  await Promise.all(ids.slice(i, i + 20).map(async (id) => {
    const p = await jget(`https://pokeapi.co/api/v2/pokemon/${id}`);
    out[id] = (p?.types || []).sort((a, b) => a.slot - b.slot).map((t) => TIPO_ES[t.type.name] || t.type.name);
    if (!out[id].length) out[id] = ['Normal'];
  }));
  process.stdout.write('.');
}
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`\n✓ tipos.json: ${Object.keys(out).length}`);
