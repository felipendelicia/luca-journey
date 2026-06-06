// gen-movimientos-detalle.mjs — re-enriquece movimientos.json con stats + descripción (ES).
// Lee los moveIds que ya usan los learnsets y refetchea SOLO esos moves (no toca pokemon).
// Salida movimientos.json: { "<id>": { nombre, tipo, poder, precision, pp, categoria, desc } }
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.resolve(HERE, '..', 'src', 'data');
const learnsets = JSON.parse(fs.readFileSync(path.join(DATA, 'learnsets.json'), 'utf8'));

const TIPO_ES = {
  normal: 'Normal', fighting: 'Lucha', flying: 'Volador', poison: 'Veneno', ground: 'Tierra',
  rock: 'Roca', bug: 'Bicho', ghost: 'Fantasma', steel: 'Acero', fire: 'Fuego', water: 'Agua',
  grass: 'Planta', electric: 'Eléctrico', psychic: 'Psíquico', ice: 'Hielo', dragon: 'Dragón',
  dark: 'Siniestro', fairy: 'Hada',
};
const CAT_ES = { physical: 'Físico', special: 'Especial', status: 'Estado' };
async function jget(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} } return null; }
const limpiar = (s) => (s || '').replace(/[\n\f\r]+/g, ' ').replace(/\s+/g, ' ').trim();

const moveIds = new Set();
for (const id in learnsets) for (const x of learnsets[id]) moveIds.add(x.m);

const movimientos = {};
const ids = [...moveIds];
for (let i = 0; i < ids.length; i += 20) {
  await Promise.all(ids.slice(i, i + 20).map(async (mid) => {
    const mv = await jget(`https://pokeapi.co/api/v2/move/${mid}`);
    if (!mv) return;
    const nombre = (mv.names || []).find((x) => x.language.name === 'es')?.name || mv.name;
    const flavES = (mv.flavor_text_entries || []).filter((x) => x.language.name === 'es');
    const efES = (mv.effect_entries || []).find((x) => x.language.name === 'es');
    let desc = limpiar(flavES.length ? flavES[flavES.length - 1].flavor_text : (efES ? efES.short_effect : ''));
    if (desc) desc = desc.replace('$effect_chance', String(mv.effect_chance ?? ''));
    movimientos[mid] = {
      nombre,
      tipo: TIPO_ES[mv.type?.name] || mv.type?.name || '—',
      poder: mv.power ?? null,
      precision: mv.accuracy ?? null,
      pp: mv.pp ?? null,
      categoria: CAT_ES[mv.damage_class?.name] || '—',
      desc,
    };
  }));
  process.stdout.write('.');
}
fs.writeFileSync(path.join(DATA, 'movimientos.json'), JSON.stringify(movimientos));
console.log(`\n✓ movimientos.json enriquecido: ${Object.keys(movimientos).length}`);
