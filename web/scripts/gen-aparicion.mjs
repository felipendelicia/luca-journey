// gen-aparicion.mjs — peso de APARICIÓN propio (criterio del juego, no el capture_rate).
// Más peso = aparece más seguido en el Safari. Se basa en la etapa evolutiva + rareza:
//   legendarios y pseudo-legendarios = rarísimos; bases = comunes; finales = raras.
// Usa src/data/evoluciones.json (sin red). Salida: src/data/aparicion.json { id: peso }.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const evo = JSON.parse(fs.readFileSync(path.resolve(HERE, '..', 'src', 'data', 'evoluciones.json')));

// Legendarios + míticos (gen 1-6)
const LEGENDARIOS = new Set([
  144, 145, 146, 150, 151,
  243, 244, 245, 249, 250, 251,
  377, 378, 379, 380, 381, 382, 383, 384, 385, 386,
  480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493,
  494, 638, 639, 640, 641, 642, 643, 644, 645, 646, 647, 648, 649,
  716, 717, 718, 719, 720, 721,
]);
// Pseudo-legendarios (finales con stats altísimas)
const PSEUDO = new Set([149, 248, 373, 376, 445, 635, 706]);
// Starters (formas base de cada región)
const STARTERS = new Set([1, 4, 7, 152, 155, 158, 252, 255, 258, 387, 390, 393, 495, 498, 501, 650, 653, 656]);

const evoluciona = new Set(Object.keys(evo).map(Number));        // tiene evolución (sale)
const esEvolucion = new Set();                                   // es resultado de evolución
for (const arr of Object.values(evo)) for (const t of arr) esEvolucion.add(t);

const peso = {};
for (let id = 1; id <= 721; id++) {
  const sale = evoluciona.has(id);
  const llega = esEvolucion.has(id);
  let w;
  if (LEGENDARIOS.has(id)) w = 4;          // legendario/mítico → rarísimo
  else if (PSEUDO.has(id)) w = 12;         // pseudo-legendario → muy raro
  else if (STARTERS.has(id)) w = 60;       // starter → especial
  else if (!llega && sale) w = 220;        // base de una línea → común
  else if (llega && sale) w = 75;          // intermedio
  else if (llega && !sale) w = 28;         // evolución final → rara
  else w = 110;                            // single-stage (no evoluciona ni es evolución)
  peso[id] = w;
}

fs.writeFileSync(path.resolve(HERE, '..', 'src', 'data', 'aparicion.json'), JSON.stringify(peso));
console.log(`✓ aparicion.json: ${Object.keys(peso).length} pesos`);
