// sync-ejercicios.mjs — empaqueta los ejercicios (web/src/ejercicios/<slug>/) a
// web/src/data/ejercicios.json, para corregirlos en el navegador (Pyodide).
// La fuente ahora vive en el propio proyecto web (web/src/ejercicios/).

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', 'src', 'ejercicios');
const OUT = path.resolve(HERE, '..', 'src', 'data');
fs.mkdirSync(OUT, { recursive: true });

// slug -> título y orden
const SEMANAS = [
  ['python-introduccion', 'Python: Introducción'],
  ['control-de-flujo', 'Control de Flujo'],
  ['funciones', 'Funciones'],
  ['listas-y-colecciones', 'Listas y Colecciones'],
  ['cadenas-y-archivos', 'Cadenas y Archivos'],
  ['poo-introduccion', 'POO: Introducción'],
  ['poo-avanzado', 'POO: Avanzado'],
  ['modulos-y-pip', 'Módulos y pip'],
];

const IGNORAR = new Set(['ejercicios.py', 'soluciones.py', 'test_ejercicios.py']);
const leer = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf-8') : null);

const data = [];
SEMANAS.forEach(([slug, titulo], i) => {
  const base = path.join(SRC, slug);
  const ejercicios = leer(path.join(base, 'ejercicios.py'));
  const test = leer(path.join(base, 'test_ejercicios.py'));
  const solucion = leer(path.join(base, 'soluciones.py'));
  if (!ejercicios || !test) { console.warn('faltan archivos en', slug); return; }

  const extra = {};
  for (const f of fs.readdirSync(base)) {
    if (f.endsWith('.py') && !IGNORAR.has(f)) extra[f] = leer(path.join(base, f));
  }
  data.push({ slug, titulo, orden: i, ejercicios, test, solucion, extra });
  console.log(`✓ ${slug}`);
});

fs.writeFileSync(path.join(OUT, 'ejercicios.json'), JSON.stringify(data));
console.log(`ejercicios.json: ${data.length} semanas`);
