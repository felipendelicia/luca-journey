// coleccion.js — sistema de colección de Pokémon (todo en localStorage).
// Aprender = atrapar: cada ejercicio resuelto da Pokéballs; completar un tema o
// una región te da capturas garantizadas. Se pueden tener REPETIDOS (conteo por id).

import { tierDe } from './rareza.js';
import evoData from '../data/evoluciones.json' with { type: 'json' };
import aparicion from '../data/aparicion.json' with { type: 'json' };
import learnsets from '../data/learnsets.json' with { type: 'json' };
import { ITEMS } from './items.js';
import { migrarPC } from './migracion-pc.js';
import habilidades from '../data/habilidades.json';
import yields from '../data/yields.json';
import tipos from '../data/tipos.json' with { type: 'json' };
import { probCaptura, pisoIV, fleeProb, sincronizaNat } from './safari-core.js';
import { rolarIdentidad, identidad as identidadCore, NATURALEZAS, sumarEV } from './combate-core.ts';

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
export const caramelosDe = (id) => caramelos()[familiaDe(id)] || 0;                     // caramelos de la familia evolutiva
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

// nivel al que cada especie se "produce" por evolución (reverse de evoData). Sirve para que un
// Pokémon evolucionado NO aparezca salvaje a nivel bajo.
const _nivelProduccion = {};   // id -> nivel del trigger que lo produce (0 = piedra/etc)
for (const sid in evoData) for (const ev of (evoData[sid].evos || [])) {
  if (_nivelProduccion[ev.a] === undefined || ev.nivel > _nivelProduccion[ev.a]) _nivelProduccion[ev.a] = ev.nivel;
}

// nivel mínimo salvaje: combina rareza (tier 1..10) y etapa evolutiva. Un evolucionado puede
// salir un poco POR DEBAJO de su nivel de evolución (margen 8): Charizard (evo nv.36) sale desde
// ~28, nunca a nv.3; Caterpie (común, base) sale bajo; legendarios (tier alto) salen altos.
const MARGEN_EVO = 8;
export function nivelMinWild(id) {
  const prod = _nivelProduccion[id];
  if (prod !== undefined) {   // es una evolución → manda el nivel de evolución (con margen)
    return Math.min(50, Math.max(1, (prod > 0 ? prod : 22) - MARGEN_EVO)); // por nivel: N-8; piedra: 14
  }
  // forma base → por rareza (tier): legendarios salen altos, comunes bajos.
  const tier = tierDe(id, aparicion).nivel;                 // 1..10
  return Math.round((tier - 1) / 9 * 38) + 1;               // tier1→1 … tier10→39
}
// nivel salvaje al atrapar: ≥ mínimo, con cola EXPONENCIAL real (media ~4 sobre el mínimo →
// niveles MUY altos son rarísimos, sin importar la especie).
export function nivelWild(id) {
  const min = nivelMinWild(id);
  const extra = Math.floor(-4 * Math.log(1 - Math.random()));
  return Math.min(50, min + extra);
}

// crea una instancia nueva (al atrapar) + suma a vistos + caramelos a la familia. Devuelve la instancia.
export function atrapar(id, { shiny = false, nivel = 1, alfa = false, ivs = null, nat = null, hab = null, gen = null } = {}) {
  id = Number(id);
  const idn = (ivs && nat != null) ? { ivs, nat, hab, gen } : rolarIdentidad(id, habilidades);
  const inst = { iid: _uid(), id, nivel, exp: 0, shiny, movs: [], creado: Date.now(),
    ivs: idn.ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen, evs: [0, 0, 0, 0, 0, 0], ...(alfa ? { alfa: true } : {}) };
  const arr = pc(); arr.push(inst); setPC(arr);
  addVisto(id); addCaramelos(id, CARAMELOS_POR_CAPTURA);
  return inst;
}

// data de combate para derivar identidad de una instancia (para UI)
const _DATOS_ID = { habilidades };
export const identidadDe = (inst) => identidadCore(inst, _DATOS_ID);
export const evsDe = (inst) => (inst.evs && inst.evs.length === 6) ? inst.evs : [0, 0, 0, 0, 0, 0];
export const naturalezaDe = (inst) => NATURALEZAS[identidadDe(inst).nat] || NATURALEZAS[0];
export const habMeta = (key) => (habilidades.meta || {})[key] || null;
export const yieldDe = (id) => yields[String(id)] || [0, 0, 0, 0, 0, 0];

// % de IVs (0-100) y estrellas (0-4) para el header estilo GO.
export const ivPct = (ivs) => Math.round((ivs.reduce((a, b) => a + b, 0) / 186) * 100);
export const ivEstrellas = (ivs) => { const p = ivPct(ivs); return p >= 90 ? 4 : p >= 75 ? 3 : p >= 50 ? 2 : p >= 25 ? 1 : 0; };
// frase del "Juez" por IV individual (0-31).
export const juezIV = (iv) => iv === 31 ? '¡Inmejorable!' : iv >= 26 ? 'Fantástico' : iv >= 16 ? 'Muy bueno' : iv >= 1 ? 'Normal' : 'Flojo';

// otorga EVs a una instancia (por iid) según un vector yield. Persiste. Respeta caps.
export function darEV(iid, yieldVec) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return;
  m.evs = sumarEV(evsDe(m), yieldVec); setPC(arr);
}

// usa una vitamina sobre una instancia: +10 EV al stat, tope 100 por vía vitamina y caps globales (252/510).
export function usarVitamina(iid, statIdx) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
  const ev = evsDe(m);
  if (ev[statIdx] >= 100) return false;        // tope vitamina
  const yieldVec = [0, 0, 0, 0, 0, 0]; yieldVec[statIdx] = Math.min(10, 100 - ev[statIdx]);
  m.evs = sumarEV(ev, yieldVec); setPC(arr);
  return true;
}

export const BALLS_POR_EJERCICIO = 2;
export const REGALO_BALLS = 8;                     // Pokéballs por regalo (cada 20 min)
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
export const LEGENDARIOS = { kanto: 150, johto: 249, hoenn: 384, sinnoh: 483, unova: 643, kalos: 716, alola: 791, galar: 888, paldea: 1007 };

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

  const capturar = (id) => { if (id) { atrapar(id, { nivel: nivelWild(id) }); nuevo.capturas.push(id); } };
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
export const NIVEL_MAX = 99;   // tope de Power-Up. (La captura salvaje sigue capada a 50, ver nivelWild)
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

// ¿el req es una piedra tipada? (las evos por piedra aceptan el comodín legacy 'piedra').
const esPiedra = (req) => !!req && req.startsWith('piedra');
// ¿tengo lo que pide esta evo? sin req → sí; piedra tipada → ella o el comodín legacy.
const tieneReq = (req) => !req || tieneItem(req) || (esPiedra(req) && tieneItem('piedra'));
// consume el req (la piedra tipada, o el comodín 'piedra' como respaldo). true si gastó algo.
const usarReq = (req) => !req || usarItem(req) || (esPiedra(req) && usarItem('piedra'));

// Opciones de evolución de una instancia (lista; las ramificadas tienen varias). Cada una con su
// requisito: nivel>0 pide nivel + caramelos; por piedra/Disco (`req`) pide SOLO el item (0 caramelos,
// fiel al canon); amistad/otras (nivel===0 sin req) piden caramelos. El comodín legacy 'piedra' sirve.
export function opcionesEvo(iid) {
  const m = buscarInst(pc(), iid); if (!m) return [];
  const car = caramelos()[familiaDe(m.id)] || 0;
  return ((evoData[m.id] && evoData[m.id].evos) || []).map((ev) => {
    const req = ev.req || null;                             // item de tienda que hace falta (o null)
    const costo = (req || ev.nivel > 0) ? 0 : costoEvo(ev.nivel);   // por piedra/disco o por NIVEL: solo el requisito (0 caramelos); amistad/otras: caramelos
    const ok = (ev.nivel > 0 ? m.nivel >= ev.nivel : true) && tieneReq(req) && car >= costo;
    return { a: ev.a, nivel: ev.nivel, costo, ok, req };
  });
}

// Evoluciona la instancia hacia 'targetId' (una opción de opcionesEvo). Conserva el nivel; el
// pre-evo queda en vistos; NO deja copia en el PC.
export function evolucionarInst(iid, targetId) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const op = opcionesEvo(iid).find((o) => o.a === Number(targetId) && o.ok); if (!op) return false;
  if (!usarReq(op.req)) return false;                       // gasta la piedra/disco que pida (si pide)
  if (op.costo) { const c = get('col:caramelos', {}); c[familiaDe(m.id)] = (c[familiaDe(m.id)] || 0) - op.costo; set('col:caramelos', c); }
  addVisto(m.id);
  m.id = op.a; m.movs = [];          // nueva especie; movs se recalculan en Etapa 2
  addVisto(m.id);
  set('col:evos', get('col:evos', 0) + 1);   // contador para el logro "primera evolución"
  setPC(arr);
  return op.a;
}

// Poné/sacá el mote (apodo) de una instancia. Vacío = sin mote.
export function renombrar(iid, mote) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const v = String(mote || '').trim().slice(0, 16);
  if (v) m.mote = v; else delete m.mote;
  setPC(arr); return true;
}

// Learnset COMPLETO de una especie (incl. ataques aún bloqueados): [{m:moveId, n:nivel}].
export const learnsetDe = (id) => learnsets[id] || [];
// Ataques DESBLOQUEADOS por una instancia: del learnset, los que aprende a nivel ≤ su nivel.
export function movsDesbloqueados(inst) {
  return (learnsets[inst.id] || []).filter((x) => x.n <= inst.nivel);
}
// Fijar los 4 ataques ACTIVOS de una instancia (deben estar desbloqueados; máximo 4).
export function setMovs(iid, moveIds) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const ok = new Set(movsDesbloqueados(m).map((x) => x.m));
  m.movs = (moveIds || []).map(Number).filter((id) => ok.has(id)).slice(0, 4);
  setPC(arr); return true;
}

// Premios (batalla): sumar caramelos a una familia / sumar Pokéballs.
export function darCaramelos(id, n) { addCaramelos(id, Math.max(0, n | 0)); }
export function darBalls(n) { set('col:balls', get('col:balls', 0) + Math.max(0, n | 0)); }

// ───────── Tienda · inventario de items (col:items) ─────────
export const items = () => get('col:items', {});
export function darItem(id, n = 1) { const inv = get('col:items', {}); inv[id] = (inv[id] || 0) + n; set('col:items', inv); }
export const tieneItem = (id) => (get('col:items', {})[id] || 0) > 0;
export function usarItem(id) { const inv = get('col:items', {}); if (!(inv[id] > 0)) return false; inv[id]--; if (inv[id] <= 0) delete inv[id]; set('col:items', inv); return true; }
export function comprarItem(id) {
  const it = ITEMS[id]; if (!it) return false;
  const balls = get('col:balls', 0); if (balls < it.precio) return false;
  set('col:balls', balls - it.precio); darItem(id, 1); return true;
}

// Liberar una instancia (GO): la perdés del PC y te da 1 caramelo de la familia. Queda en vistos.
export function liberar(iid) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const i = arr.indexOf(m); if (i < 0) return false;
  arr.splice(i, 1);
  addCaramelos(m.id, 1);
  setPC(arr);
  return true;
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

// ───────── Racha diaria ─────────
// col:racha = { dias, ultima:'YYYY-MM-DD' }. Días consecutivos dan bonus de Pokébolas (escalado).
const hoyISO = () => new Date().toLocaleDateString('en-CA');   // YYYY-MM-DD local
const diaAnterior = (iso) => { const d = new Date(iso + 'T12:00:00'); d.setDate(d.getDate() - 1); return d.toLocaleDateString('en-CA'); };
export function rachaEstado() { return get('col:racha', { dias: 0, ultima: '' }); }
// Reclama la racha del día (idempotente por día). Devuelve { dias, bonus, nuevo }.
export function rachaHoy() {
  const hoy = hoyISO(); const r = rachaEstado();
  if (r.ultima === hoy) return { dias: r.dias, bonus: 0, nuevo: false };   // ya reclamada hoy
  const dias = r.ultima === diaAnterior(hoy) ? (r.dias || 0) + 1 : 1;      // consecutivo o reinicio
  const bonus = 5 * Math.min(dias, 5);                                     // +5..+25
  set('col:racha', { dias, ultima: hoy });
  set('col:balls', get('col:balls', 0) + bonus);
  return { dias, bonus, nuevo: true };
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

// ───────────────────────── safari profundo (encuentro 2 pasos) ─────────────────────────
const BALL_KEYS = ['pokeball', 'superball', 'ultraball', 'veloz', 'turno', 'red', 'repeticion', 'xeneize', 'master'];

// inventario de balls que tenés (pokeball = contador col:balls; el resto = items). [{key,n,...meta}]
export function inventarioBalls() {
  const inv = items();
  return BALL_KEYS
    .map((k) => ({ key: k, n: k === 'pokeball' ? get('col:balls', 0) : (inv[k] || 0), ...ITEMS[k] }))
    .filter((b) => b.n > 0);
}
export const tieneBall = (key) => key === 'pokeball' ? get('col:balls', 0) > 0 : (items()[key] || 0) > 0;
function consumirBall(key) {
  if (key === 'pokeball') set('col:balls', Math.max(0, get('col:balls', 0) - 1));
  else usarItem(key);
}

// compañero (para Sincronía). col:companero = iid.
export const companero = () => { const iid = get('col:companero', null); return iid ? pc().find((m) => m.iid === iid) || null : null; };
export function setCompanero(iid) { set('col:companero', iid); }

// sube los `n` IVs más bajos (no perfectos) a 31. Para alfa (3 garantizados).
function forzarPerfectos(ivs, n) {
  const out = ivs.slice();
  const idxs = out.map((v, i) => [v, i]).filter(([v]) => v < 31).sort((a, b) => a[0] - b[0]).slice(0, n);
  for (const [, i] of idxs) out[i] = 31;
  return out;
}

export const PROB_ALFA = 0.04;

// PASO 1: aparece un salvaje. Rolea especie + identidad + shiny + alfa. NO persiste.
export function encontrar(pokemon, temas, pesos = {}) {
  const regiones = regionesDesbloqueadas(temas);
  const pool = pokemon.filter((p) => regiones.has(p.region));
  if (!pool.length) return { error: 'vacio' };
  const elegido = elegirPonderado(pool, pesos);
  const id = elegido.id;
  const idn = rolarIdentidad(id, habilidades);
  // Sincronía: si el compañero la tiene, fija la naturaleza
  const comp = companero();
  if (comp) { const ci = identidadCore(comp, _DATOS_ID); const ns = sincronizaNat(ci.hab, ci.nat); if (ns != null) idn.nat = ns; }
  const alfa = Math.random() < PROB_ALFA;
  const ivs = alfa ? forzarPerfectos(idn.ivs, 3) : idn.ivs;
  return {
    id, nivel: nivelWild(id), ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen,
    shiny: Math.random() < PROB_SHINY, alfa,
    rarezaTier: tierDe(id, aparicion).nivel, estrellas: ivEstrellas(ivs),
    naturalezaNombre: NATURALEZAS[idn.nat].nombre,
    tiposWild: tipos[String(id)] || [], vistoYa: vistos().has(id),
    pokemon: elegido,
  };
}

// PASO 2: tirás la ball elegida con una calidad de tiro. Consume la ball; en éxito persiste.
export function capturar(enc, ballKey, calidad = 'Normal', extra = {}) {
  if (!tieneBall(ballKey)) return { error: 'sin-ball' };
  consumirBall(ballKey);
  const ballDef = { key: ballKey, ...ITEMS[ballKey] };
  const tiroN = extra.tiroN || 1;
  const ctx = { tiroN, calidad, tiposWild: enc.tiposWild, vistoYa: enc.vistoYa };
  const prob = probCaptura(enc.rarezaTier, ballDef, ctx);
  if (Math.random() < prob) {
    const ivs = pisoIV(enc.ivs, calidad);
    const inst = atrapar(enc.id, { shiny: enc.shiny, nivel: enc.nivel, alfa: enc.alfa, ivs, nat: enc.nat, hab: enc.hab, gen: enc.gen });
    return { ok: true, inst, prob, calidad, ball: ballKey };
  }
  const huyo = Math.random() < fleeProb(enc.rarezaTier);
  return { ok: false, huyo, prob, calidad, ball: ballKey };
}
