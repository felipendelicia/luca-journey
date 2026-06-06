// gen-pokemon.mjs — ONE-SHOT: baja la lista de Pokémon (gen 1-3) de la PokéAPI
// y la guarda en src/data/pokemon.json (id, nombre, region). Se corre una vez.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'pokemon.json');

const cap = (s) => s.split('-').map((w) => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
// La PokéAPI da el nombre de la FORMA por defecto (ej. "mimikyu-disguised"); sacamos ese sufijo
// para mostrar el nombre base ("Mimikyu"). Lista curada de formas (no chocan con nombres base).
const FORMAS = /\s+(Disguised|Incarnate|Standard|Ordinary|Aria|Average|Baile|Pau|Pom Pom|Sensu|Midday|Midnight|Dusk|Solo|School|Amped|Low Key|Ice|Noice|Full Belly|Hangry|Single Strike|Rapid Strike|Zero|Hero|Combat Breed|Blaze Breed|Aqua Breed|Green Plumage|Blue Plumage|Yellow Plumage|White Plumage|Curly|Droopy|Stretchy|Two Segment|Three Segment|Family Of Three|Family Of Four|Plant|Sandy|Trash|Red Striped|Blue Striped|White Striped|Male|Female|Altered|Origin|Land|Sky)$/;
const limpiarForma = (n) => n.replace(FORMAS, '').trim();
const regionDe = (id) => (
  id <= 151 ? 'kanto' : id <= 251 ? 'johto' : id <= 386 ? 'hoenn' : id <= 493 ? 'sinnoh'
  : id <= 649 ? 'unova' : id <= 721 ? 'kalos' : id <= 809 ? 'alola' : id <= 905 ? 'galar' : 'paldea');

const res = await fetch('https://pokeapi.co/api/v2/pokemon?limit=1025');
const data = await res.json();
const lista = data.results.map((p, i) => ({ id: i + 1, nombre: limpiarForma(cap(p.name)), region: regionDe(i + 1) }));

fs.writeFileSync(OUT, JSON.stringify(lista));
console.log(`✓ pokemon.json: ${lista.length} Pokémon (Kanto…Paldea, gen 1-9)`);
