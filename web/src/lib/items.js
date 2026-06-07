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
  // ── Vitaminas · entrenamiento (EV) ── (ev = índice de stat: 0=PS,1=Atk,2=Def,3=SpA,4=SpD,5=Vel)
  proteina: { nombre: 'Proteína', sprite: 'vitamina', precio: 30, cat: 'ev', ev: 1, evMax: 100, desc: '+10 EV de Ataque (hasta 100 por esta vía).' },
  hierro:   { nombre: 'Hierro',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 2, evMax: 100, desc: '+10 EV de Defensa (hasta 100).' },
  calcio:   { nombre: 'Calcio',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 3, evMax: 100, desc: '+10 EV de Ataque Especial (hasta 100).' },
  zinc:     { nombre: 'Zinc',     sprite: 'vitamina', precio: 30, cat: 'ev', ev: 4, evMax: 100, desc: '+10 EV de Defensa Especial (hasta 100).' },
  carburo:  { nombre: 'Carburo',  sprite: 'vitamina', precio: 30, cat: 'ev', ev: 5, evMax: 100, desc: '+10 EV de Velocidad (hasta 100).' },
  masps:    { nombre: 'Más PS',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 0, evMax: 100, desc: '+10 EV de PS (hasta 100).' },
  // ── Pokeballs ── (la captura depende de `catch`/condición; ver safari-core.catchBall)
  pokeball:   { nombre: 'Poké Ball',  sprite: 'ball0', cat: 'ball', tier: 0, catch: 1,   noVenta: true, desc: 'La de siempre. Se gana resolviendo ejercicios. Captura estándar.' },
  superball:  { nombre: 'Super Ball', sprite: 'ball1', cat: 'ball', tier: 1, catch: 1.5, precio: 25, desc: 'Captura mejorada (×1.5). Para los que zafan un poco.' },
  ultraball:  { nombre: 'Ultra Ball', sprite: 'ball2', cat: 'ball', tier: 2, catch: 2,   precio: 60, desc: 'Captura premium (×2). Para los raros.' },
  veloz:      { nombre: 'Ball Veloz',      sprite: 'ballveloz',   cat: 'ball', cond: 'veloz',      precio: 25, desc: '×4 de captura si la tirás apenas aparece (primer tiro).' },
  turno:      { nombre: 'Ball Turno',      sprite: 'ballturno',   cat: 'ball', cond: 'turno',      precio: 25, desc: 'Mejora cuantos más tiros llevás en el encuentro.' },
  red:        { nombre: 'Ball Red',        sprite: 'ballred',     cat: 'ball', cond: 'red',        precio: 30, desc: '×3 de captura contra Pokémon de tipo Bicho o Agua.' },
  repeticion: { nombre: 'Ball Repetición', sprite: 'ballrepe',    cat: 'ball', cond: 'repeticion', precio: 30, desc: '×3 si ya tenés esa especie en la Pokédex.' },
  master:     { nombre: 'Master Ball',     sprite: 'ballmaster',  cat: 'ball', catch: 'master',    precio: 5000, desc: 'Captura 100% garantizada. Carísima: guardala para EL Pokémon.' },
  xeneize:    { nombre: 'Ball Xeneize',    sprite: 'ballxeneize', cat: 'ball', catch: 2, boca: true, precio: 80, desc: '💙💛 Edición Boca. Captura premium (×2) + festejo azul y oro al atrapar.' },
};
export const itemsPorCat = (cat) => Object.entries(ITEMS).filter(([, it]) => it.cat === cat).map(([id, it]) => ({ id, ...it }));
