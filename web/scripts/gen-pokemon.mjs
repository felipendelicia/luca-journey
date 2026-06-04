// gen-pokemon.mjs — ONE-SHOT: baja la lista de Pokémon (gen 1-3) de la PokéAPI
// y la guarda en src/data/pokemon.json (id, nombre, region). Se corre una vez.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'pokemon.json');

const cap = (s) => s.split('-').map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
const regionDe = (id) => (id <= 151 ? 'kanto' : id <= 251 ? 'johto' : id <= 386 ? 'hoenn' : id <= 493 ? 'sinnoh' : 'unova');

const res = await fetch('https://pokeapi.co/api/v2/pokemon?limit=649');
const data = await res.json();
const lista = data.results.map((p, i) => ({ id: i + 1, nombre: cap(p.name), region: regionDe(i + 1) }));

fs.writeFileSync(OUT, JSON.stringify(lista));
console.log(`✓ pokemon.json: ${lista.length} Pokémon (Kanto/Johto/Hoenn/Sinnoh)`);
