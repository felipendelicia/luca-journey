// regiones.mjs — ÚNICA fuente de verdad de las regiones del curso (orden, nombre, emoji, tema).
// Antes esta lista estaba hardcodeada en liga, pokedex, safari, ejercicios, desafíos, perfiles…
// Ahora agregar una región nueva = agregar UNA entrada acá (+ su contenido en libro/ejercicios/
// proyectos y sus medallas en sprites.js/liga BADGES). Los IDs deben coincidir con el campo
// `region` de los temas (sync-ejercicios.mjs) y con la región de cada especie (pokemon.json).
export const REGIONES = [
  { id: 'kanto',  nombre: 'Kanto',  emoji: '🔴', tema: 'Fundamentos de Python' },
  { id: 'johto',  nombre: 'Johto',  emoji: '⚪', tema: 'Análisis de datos' },
  { id: 'hoenn',  nombre: 'Hoenn',  emoji: '🟢', tema: 'APIs con Flask' },
  { id: 'sinnoh', nombre: 'Sinnoh', emoji: '🔵', tema: 'Bases de datos' },
  { id: 'unova',  nombre: 'Unova',  emoji: '⚫', tema: 'Inteligencia Artificial' },
  { id: 'kalos',  nombre: 'Kalos',  emoji: '🟠', tema: 'Testing y calidad' },
  { id: 'alola',  nombre: 'Alola',  emoji: '🌺', tema: 'Automatizaciones' },
];

export const REGION_IDS = REGIONES.map((r) => r.id);
export const REGION_POR_ID = Object.fromEntries(REGIONES.map((r) => [r.id, r]));

// helpers de etiqueta (cada página elige el formato que necesita)
export const etiqueta = (r) => `${r.emoji} ${r.nombre}`;                 // "🔴 Kanto"
export const etiquetaTema = (r) => `${r.emoji} ${r.nombre} · ${r.tema}`; // "🔴 Kanto · Fundamentos de Python"
export const nombreDe = (id) => (REGION_POR_ID[id] ? REGION_POR_ID[id].nombre : id);
export const emojiDe = (id) => (REGION_POR_ID[id] ? REGION_POR_ID[id].emoji : '🔵');
