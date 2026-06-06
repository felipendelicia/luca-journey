// gen-movimientos.mjs — learnsets (movimientos por nivel) + metadata de cada move, desde PokeAPI.
// Salidas:
//   learnsets.json    { "<especieId>": [ {m:<moveId>, n:<nivel>}, ... ] }  (level-up, ordenado, dedup nivel más bajo)
//   movimientos.json  { "<moveId>": { nombre, tipo, poder } }              (nombre ES, tipo ES, poder|null)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.resolve(HERE, '..', 'src', 'data');
const N = 1025;
const TIPO_ES = {
  normal: 'Normal', fighting: 'Lucha', flying: 'Volador', poison: 'Veneno', ground: 'Tierra',
  rock: 'Roca', bug: 'Bicho', ghost: 'Fantasma', steel: 'Acero', fire: 'Fuego', water: 'Agua',
  grass: 'Planta', electric: 'Eléctrico', psychic: 'Psíquico', ice: 'Hielo', dragon: 'Dragón',
  dark: 'Siniestro', fairy: 'Hada',
};
async function jget(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} } return null; }
const idDe = (u) => Number(u.match(/\/(\d+)\/?$/)?.[1]);
async function lotes(items, n, fn) { for (let i = 0; i < items.length; i += n) { await Promise.all(items.slice(i, i + n).map(fn)); process.stdout.write('.'); } }

// 1) learnsets level-up por especie
const learnsets = {};
const moveIds = new Set();
await lotes(Array.from({ length: N }, (_, i) => i + 1), 16, async (id) => {
  const p = await jget(`https://pokeapi.co/api/v2/pokemon/${id}`);
  if (!p?.moves) { learnsets[id] = []; return; }
  const porMove = {};
  for (const mv of p.moves) {
    const mid = idDe(mv.move.url);
    let nivel = Infinity;
    for (const d of mv.version_group_details) {
      if (d.move_learn_method.name === 'level-up' && d.level_learned_at > 0) nivel = Math.min(nivel, d.level_learned_at);
    }
    if (nivel !== Infinity) { porMove[mid] = Math.min(porMove[mid] ?? Infinity, nivel); moveIds.add(mid); }
  }
  learnsets[id] = Object.entries(porMove).map(([m, n]) => ({ m: Number(m), n })).sort((a, b) => a.n - b.n || a.m - b.m);
});
console.log(`\nlearnsets: ${Object.keys(learnsets).length} especies · ${moveIds.size} moves únicos`);

// 2) metadata de cada move usado
const movimientos = {};
await lotes([...moveIds], 20, async (mid) => {
  const mv = await jget(`https://pokeapi.co/api/v2/move/${mid}`);
  if (!mv) return;
  const es = (mv.names || []).find((x) => x.language.name === 'es');
  movimientos[mid] = {
    nombre: es?.name || mv.name,
    tipo: TIPO_ES[mv.type?.name] || (mv.type?.name || '—'),
    poder: mv.power ?? null,
  };
});
console.log(`\nmovimientos: ${Object.keys(movimientos).length}`);

fs.writeFileSync(path.join(DATA, 'learnsets.json'), JSON.stringify(learnsets));
fs.writeFileSync(path.join(DATA, 'movimientos.json'), JSON.stringify(movimientos));
console.log('✓ learnsets.json + movimientos.json');
