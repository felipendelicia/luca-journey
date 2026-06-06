// items.js — catálogo de la tienda (puro). El inventario vive en coleccion.js (col:items).
export const ITEMS = {
  piedra:      { nombre: 'Piedra Evolutiva', ico: '🪨', precio: 80, cat: 'evo',  desc: 'Evoluciona a los Pokémon que evolucionan por piedra (Eevee, Pikachu, Vulpix…). Se gasta 1 al evolucionar.' },
  pocion:      { nombre: 'Poción',           ico: '🧪', precio: 15, cat: 'cura', cura: 30,   desc: 'Cura 30 HP de tu Pokémon en batalla.' },
  superpocion: { nombre: 'Súper Poción',     ico: '⚗️', precio: 35, cat: 'cura', cura: 70,   desc: 'Cura 70 HP en batalla.' },
  pocionmax:   { nombre: 'Poción Máxima',    ico: '💉', precio: 70, cat: 'cura', cura: 9999, desc: 'Cura TODO el HP en batalla.' },
  superball:   { nombre: 'Super Ball',       ico: '🔵', precio: 25, cat: 'ball', tier: 1, desc: 'Mejor captura: +shiny, +nivel, +rareza y +caramelos (moderado).' },
  ultraball:   { nombre: 'Ultra Ball',       ico: '🟡', precio: 60, cat: 'ball', tier: 2, desc: 'Captura premium: ++shiny, ++nivel, ++rareza y ++caramelos.' },
};
// boosts de captura por tier de ball (0 = Pokéball normal).
export const BALL_BOOST = {
  0: { shiny: 1, nivelPct: 0,    rareza: 1,   caramelos: 3 },
  1: { shiny: 2, nivelPct: 0.20, rareza: 1.4, caramelos: 5 },
  2: { shiny: 4, nivelPct: 0.45, rareza: 2.0, caramelos: 8 },
};
export const itemsPorCat = (cat) => Object.entries(ITEMS).filter(([, it]) => it.cat === cat).map(([id, it]) => ({ id, ...it }));
