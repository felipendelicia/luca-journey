// fix-learnsets.mjs — corrige los niveles del learnset usando la LÍNEA EVOLUTIVA.
// PokeAPI vuelca muchos moves a "nivel 1" en formas evolucionadas (los que sabe al evolucionar),
// lo que dejaría que un Charizard nivel 1 use moves fuertes. Solución: el nivel efectivo de un move
// para una especie = min sobre su cadena (base→…→especie) de max(nivelAprende, nivelEntrada), donde
// nivelEntrada = el nivel al que aparece esa etapa (1 para la base; nivel de evolución para las demás).
// Así los moves "volcados a 1" del evolucionado pasan a su nivel de evolución. Puro: lee/escribe JSON.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DATA = path.resolve(HERE, '..', 'src', 'data');
const learnsets = JSON.parse(fs.readFileSync(path.join(DATA, 'learnsets.json'), 'utf8'));
const evo = JSON.parse(fs.readFileSync(path.join(DATA, 'evoluciones.json'), 'utf8'));

const NIVEL_STONE = 20;
const preEvo = {}; // evoId -> { from, nivel }
for (const from in evo) for (const e of (evo[from].evos || [])) preEvo[e.a] = { from: Number(from), nivel: e.nivel };

const cadena = (id) => { const c = [id]; let cur = id; while (preEvo[cur]) { cur = preEvo[cur].from; c.unshift(cur); } return c; };
const nivelEntrada = (id) => { const p = preEvo[id]; if (!p) return 1; return p.nivel > 0 ? p.nivel : NIVEL_STONE; };

const out = {};
for (const sid in learnsets) {
  const id = Number(sid);
  const acc = {};
  for (const sp of cadena(id)) {
    const E = nivelEntrada(sp);
    for (const { m, n } of (learnsets[sp] || [])) {
      const eff = Math.max(n, E);
      if (acc[m] == null || eff < acc[m]) acc[m] = eff;
    }
  }
  out[id] = Object.entries(acc).map(([m, n]) => ({ m: Number(m), n })).sort((a, b) => a.n - b.n || a.m - b.m);
}
fs.writeFileSync(path.join(DATA, 'learnsets.json'), JSON.stringify(out));
console.log(`✓ learnsets.json recalculado por línea evolutiva: ${Object.keys(out).length} especies`);
