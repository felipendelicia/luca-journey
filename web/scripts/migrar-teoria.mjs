// migrar-teoria.mjs — ONE-SHOT: trae la teoría existente (curso/*/teoria.md) a
// las content collections de Astro (web/src/content/libro/*.md).
//
// Después de esto, el contenido se mantiene ACÁ (en web/src/content/libro/),
// y los teoria.md de curso/ quedan obsoletos. Este script se corre una sola vez.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '..', '..');
const OUT = path.resolve(HERE, '..', 'src', 'content', 'libro');
fs.mkdirSync(OUT, { recursive: true });

// orden, slug-de-archivo, ruta de la teoría original
const CAPS = [
  [10, 'linux-fundamentos', 'curso/semana-01-linux-fundamentos/teoria.md'],
  [20, 'linux-intermedio', 'curso/semana-02-linux-intermedio/teoria.md'],
  [30, 'python-introduccion', 'curso/semana-03-python-introduccion/teoria.md'],
  [40, 'control-de-flujo', 'curso/semana-04-python-control-de-flujo/teoria.md'],
  [50, 'funciones', 'curso/semana-05-python-funciones/teoria.md'],
  [60, 'listas-y-colecciones', 'curso/semana-06-python-listas-y-colecciones/teoria.md'],
  [70, 'cadenas-y-archivos', 'curso/semana-07-python-cadenas-y-archivos/teoria.md'],
  [75, 'git', 'curso/semana-git-control-de-versiones/teoria.md'],
  [80, 'poo-introduccion', 'curso/semana-08-python-poo-introduccion/teoria.md'],
  [90, 'poo-avanzado', 'curso/semana-09-python-poo-avanzado/teoria.md'],
  [95, 'modulos-y-pip', 'curso/semana-10-python-modulos-y-pip/teoria.md'],
];

function titulo(md) {
  const m = md.match(/^#\s+(.*)$/m);
  if (!m) return 'Capítulo';
  let t = m[1].trim();
  if (t.includes(' — ')) t = t.split(' — ').pop().trim();
  // sacamos emoji inicial
  return t.replace(/^[^\p{L}\p{N}]+/u, '').trim();
}

for (const [order, slug, rel] of CAPS) {
  const src = path.join(REPO, rel);
  if (!fs.existsSync(src)) { console.warn('falta', rel); continue; }
  let md = fs.readFileSync(src, 'utf-8');
  const t = titulo(md);
  // sacamos la primera línea h1 (el título va en el frontmatter)
  md = md.replace(/^#\s+.*$/m, '').replace(/^\s+/, '');
  const front = `---\ntitle: ${JSON.stringify(t)}\norder: ${order}\n---\n\n`;
  fs.writeFileSync(path.join(OUT, `${order}-${slug}.md`), front + md);
  console.log(`✓ ${order}-${slug}.md  («${t}»)`);
}
console.log('Migración lista. A partir de ahora, editá el contenido en web/src/content/libro/');
