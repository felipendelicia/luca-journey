// coleccion.js — sistema de colección de Pokémon (todo en localStorage).
// Aprender = atrapar: cada ejercicio resuelto da Pokéballs; completar un tema o
// una región te da capturas garantizadas. Se pueden tener REPETIDOS (conteo por id).

const get = (k, def) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? def; } catch { return def; } };
const set = (k, v) => localStorage.setItem(k, JSON.stringify(v));

export const BALLS_POR_EJERCICIO = 2;
export const REGALO_DIARIO = 5;
export const PROB_SHINY = 0.01; // 1% de que un salvaje sea shiny ✨
export const COSTO_EVOLUCION = 3; // cuántos repetidos consume evolucionar

// Pokémon insignia de cada tema (id de la PokéAPI).
export const INSIGNIAS = {
  'python-introduccion': 25, 'control-de-flujo': 4, 'funciones': 68,
  'listas-y-colecciones': 103, 'cadenas-y-archivos': 65, 'poo-introduccion': 132,
  'poo-avanzado': 149, 'modulos-y-pip': 137,
  'numpy-arrays': 201, 'numpy-calculo': 196, 'pandas-series-dataframe': 175,
  'pandas-seleccion': 215, 'pandas-limpieza': 194, 'pandas-groupby': 181,
  'matplotlib': 197, 'analisis-integrador': 248,
  'api-http-json': 252, 'flask-primera-app': 255, 'flask-json': 258,
  'flask-parametros': 280, 'flask-post': 304, 'flask-rest-crud': 376,
  'consumir-api': 351, 'pokedex-api': 373,
  'sql-intro': 81, 'sql-crear': 100, 'sql-select': 82, 'sql-agregaciones': 101,
  'sql-update-delete': 125, 'sql-join': 233, 'sqlite-python': 239, 'proyecto-db': 243,
};
export const LEGENDARIOS = { kanto: 150, johto: 249, hoenn: 384, sinnoh: 251 };

export const spriteUrl = (id, shiny = false) =>
  `https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${shiny ? 'shiny/' : ''}${id}.png`;

const ejDone = (slug, exId) => localStorage.getItem(`ej:${slug}:${exId}:ok`) === '1';

// atrapados = { id: cantidad }  (se permiten repetidos)
export function estado() {
  const at = get('col:atrapados', {});
  return {
    balls: get('col:balls', 0),
    atrapados: at,
    unicos: Object.keys(at).length,
    total: Object.values(at).reduce((a, b) => a + b, 0),
    shiny: new Set(get('col:shiny', [])),
  };
}

export function regionesDesbloqueadas(temas) {
  const r = new Set(['kanto']);
  for (const t of temas) if (t.ejercicios.some((ex) => ejDone(t.slug, ex.id))) r.add(t.region);
  return r;
}

// Otorga lo pendiente (idempotente). Devuelve {balls, capturas:[id...]} de lo NUEVO.
export function sincronizar(temas) {
  let balls = get('col:balls', 0);
  const ganados = new Set(get('col:ganados', []));
  const hitos = new Set(get('col:hitos', []));
  const at = get('col:atrapados', {});
  const nuevo = { balls: 0, capturas: [] };

  const capturar = (id) => { if (id) { at[id] = (at[id] || 0) + 1; nuevo.capturas.push(id); } };

  for (const t of temas) {
    let hechos = 0;
    for (const ex of t.ejercicios) {
      if (ejDone(t.slug, ex.id)) {
        hechos++;
        const gk = `${t.slug}:${ex.id}`;
        if (!ganados.has(gk)) { ganados.add(gk); balls += BALLS_POR_EJERCICIO; nuevo.balls += BALLS_POR_EJERCICIO; }
      }
    }
    if (t.ejercicios.length && hechos === t.ejercicios.length) {
      const hk = `tema:${t.slug}`;
      if (!hitos.has(hk)) { hitos.add(hk); capturar(INSIGNIAS[t.slug]); }
    }
  }
  const porReg = {};
  for (const t of temas) (porReg[t.region] ||= []).push(t);
  for (const [region, ts] of Object.entries(porReg)) {
    const completa = ts.every((t) => t.ejercicios.length && t.ejercicios.every((ex) => ejDone(t.slug, ex.id)));
    if (completa) {
      const hk = `region:${region}`;
      if (!hitos.has(hk)) { hitos.add(hk); capturar(LEGENDARIOS[region]); }
    }
  }

  set('col:balls', balls);
  set('col:ganados', [...ganados]);
  set('col:hitos', [...hitos]);
  set('col:atrapados', at);
  return nuevo;
}

// ¿Qué Pokémon podés evolucionar? (tenés COSTO_EVOLUCION o más y existe evolución).
export function evolucionesPosibles(evoMap) {
  const at = get('col:atrapados', {});
  const res = [];
  for (const [id, n] of Object.entries(at)) {
    if (n >= COSTO_EVOLUCION && evoMap[id]) res.push({ from: Number(id), cantidad: n, opciones: evoMap[id] });
  }
  return res;
}

// Evoluciona: consume COSTO_EVOLUCION del 'from' y suma 1 del 'to'.
export function evolucionar(fromId, toId, evoMap) {
  const at = get('col:atrapados', {});
  if ((at[fromId] || 0) < COSTO_EVOLUCION || !(evoMap[fromId] || []).includes(toId)) return false;
  at[fromId] -= COSTO_EVOLUCION;
  if (at[fromId] <= 0) delete at[fromId];
  at[toId] = (at[toId] || 0) + 1;
  set('col:atrapados', at);
  return true;
}

// Regalo diario: +5 Pokéballs una vez por día.
export function reclamarRegalo() {
  const hoy = new Date().toISOString().slice(0, 10);
  if (localStorage.getItem('col:regalo') === hoy) return 0;
  localStorage.setItem('col:regalo', hoy);
  set('col:balls', get('col:balls', 0) + REGALO_DIARIO);
  return REGALO_DIARIO;
}
export function regaloDisponible() {
  return localStorage.getItem('col:regalo') !== new Date().toISOString().slice(0, 10);
}

// Tirá una Pokéball: atrapás un salvaje al azar de las regiones desbloqueadas.
// Se permiten REPETIDOS, así que siempre hay algo para atrapar.
export function tirar(pokemon, temas) {
  let balls = get('col:balls', 0);
  if (balls <= 0) return { error: 'sin-balls' };
  // salvajes solo de las regiones desbloqueadas (hacés ejercicios de una región
  // para que aparezcan sus Pokémon). Se permiten repetidos.
  const regiones = regionesDesbloqueadas(temas);
  const pool = pokemon.filter((p) => regiones.has(p.region));
  if (!pool.length) return { error: 'vacio' };
  const elegido = pool[Math.floor(Math.random() * pool.length)];
  const at = get('col:atrapados', {});
  at[elegido.id] = (at[elegido.id] || 0) + 1;
  balls--;
  // shiny: 1% de las veces; se guarda aparte (podés tener el shiny de un Pokémon)
  const shiny = Math.random() < PROB_SHINY;
  let nuevoShiny = false;
  if (shiny) {
    const s = get('col:shiny', []);
    if (!s.includes(elegido.id)) { s.push(elegido.id); set('col:shiny', s); nuevoShiny = true; }
  }
  set('col:balls', balls);
  set('col:atrapados', at);
  return { pokemon: elegido, cantidad: at[elegido.id], repetido: at[elegido.id] > 1, shiny, nuevoShiny, balls };
}
