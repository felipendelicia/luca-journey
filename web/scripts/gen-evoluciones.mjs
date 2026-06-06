// gen-evoluciones.mjs — cadena evolutiva con datos REALES de PokeAPI.
// Salida: { "<id>": { evos:[{a:<evoId>, nivel:<min_level|30>}], familia:<idBase> } }
// 'nivel' = min_level del trigger level-up; si la evo NO es por nivel (piedra/trade/amistad),
// 'nivel' = 0 → en la app se evoluciona SOLO con caramelos (estilo GO). 'familia' = id base.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'evoluciones.json');
const N = 721, NIVEL_NO_LEVEL = 0;

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
    if (from <= N) (out[from] ||= { evos: [], familia: baseId }).evos.push({ a: to, nivel });
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
