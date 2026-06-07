// gen-habilidades.mjs — baja habilidades (slots por especie + meta ES) y gender_rate de PokeAPI.
// Salida: web/src/data/habilidades.json. Correr: node scripts/gen-habilidades.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'habilidades.json');
const MAX = 1025;
const API = 'https://pokeapi.co/api/v2';

// set CURADO: key interno → {nombre, desc, efecto:true}. El resto se marca efecto:false.
const CURADAS = {
  intimidate:      { nombre: 'Intimidación', desc: 'Al entrar en combate baja el Ataque del rival.' },
  levitate:        { nombre: 'Levitación',   desc: 'Inmune a los movimientos de tipo Tierra.' },
  sturdy:          { nombre: 'Robustez',     desc: 'Soporta con 1 PS un golpe letal si tenía los PS al máximo.' },
  static:          { nombre: 'Estática',     desc: 'Puede paralizar al atacante al recibir un golpe de contacto.' },
  'flame-body':    { nombre: 'Cuerpo Llama', desc: 'Puede quemar al atacante al recibir un golpe de contacto.' },
  overgrow:        { nombre: 'Espesura',     desc: 'Potencia los movimientos de tipo Planta con pocos PS.' },
  blaze:           { nombre: 'Mar Llamas',   desc: 'Potencia los movimientos de tipo Fuego con pocos PS.' },
  torrent:         { nombre: 'Torrente',     desc: 'Potencia los movimientos de tipo Agua con pocos PS.' },
  guts:            { nombre: 'Agallas',      desc: 'Sube el Ataque si sufre un estado alterado.' },
  'water-absorb':  { nombre: 'Absorbe Agua', desc: 'Inmune a los movimientos de tipo Agua.' },
  'flash-fire':    { nombre: 'Absorbe Fuego', desc: 'Inmune a los movimientos de tipo Fuego.' },
  immunity:        { nombre: 'Inmunidad',    desc: 'No puede ser envenenado.' },
  insomnia:        { nombre: 'Insomnio',     desc: 'No puede quedarse dormido.' },
  'magma-armor':   { nombre: 'Armadura Magma', desc: 'No puede ser congelado.' },
  'compound-eyes': { nombre: 'Ojo Compuesto', desc: 'Aumenta la precisión de sus movimientos.' },
};

const get = async (u) => {
  for (let intento = 0; intento < 4; intento++) {
    try { const r = await fetch(u); if (r.ok) return r.json(); } catch (e) { /* reintenta */ }
    await new Promise((res) => setTimeout(res, 400 * (intento + 1)));
  }
  throw new Error('fallo ' + u);
};
const esES = (arr, key) => (arr.find((x) => x.language.name === 'es') || {})[key] || '';

const especies = {}, genero = {}, meta = {};
const abilityKeys = new Set();
for (let id = 1; id <= MAX; id++) {
  const p = await get(`${API}/pokemon/${id}`);
  especies[id] = p.abilities.map((a) => ({ key: a.ability.name, hidden: a.is_hidden }));
  p.abilities.forEach((a) => abilityKeys.add(a.ability.name));
  const sp = await get(`${API}/pokemon-species/${id}`);
  genero[id] = sp.gender_rate;            // -1 sin género, 0 siempre ♂, 8 siempre ♀, n = n/8 ♀
  if (id % 50 === 0) console.log('… especies', id);
}
let n = 0;
for (const key of abilityKeys) {
  if (CURADAS[key]) { meta[key] = { ...CURADAS[key], efecto: true }; continue; }
  const a = await get(`${API}/ability/${key}`);
  meta[key] = {
    nombre: esES(a.names, 'name') || key,
    desc: (esES(a.flavor_text_entries, 'flavor_text') || '').replace(/\s+/g, ' ').trim(),
    efecto: false,
  };
  if (++n % 30 === 0) console.log('… habilidades meta', n);
}
fs.writeFileSync(OUT, JSON.stringify({ especies, genero, meta }));
console.log('✓ habilidades.json', Object.keys(especies).length, 'especies,', Object.keys(meta).length, 'habilidades');
