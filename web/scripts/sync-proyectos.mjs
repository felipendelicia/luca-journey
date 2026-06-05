// sync-proyectos.mjs — empaqueta web/src/proyectos/<slug>/ a web/src/data/proyectos.json.
// Cada proyecto = un líder de gimnasio (o integrador): pasos auto-corregidos + capstone.
// NO emite proyecto.py (solución de referencia). El test_proyecto.py se emite como 'test'.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', 'src', 'proyectos');
const OUT = path.resolve(HERE, '..', 'src', 'data', 'proyectos.json');
const out = {};
if (fs.existsSync(SRC)) {
  for (const slug of fs.readdirSync(SRC)) {
    const dir = path.join(SRC, slug);
    if (!fs.statSync(dir).isDirectory()) continue;
    const meta = JSON.parse(fs.readFileSync(path.join(dir, 'meta.json'), 'utf8'));
    const test = fs.existsSync(path.join(dir, 'test_proyecto.py'))
      ? fs.readFileSync(path.join(dir, 'test_proyecto.py'), 'utf8') : '';
    out[slug] = {
      slug, tipo: meta.tipo, tema: meta.tema || null, region: meta.region,
      titulo: meta.titulo, lider: meta.lider || '', premio: meta.premio || 0,
      intro: meta.intro || '', preamble: meta.preamble || '', packages: meta.packages || [],
      test, pasos: meta.pasos || [],
    };
  }
}
fs.mkdirSync(path.dirname(OUT), { recursive: true });
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`✓ proyectos.json: ${Object.keys(out).length} proyectos`);
