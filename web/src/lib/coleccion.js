// coleccion.js — sistema de colección de Pokémon (todo en localStorage).
// Aprender = atrapar: cada ejercicio resuelto da Pokéballs; completar un tema o
// una región te da capturas garantizadas. Se pueden tener REPETIDOS (conteo por id).

import { tierDe } from './rareza.js';
import evoData from '../data/evoluciones.json' with { type: 'json' };
import { migrarPC } from './migracion-pc.js';

// corre la migración a v2 (conteos→instancias) una vez, antes de tocar el PC.
let _migrado = false;
function asegurarMigrado() { if (!_migrado) { _migrado = true; try { migrarPC(); } catch {} } }

const get = (k, def) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? def; } catch { return def; } };
const set = (k, v) => localStorage.setItem(k, JSON.stringify(v));

// ───────── Colección v2 (instancias estilo GO) ─────────
// col:pc = [{iid,id,nivel,exp,shiny,movs,creado}] (fuente de verdad). Se derivan
// col:atrapados/col:shiny para compatibilidad con el código viejo (intercambios, perfil, logros).
const familiaDe = (id) => (evoData[id] && evoData[id].familia) || Number(id);
const _uid = () => Math.random().toString(36).slice(2, 10);

export const pc = () => { asegurarMigrado(); return get('col:pc', []); };              // instancias
export const caramelos = () => { asegurarMigrado(); return get('col:caramelos', {}); }; // {familiaId: cantidad}
export const vistos = () => { asegurarMigrado(); return new Set(get('col:vistos', [])); };

// deriva col:atrapados (conteos) y col:shiny (especies) desde el PC → compat.
export function derivarCompat(arr = pc()) {
  const at = {}, shi = new Set();
  for (const m of arr) { at[m.id] = (at[m.id] || 0) + 1; if (m.shiny) shi.add(m.id); }
  set('col:atrapados', at);
  set('col:shiny', [...shi]);
}
function setPC(arr) { set('col:pc', arr); derivarCompat(arr); }
function addVisto(id) { const v = get('col:vistos', []); if (!v.includes(Number(id))) { v.push(Number(id)); set('col:vistos', v); } }
function addCaramelos(id, n) { const c = get('col:caramelos', {}); const f = familiaDe(id); c[f] = (c[f] || 0) + n; set('col:caramelos', c); }

export const CARAMELOS_POR_CAPTURA = 3;
// crea una instancia nueva (al atrapar) + suma a vistos + caramelos a la familia. Devuelve la instancia.
export function atrapar(id, { shiny = false } = {}) {
  id = Number(id);
  const inst = { iid: _uid(), id, nivel: 1, exp: 0, shiny, movs: [], creado: Date.now() };
  const arr = pc(); arr.push(inst); setPC(arr);
  addVisto(id); addCaramelos(id, CARAMELOS_POR_CAPTURA);
  return inst;
}

export const BALLS_POR_EJERCICIO = 2;
export const REGALO_BALLS = 5;                     // Pokéballs por regalo
export const REGALO_COOLDOWN_MS = 20 * 60 * 1000;  // cada 20 minutos
export const PROB_SHINY = 0.01; // 1% de que un salvaje sea shiny ✨
export const COSTO_EVOLUCION = 3; // cuántos hacen falta para evolucionar (te queda 1 del pre-evolucionado)

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
  'sql-intro': 387, 'sql-crear': 390, 'sql-select': 393, 'sql-agregaciones': 403,
  'sql-update-delete': 417, 'sql-join': 462, 'sqlite-python': 474, 'proyecto-db': 466,
  'ia-intro': 495, 'ia-datos': 498, 'ia-clasificacion': 501, 'ia-evaluacion': 522,
  'ia-regresion': 587, 'ia-arboles': 599, 'ia-clustering': 602, 'ia-proyecto': 637,
  'errores-try-except': 650, 'raise-validar': 653, 'excepciones-propias': 656, 'assert-afirmaciones': 659,
  'primer-test': 667, 'casos-limite': 677, 'tdd': 696, 'proyecto-testing': 714,
};
export const LEGENDARIOS = { kanto: 150, johto: 249, hoenn: 384, sinnoh: 483, unova: 643, kalos: 716 };

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
  const nuevo = { balls: 0, capturas: [] };

  const capturar = (id) => { if (id) { atrapar(id); nuevo.capturas.push(id); } };
  const proyOk = (k) => localStorage.getItem('proy:' + k + ':ok') === '1';

  for (const t of temas) {
    let hechos = 0;
    for (const ex of t.ejercicios) {
      if (ejDone(t.slug, ex.id)) {
        hechos++;
        const gk = `${t.slug}:${ex.id}`;
        if (!ganados.has(gk)) { ganados.add(gk); balls += BALLS_POR_EJERCICIO; nuevo.balls += BALLS_POR_EJERCICIO; }
      }
    }
    if (t.ejercicios.length && hechos === t.ejercicios.length && (proyOk(t.slug) || hitos.has(`tema:${t.slug}`))) {
      const hk = `tema:${t.slug}`;
      if (!hitos.has(hk)) { hitos.add(hk); capturar(INSIGNIAS[t.slug]); }
    }
  }
  const porReg = {};
  for (const t of temas) (porReg[t.region] ||= []).push(t);
  for (const [region, ts] of Object.entries(porReg)) {
    const completa = ts.every((t) => t.ejercicios.length && t.ejercicios.every((ex) => ejDone(t.slug, ex.id)));
    if (completa && (proyOk(region + '-integrador') || hitos.has(`region:${region}`))) {
      const hk = `region:${region}`;
      if (!hitos.has(hk)) { hitos.add(hk); capturar(LEGENDARIOS[region]); }
    }
  }

  set('col:balls', balls);
  set('col:ganados', [...ganados]);
  set('col:hitos', [...hitos]);
  return nuevo;
}

// ───────── niveles + evolución (v2) ─────────
export const NIVEL_MAX = 50;
export const costoSubir = (nivel) => 1 + Math.floor(nivel / 8);   // caramelos para nivel→nivel+1
const costoEvo = (nivelReq) => (nivelReq > 0 ? 25 : 50);          // por nivel: 25; piedra/etc (GO): 50
const buscarInst = (arr, iid) => arr.find((m) => m.iid === iid);

// Power-Up: gasta caramelos de la familia y sube 1 nivel. true si pudo.
export function subirNivel(iid) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m || m.nivel >= NIVEL_MAX) return false;
  const c = get('col:caramelos', {}); const f = familiaDe(m.id); const costo = costoSubir(m.nivel);
  if ((c[f] || 0) < costo) return false;
  c[f] -= costo; set('col:caramelos', c);
  m.nivel += 1; setPC(arr);
  return true;
}

// Opciones de evolución de una instancia (lista; las ramificadas tienen varias). Cada una con su
// requisito: nivel>0 pide nivel; nivel===0 (piedra/trade/amistad → GO puro) solo caramelos.
export function opcionesEvo(iid) {
  const m = buscarInst(pc(), iid); if (!m) return [];
  const car = caramelos()[familiaDe(m.id)] || 0;
  return ((evoData[m.id] && evoData[m.id].evos) || []).map((ev) => {
    const costo = costoEvo(ev.nivel);
    const ok = (ev.nivel === 0 || m.nivel >= ev.nivel) && car >= costo;
    return { a: ev.a, nivel: ev.nivel, costo, ok };
  });
}

// Evoluciona la instancia hacia 'targetId' (una opción de opcionesEvo). Conserva el nivel; el
// pre-evo queda en vistos; NO deja copia en el PC.
export function evolucionarInst(iid, targetId) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const op = opcionesEvo(iid).find((o) => o.a === Number(targetId) && o.ok); if (!op) return false;
  const c = get('col:caramelos', {}); c[familiaDe(m.id)] -= op.costo; set('col:caramelos', c);
  addVisto(m.id);
  m.id = op.a; m.movs = [];          // nueva especie; movs se recalculan en Etapa 2
  addVisto(m.id);
  setPC(arr);
  return op.a;
}

// Reconciliar el PC con conteos AUTORITATIVOS (vienen del server tras un trade, en 1a).
// Especie con más cantidad → agrega instancias nivel 1; con menos → saca (menor nivel primero).
export function reconciliarPC(atrapadosExt, shinyExt = []) {
  const arr = pc(); const objetivo = atrapadosExt || {};
  const porEsp = {}; for (const m of arr) (porEsp[m.id] ||= []).push(m);
  for (const id of new Set([...Object.keys(porEsp), ...Object.keys(objetivo)])) {
    const tengo = (porEsp[id] || []).length; const quiero = objetivo[id] || 0;
    if (quiero < tengo) {
      (porEsp[id] || []).sort((a, b) => a.nivel - b.nivel).slice(0, tengo - quiero)
        .forEach((m) => { const i = arr.indexOf(m); if (i >= 0) arr.splice(i, 1); });
    } else if (quiero > tengo) {
      for (let k = 0; k < quiero - tengo; k++) arr.push({ iid: _uid(), id: Number(id), nivel: 1, exp: 0, shiny: false, movs: [], creado: Date.now() });
      addVisto(id);
    }
  }
  for (const sid of shinyExt) { addVisto(sid); const inst = arr.find((m) => m.id === Number(sid) && !m.shiny); if (inst) inst.shiny = true; }
  setPC(arr);
}

// Regalo: +5 Pokéballs cada 20 minutos (col:regalo guarda el timestamp ms del último).
export function reclamarRegalo() {
  const ult = Number(localStorage.getItem('col:regalo')) || 0;
  if (Date.now() - ult < REGALO_COOLDOWN_MS) return 0;
  localStorage.setItem('col:regalo', String(Date.now()));
  set('col:balls', get('col:balls', 0) + REGALO_BALLS);
  return REGALO_BALLS;
}
export function regaloDisponible() {
  const ult = Number(localStorage.getItem('col:regalo')) || 0;
  return Date.now() - ult >= REGALO_COOLDOWN_MS;
}

// Elige un Pokémon del pool con probabilidad proporcional a su peso (rareza):
// los comunes (peso alto) salen más seguido; los raros/legendarios (peso bajo), menos.
function elegirPonderado(pool, pesos) {
  let total = 0;
  for (const p of pool) total += pesos[p.id] || 1;
  let r = Math.random() * total;
  for (const p of pool) { r -= pesos[p.id] || 1; if (r <= 0) return p; }
  return pool[pool.length - 1];
}

// Tirá una Pokéball: atrapás un salvaje de las regiones desbloqueadas, ponderado por
// rareza (puede aparecer cualquiera, pero con probabilidades distintas). Permite repetidos.
export function tirar(pokemon, temas, pesos = {}) {
  let balls = get('col:balls', 0);
  if (balls <= 0) return { error: 'sin-balls' };
  // salvajes solo de las regiones desbloqueadas (hacés ejercicios de una región
  // para que aparezcan sus Pokémon). Se permiten repetidos.
  const regiones = regionesDesbloqueadas(temas);
  const pool = pokemon.filter((p) => regiones.has(p.region));
  if (!pool.length) return { error: 'vacio' };
  const elegido = elegirPonderado(pool, pesos);
  // probabilidad de que apareciera justo este (su peso sobre el total del pool)
  const totalPeso = pool.reduce((a, p) => a + (pesos[p.id] || 1), 0);
  const prob = (pesos[elegido.id] || 1) / totalPeso;
  // "aparece 1 de cada X intentos" (más intuitivo que el % chico)
  const cadaCuantos = Math.max(1, Math.round(1 / prob));
  balls--;
  // shiny: 1% de las veces (ahora es propiedad de la instancia)
  const shiny = Math.random() < PROB_SHINY;
  atrapar(elegido.id, { shiny });                 // crea la instancia + vistos + caramelos
  const cant = pc().filter((m) => m.id === elegido.id).length;
  set('col:balls', balls);
  return { pokemon: elegido, cantidad: cant, repetido: cant > 1, shiny, nuevoShiny: shiny, balls, prob, cadaCuantos, tier: tierDe(elegido.id, pesos), caramelos: caramelos()[familiaDe(elegido.id)] || 0 };
}
