// sync-ejercicios.mjs — empaqueta los ejercicios (web/src/ejercicios/<slug>/) a
// web/src/data/ejercicios.json, DIVIDIDOS por función/clase, con sus tests.
// Cada semana = { preamble, test, solucion, extra, ejercicios:[{id,titulo,prompt,starter,tests}] }

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SRC = path.resolve(HERE, '..', 'src', 'ejercicios');
const OUT = path.resolve(HERE, '..', 'src', 'data');
fs.mkdirSync(OUT, { recursive: true });

// [slug, título, region]
const SEMANAS = [
  ['python-introduccion', 'Python: Introducción', 'kanto'],
  ['control-de-flujo', 'Control de Flujo', 'kanto'],
  ['funciones', 'Funciones', 'kanto'],
  ['listas-y-colecciones', 'Listas y Colecciones', 'kanto'],
  ['cadenas-y-archivos', 'Cadenas y Archivos', 'kanto'],
  ['poo-introduccion', 'POO: Introducción', 'kanto'],
  ['poo-avanzado', 'POO: Avanzado', 'kanto'],
  ['modulos-y-pip', 'Módulos y pip', 'kanto'],
  // Johto — análisis de datos
  ['numpy-arrays', 'NumPy: Arrays', 'johto'],
  ['numpy-calculo', 'NumPy: Cálculo numérico', 'johto'],
  ['pandas-series-dataframe', 'pandas: Series y DataFrame', 'johto'],
  ['pandas-seleccion', 'pandas: Selección y filtrado', 'johto'],
  ['pandas-limpieza', 'pandas: Limpieza de datos', 'johto'],
  ['pandas-groupby', 'pandas: Agrupar y combinar', 'johto'],
  ['matplotlib', 'matplotlib: Gráficos', 'johto'],
  ['analisis-integrador', 'Análisis integrador', 'johto'],
];
const IGNORAR = new Set(['ejercicios.py', 'soluciones.py', 'test_ejercicios.py']);
const leer = (p) => (fs.existsSync(p) ? fs.readFileSync(p, 'utf-8') : null);

// Paquetes de Pyodide que hay que cargar según lo que importe el código.
function paquetesDe(textos) {
  const todo = textos.join('\n');
  const pk = [];
  if (/\b(import numpy|from numpy)\b/.test(todo) || /\bnp\./.test(todo)) pk.push('numpy');
  if (/\b(import pandas|from pandas)\b/.test(todo) || /\bpd\./.test(todo)) pk.push('pandas');
  if (/\b(import matplotlib|from matplotlib|matplotlib\.pyplot)\b/.test(todo) || /\bplt\./.test(todo)) pk.push('matplotlib');
  return pk;
}

// Divide el ejercicios.py en preamble + bloques (cada def/class top-level con su comentario)
function dividir(src) {
  const lines = src.split('\n');
  const esBlanca = (l) => l.trim() === '';
  const esCabecera = (l) => /^#/.test(l) || /^@/.test(l) || esBlanca(l);
  // anclas = def/class top-level
  const anclas = [];
  for (let i = 0; i < lines.length; i++) {
    if (/^(def |class )/.test(lines[i])) anclas.push(i);
  }
  if (!anclas.length) return { preamble: src, ejercicios: [] };

  // inicio del bloque de cada ancla (subo sobre comentarios/decoradores/blancos)
  const inicios = anclas.map((a) => {
    let s = a;
    while (s - 1 >= 0 && esCabecera(lines[s - 1])) s--;
    return s;
  });

  const preamble = lines.slice(0, inicios[0]).join('\n').trim();
  const ejercicios = [];
  for (let k = 0; k < anclas.length; k++) {
    const ini = inicios[k];
    const fin = k + 1 < anclas.length ? inicios[k + 1] : lines.length;
    const ancla = anclas[k];
    // líneas de comentario, sin el '#' y sin separadores tipo '-----' o '====='
    const lc = lines.slice(ini, ancla)
      .filter((l) => /^#/.test(l))
      .map((l) => l.replace(/^#\s?/, '').replace(/\s+$/, ''))
      .filter((l) => !/^[-=~*_·.]{3,}$/.test(l));
    const comentario = lc.join('\n').trim();
    const m = lines[ancla].match(/^(?:def|class)\s+([A-Za-z_]\w*)/);
    const name = m ? m[1] : 'ej' + k;
    const starter = lines.slice(ancla, fin).join('\n').replace(/\s+$/, '') + '\n';
    let titulo = (lc.find((l) => l.trim()) || name).trim();
    if (titulo.length > 90) titulo = titulo.slice(0, 88) + '…';
    ejercicios.push({ id: name, name, titulo, prompt: comentario, starter, tests: [] });
  }
  return { preamble, ejercicios };
}

// Mapea cada test_* a los ejercicios cuyos símbolos usa (modulo.<name>)
function mapearTests(testSrc, ejercicios) {
  const lines = testSrc.split('\n');
  const idx = [];
  for (let i = 0; i < lines.length; i++) if (/^def (test_\w+)/.test(lines[i])) idx.push(i);
  const porNombre = new Map(ejercicios.map((e) => [e.name, e]));
  for (let k = 0; k < idx.length; k++) {
    const ini = idx[k], fin = k + 1 < idx.length ? idx[k + 1] : lines.length;
    const nombre = lines[ini].match(/^def (test_\w+)/)[1];
    const cuerpo = lines.slice(ini, fin).join('\n');
    const usados = new Set([...cuerpo.matchAll(/modulo\.([A-Za-z_]\w*)/g)].map((m) => m[1]));
    let asignado = false;
    for (const u of usados) {
      if (porNombre.has(u)) { porNombre.get(u).tests.push(nombre); asignado = true; }
    }
    // si no matchea símbolo, lo dejamos en el primer ejercicio cuyo nombre aparezca en el test
    if (!asignado && ejercicios.length) {
      const e = ejercicios.find((e) => nombre.includes(e.name)) || ejercicios[0];
      e.tests.push(nombre);
    }
  }
}

const data = [];
SEMANAS.forEach(([slug, titulo, region], i) => {
  const base = path.join(SRC, slug);
  const ejSrc = leer(path.join(base, 'ejercicios.py'));
  const test = leer(path.join(base, 'test_ejercicios.py'));
  const solucion = leer(path.join(base, 'soluciones.py'));
  if (!ejSrc || !test) { console.warn('(falta, lo salto)', slug); return; }

  const extra = {};
  for (const f of fs.readdirSync(base)) {
    if (f.endsWith('.py') && !IGNORAR.has(f)) extra[f] = leer(path.join(base, f));
  }
  const { preamble, ejercicios } = dividir(ejSrc);
  mapearTests(test, ejercicios);
  // solución por ejercicio (dividimos soluciones.py igual y mapeamos por nombre)
  if (solucion) {
    const sol = dividir(solucion);
    const solMap = new Map(sol.ejercicios.map((e) => [e.name, e.starter]));
    ejercicios.forEach((e) => { e.solucion = solMap.get(e.name) || ''; });
  }
  const packages = paquetesDe([ejSrc, test, solucion || '', ...Object.values(extra)]);
  const conTests = ejercicios.filter((e) => e.tests.length).length;
  data.push({ slug, titulo, region: region || 'kanto', packages, orden: i, preamble, test, solucion, extra, ejercicios });
  console.log(`✓ ${slug.padEnd(24)} [${region}] ${ejercicios.length} ej (${conTests} c/test)${packages.length ? ' pkg:' + packages.join(',') : ''}`);
});

fs.writeFileSync(path.join(OUT, 'ejercicios.json'), JSON.stringify(data));
console.log(`ejercicios.json: ${data.length} semanas`);
