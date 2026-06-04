// gen-rarezas.mjs — ONE-SHOT: trae el capture_rate de cada especie (gen 1-6) de la
// PokéAPI y lo guarda en src/data/rarezas.json como { id: peso }. Mayor peso = aparece
// más seguido en el Safari (los comunes ~255, los legendarios ~3).
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'rarezas.json');

const peso = {};
const ids = Array.from({ length: 721 }, (_, i) => i + 1);
const lote = 25;
for (let i = 0; i < ids.length; i += lote) {
  await Promise.all(ids.slice(i, i + lote).map(async (id) => {
    try {
      const r = await fetch(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
      const s = await r.json();
      peso[id] = typeof s.capture_rate === 'number' ? s.capture_rate : 45;
    } catch (e) { peso[id] = 45; }
  }));
  process.stdout.write('.');
}
fs.writeFileSync(OUT, JSON.stringify(peso));
console.log(`\n✓ rarezas.json: ${Object.keys(peso).length} pesos (capture_rate)`);
