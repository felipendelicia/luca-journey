// gen-evoluciones.mjs — ONE-SHOT: arma el mapa de evoluciones (gen 1-3) desde la
// PokéAPI y lo guarda en src/data/evoluciones.json. fromId -> [toId...].
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'evoluciones.json');
const idDe = (url) => +url.split('/').filter(Boolean).pop();

const evo = {};
const ids = Array.from({ length: 649 }, (_, i) => i + 1);
const lote = 25;
for (let i = 0; i < ids.length; i += lote) {
  await Promise.all(ids.slice(i, i + lote).map(async (id) => {
    try {
      const r = await fetch(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
      const s = await r.json();
      if (s.evolves_from_species) {
        const from = idDe(s.evolves_from_species.url);
        if (from >= 1 && from <= 649) (evo[from] ||= []).push(id);
      }
    } catch (e) { /* ignorar */ }
  }));
  process.stdout.write('.');
}
fs.writeFileSync(OUT, JSON.stringify(evo));
console.log(`\n✓ evoluciones.json: ${Object.keys(evo).length} Pokémon evolucionan`);
