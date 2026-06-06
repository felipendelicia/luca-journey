// gen-evoluciones.mjs — cadena evolutiva con datos REALES de PokeAPI.
// Salida: { "<id>": { evos:[{a:<evoId>, nivel:<min_level|0>, req?:<itemId>, m?:<metodo>}], familia:<idBase> } }
// 'nivel' = min_level del trigger level-up; si la evo NO es por nivel (piedra/trade/amistad),
// 'nivel' = 0. 'req' = item de la tienda que hace falta (piedra tipada / disco de enlace).
// 'm' = método ('piedra'|'trade'|'amistad'|'otro'); sin 'm' y nivel>0 = evo por nivel.
// 'familia' = id base.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'evoluciones.json');
const N = 1025, NIVEL_NO_LEVEL = 0;

// item.name de PokeAPI → id de la piedra tipada en la tienda (web/src/lib/items.js).
const MAP_STONE = {
  'fire-stone': 'piedrafuego', 'water-stone': 'piedraagua', 'thunder-stone': 'piedratrueno',
  'leaf-stone': 'piedrahoja', 'moon-stone': 'piedraluna', 'sun-stone': 'piedrasol',
  'shiny-stone': 'piedradia', 'dawn-stone': 'piedraalba', 'dusk-stone': 'piedranoche',
};

// deriva {req, m} del trigger de evolución de PokeAPI (evolution_details[0]).
function metodo(det) {
  const trig = det.trigger?.name;
  if (trig === 'use-item') { const req = MAP_STONE[det.item?.name]; return req ? { req, m: 'piedra' } : { m: 'otro' }; }
  if (trig === 'trade') return { req: 'discoenlace', m: 'trade' };
  if (det.min_happiness) return { m: 'amistad' };
  if (det.min_level) return {};                         // evo por nivel: lo cubre 'nivel'
  return { m: 'otro' };                                  // location/move/beauty/etc → solo caramelos
}

async function jget(url) {
  for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} }
  return null;
}
const idDe = (u) => Number(u.match(/\/(\d+)\/?$/)?.[1]);

// recorre el árbol de la chain; setea evos[] de cada nodo (id<=721) y la familia (raíz)
function recorrer(nodo, baseId, out) {
  const from = idDe(nodo.species.url);
  for (const sig of nodo.evolves_to) {
    const to = idDe(sig.species.url);
    const det = sig.evolution_details?.[0] || {};
    const nivel = det.min_level || NIVEL_NO_LEVEL;
    if (from <= N && to <= N) (out[from] ||= { evos: [], familia: baseId }).evos.push({ a: to, nivel, ...metodo(det) });
    recorrer(sig, baseId, out);
  }
  if (from <= N && !out[from]) out[from] = { evos: [], familia: baseId };
}

const out = {};
const chainCache = new Map();
const procesadas = new Set();   // cada cadena se recorre UNA sola vez (evita evos duplicados)
const ids = Array.from({ length: N }, (_, i) => i + 1);
for (let i = 0; i < ids.length; i += 20) {
  await Promise.all(ids.slice(i, i + 20).map(async (id) => {
    const spec = await jget(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
    const chainUrl = spec?.evolution_chain?.url;
    if (!chainUrl) { out[id] ||= { evos: [], familia: id }; return; }
    let chain = chainCache.get(chainUrl);
    if (!chain) { chain = await jget(chainUrl); chainCache.set(chainUrl, chain); }
    if (chain?.chain && !procesadas.has(chainUrl)) {
      procesadas.add(chainUrl);
      recorrer(chain.chain, idDe(chain.chain.species.url), out);
    }
  }));
  process.stdout.write('.');
}
for (const id of ids) out[id] ||= { evos: [], familia: id };
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`\n✓ evoluciones.json: ${Object.keys(out).length} (evos+nivel+familia)`);
