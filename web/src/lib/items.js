// items.js — catálogo de la tienda (puro). El inventario vive en coleccion.js (col:items).
// Las piedras tipadas + el Disco de Enlace cubren las evos reales de evoluciones.json (campo `req`).
// El id legacy `piedra` (Piedra Evolutiva genérica) NO está en el catálogo: ya no se compra, pero
// sigue funcionando como comodín para cualquier evo por piedra (ver coleccion.js).
export const ITEMS = {
  // ── Evolución ── (piedras tipadas single-use: precio bajo; el Disco cubre 25 evos → un poco más)
  piedrafuego:  { nombre: 'Piedra Fuego',   ico: '🔥', precio: 40, cat: 'evo', sprite: 'piedrafuego',  desc: 'Evos de Fuego: Vulpix→Ninetales, Growlithe→Arcanine, Eevee→Flareon. Se gasta 1.' },
  piedraagua:   { nombre: 'Piedra Agua',    ico: '💧', precio: 40, cat: 'evo', sprite: 'piedraagua',   desc: 'Evos de Agua: Eevee→Vaporeon, Poliwhirl→Poliwrath, Shellder→Cloyster, Staryu→Starmie. Se gasta 1.' },
  piedratrueno: { nombre: 'Piedra Trueno',  ico: '⚡', precio: 40, cat: 'evo', sprite: 'piedratrueno', desc: 'Evos Eléctricas: Pikachu→Raichu, Eevee→Jolteon, Eelektrik→Eelektross. Se gasta 1.' },
  piedrahoja:   { nombre: 'Piedra Hoja',    ico: '🍃', precio: 40, cat: 'evo', sprite: 'piedrahoja',   desc: 'Evos de Planta: Gloom→Vileplume, Weepinbell→Victreebel, Exeggcute→Exeggutor. Se gasta 1.' },
  piedraluna:   { nombre: 'Piedra Lunar',   ico: '🌙', precio: 40, cat: 'evo', sprite: 'piedraluna',   desc: 'Clefairy→Clefable, Jigglypuff→Wigglytuff, Nidorina→Nidoqueen, Nidorino→Nidoking. Se gasta 1.' },
  piedrasol:    { nombre: 'Piedra Solar',   ico: '☀️', precio: 40, cat: 'evo', sprite: 'piedrasol',    desc: 'Gloom→Bellossom, Sunkern→Sunflora, Cottonee→Whimsicott, Petilil→Lilligant. Se gasta 1.' },
  piedradia:    { nombre: 'Piedra Día',     ico: '✨', precio: 40, cat: 'evo', sprite: 'piedradia',    desc: 'Togetic→Togekiss, Roselia→Roserade, Minccino→Cinccino, Floette→Florges. Se gasta 1.' },
  piedraalba:   { nombre: 'Piedra Alba',    ico: '🔆', precio: 40, cat: 'evo', sprite: 'piedraalba',   desc: 'Evos de día/macho: Kirlia→Gallade, Snorunt→Froslass. Se gasta 1.' },
  piedranoche:  { nombre: 'Piedra Noche',   ico: '🌑', precio: 40, cat: 'evo', sprite: 'piedranoche',  desc: 'Murkrow→Honchkrow, Misdreavus→Mismagius, Lampent→Chandelure, Doublade→Aegislash. Se gasta 1.' },
  discoenlace:  { nombre: 'Disco de Enlace', ico: '🔗', precio: 50, cat: 'evo', sprite: 'discoenlace',  desc: 'Para evos por intercambio: Kadabra→Alakazam, Machoke→Machamp, Graveler→Golem, Haunter→Gengar. Se gasta 1.' },
  // ── Curación · batalla ── (botella spray, color por potencia)
  pocion:      { nombre: 'Poción',           sprite: 'pocion',      precio: 15, cat: 'cura', cura: 30,   desc: 'Cura 30 HP de tu Pokémon en batalla.' },
  superpocion: { nombre: 'Súper Poción',     sprite: 'superpocion', precio: 35, cat: 'cura', cura: 70,   desc: 'Cura 70 HP en batalla.' },
  pocionmax:   { nombre: 'Poción Máxima',    sprite: 'pocionmax',   precio: 70, cat: 'cura', cura: 9999, desc: 'Cura TODO el HP en batalla.' },
  // ── Estados y revivir · batalla ── (vial color por estado; Revivir = cruz)
  antidoto:      { nombre: 'Antídoto',       sprite: 'antidoto',      precio: 18, cat: 'estado', curaEstado: 'veneno',    desc: 'Cura el Envenenamiento en batalla.' },
  antiquemar:    { nombre: 'Antiquemar',     sprite: 'antiquemar',    precio: 18, cat: 'estado', curaEstado: 'quemadura', desc: 'Cura la Quemadura en batalla.' },
  antiparalisis: { nombre: 'Antiparálisis',  sprite: 'antiparalisis', precio: 18, cat: 'estado', curaEstado: 'paralisis', desc: 'Cura la Parálisis en batalla.' },
  despertar:     { nombre: 'Despertar',      sprite: 'despertar',     precio: 18, cat: 'estado', curaEstado: 'sueno',     desc: 'Despierta a un Pokémon Dormido en batalla.' },
  antihielo:     { nombre: 'Antihielo',      sprite: 'antihielo',     precio: 18, cat: 'estado', curaEstado: 'congelado', desc: 'Descongela a un Pokémon Congelado en batalla.' },
  curatotal:     { nombre: 'Cura Total',     sprite: 'curatotal',     precio: 45, cat: 'estado', curaEstado: 'todos',     desc: 'Cura CUALQUIER estado alterado (incluida la confusión).' },
  revivir:       { nombre: 'Revivir',        sprite: 'revivir',       precio: 55, cat: 'estado', revive: 0.5,             desc: 'Revive a un Pokémon debilitado con la mitad del HP.' },
  // ── Pokeballs ──
  superball:   { nombre: 'Super Ball',       ico: '🔵', precio: 25, cat: 'ball', tier: 1, sprite: 'ball1', desc: 'Mejor captura: +shiny, +nivel, +rareza y +caramelos (moderado).' },
  ultraball:   { nombre: 'Ultra Ball',       ico: '🟡', precio: 60, cat: 'ball', tier: 2, sprite: 'ball2', desc: 'Captura premium: ++shiny, ++nivel, ++rareza y ++caramelos.' },
};
// boosts de captura por tier de ball (0 = Pokéball normal).
export const BALL_BOOST = {
  0: { shiny: 1, nivelPct: 0,    rareza: 1,   caramelos: 3 },
  1: { shiny: 2, nivelPct: 0.20, rareza: 1.4, caramelos: 5 },
  2: { shiny: 4, nivelPct: 0.45, rareza: 2.0, caramelos: 8 },
};
export const itemsPorCat = (cat) => Object.entries(ITEMS).filter(([, it]) => it.cat === cat).map(([id, it]) => ({ id, ...it }));
