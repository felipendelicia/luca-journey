# Colección v2 — Etapa 1a (instancias) — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans. Steps use checkbox (`- [ ]`).

**Goal:** Rehacer la colección al estilo Pokémon GO — el PC es una bolsa de instancias (cada Pokémon con nivel), caramelos por familia, Pokédex "vistos" ≠ PC, evolución por nivel — manteniendo el resto del juego (intercambios) andando vía una capa de compatibilidad.

**Architecture:** `coleccion.js` pasa a tener `col:pc` (instancias) como **fuente de verdad** y **deriva** `col:atrapados`/`col:shiny` (compat) para no romper consumidores. Una migración one-time convierte los conteos actuales a instancias. La UI (safari/pokédex) consume la API nueva. Los trades (que el servidor todavía resuelve por conteos) se **reconcilian** al PC cuando llega un cambio externo.

**Tech Stack:** Astro + JS vanilla + localStorage. `web/` no tiene runner JS → la lógica pura se verifica con scripts `node`; la UI, visual (screenshots/CDP).

**Spec:** `superpowers/specs/2026-06-05-coleccion-v2-instancias-design.md`

**Alcance:** Etapa **1a** (modelo + safari + pokédex + evolución + migración + compat). La **1b** (intercambios por instancia, cliente+servidor) es un plan aparte.

---

## Estructura de archivos

| Archivo | Responsabilidad |
|---|---|
| `web/scripts/gen-evoluciones.mjs` | regenerar `evoluciones.json` con `nivel` (min_level) + `familia` (especie base) desde PokeAPI |
| `web/src/data/evoluciones.json` | shape v2: `{ "<id>": { evos:[{a,nivel}], familia } }` |
| `web/src/lib/coleccion.js` | modelo v2: pc/caramelos/vistos + atrapar/subirNivel/evolucionar + derivarCompat/reconciliarPC |
| `web/src/lib/migracion-pc.js` | NUEVO: migración one-time conteos→instancias |
| `web/src/lib/nube.js` | al aplicar un cambio externo de progreso (trade), reconciliar el PC |
| `web/src/pages/safari.astro` | la captura crea instancia + muestra caramelos |
| `web/src/pages/pokedex.astro` | vistas Pokédex (vistos) vs PC (instancias) + Power-Up / Evolucionar |

---

## Task 1: `evoluciones.json` con nivel + familia

**Files:**
- Modify: `web/scripts/gen-evoluciones.mjs`
- Regenerate: `web/src/data/evoluciones.json`

- [ ] **Step 1: Reescribir el generador** para traer la cadena evolutiva con nivel + base.

```javascript
// gen-evoluciones.mjs — cadena evolutiva con datos REALES de PokeAPI.
// Salida: { "<id>": { evos:[{a:<evoId>, nivel:<min_level|30>}], familia:<idBase> } }
// 'nivel' = min_level del trigger level-up; si la evo NO es por nivel (piedra/trade/amistad),
// se mapea a 30 (en esta app todo es "por nivel"). 'familia' = id base de la cadena.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'evoluciones.json');
const N = 721, NIVEL_NO_LEVEL = 30;

async function jget(url) { for (let i = 0; i < 4; i++) { try { const r = await fetch(url); if (r.ok) return await r.json(); } catch {} } return null; }
const idDe = (u) => Number(u.match(/\/(\d+)\/?$/)?.[1]);

// recorre el árbol de la chain; setea evos[] de cada nodo (id<=721) y la familia (raíz)
function recorrer(nodo, baseId, out) {
  const from = idDe(nodo.species.url);
  for (const sig of nodo.evolves_to) {
    const to = idDe(sig.species.url);
    const det = sig.evolution_details?.[0] || {};
    const nivel = det.min_level || NIVEL_NO_LEVEL;
    if (from <= N) (out[from] ||= { evos: [], familia: baseId }).evos.push({ a: to, nivel });
    recorrer(sig, baseId, out);
  }
  if (from <= N && !out[from]) out[from] = { evos: [], familia: baseId };
}

const out = {};
const ids = Array.from({ length: N }, (_, i) => i + 1);
for (let i = 0; i < ids.length; i += 20) {
  await Promise.all(ids.slice(i, i + 20).map(async (id) => {
    const spec = await jget(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
    const chainUrl = spec?.evolution_chain?.url;
    if (!chainUrl) { out[id] ||= { evos: [], familia: id }; return; }
    const chain = await jget(chainUrl);
    if (!chain?.chain) { out[id] ||= { evos: [], familia: id }; return; }
    recorrer(chain.chain, idDe(chain.chain.species.url), out);
  }));
  process.stdout.write('.');
}
// asegurar que todos los 721 tengan entrada (familia = sí mismo si no está en cadena)
for (const id of ids) out[id] ||= { evos: [], familia: id };
fs.writeFileSync(OUT, JSON.stringify(out));
console.log(`\n✓ evoluciones.json: ${Object.keys(out).length} (evos+nivel+familia)`);
```

- [ ] **Step 2: Regenerar** (necesita internet):
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
node scripts/gen-evoluciones.mjs
```
Expected: `✓ evoluciones.json: 721 (evos+nivel+familia)`.

- [ ] **Step 3: Verificar** la forma + un par de casos conocidos:
```bash
node -e "const e=require('./src/data/evoluciones.json'); console.log('charmander 4:',JSON.stringify(e[4])); console.log('zubat 41:',JSON.stringify(e[41])); console.log('pikachu 25:',JSON.stringify(e[25]));"
```
Expected: `4: {evos:[{a:5,nivel:16}],familia:4}`, `41: {evos:[{a:42,nivel:22}],familia:41}` (Zubat→Golbat lvl 22), `25: {evos:[{a:26,nivel:30}],familia:172?}` (Pikachu evoluciona por piedra → nivel 30 fallback; familia base = Pichu 172 si la API la incluye). Anotá lo que salga.

- [ ] **Step 4: Commit**
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/scripts/gen-evoluciones.mjs web/src/data/evoluciones.json
git commit -m "datos: evoluciones.json con nivel de evolucion + familia (PokeAPI)"
```

---

## Task 2: `coleccion.js` — modelo v2 (pc/caramelos/vistos + atrapar + compat)

**Files:**
- Modify: `web/src/lib/coleccion.js`
- Verify: script node

- [ ] **Step 1: Agregar el núcleo v2** cerca de los helpers `get/set` (arriba del archivo). Importá las evoluciones para la familia:

```javascript
import evoData from '../data/evoluciones.json';

const familiaDe = (id) => (evoData[id]?.familia) || Number(id);
const uid = () => Math.random().toString(36).slice(2, 10);

// --- fuentes de verdad v2 ---
export const pc = () => get('col:pc', []);             // [{iid,id,nivel,exp,shiny,movs,creado}]
export const caramelos = () => get('col:caramelos', {}); // {familiaId: cantidad}
export const vistos = () => new Set(get('col:vistos', []));

function setPC(arr) { set('col:pc', arr); derivarCompat(arr); }
function addVisto(id) { const v = get('col:vistos', []); if (!v.includes(Number(id))) { v.push(Number(id)); set('col:vistos', v); } }
function addCaramelos(id, n) { const c = get('col:caramelos', {}); const f = familiaDe(id); c[f] = (c[f] || 0) + n; set('col:caramelos', c); }

// deriva col:atrapados (conteos) y col:shiny (especies) desde el PC → compat con código viejo.
export function derivarCompat(arr = pc()) {
  const at = {}, shi = new Set();
  for (const m of arr) { at[m.id] = (at[m.id] || 0) + 1; if (m.shiny) shi.add(m.id); }
  set('col:atrapados', at);
  set('col:shiny', [...shi]);
}

const CARAMELOS_POR_CAPTURA = 3;
// crea una instancia nueva (al atrapar). Devuelve la instancia.
export function atrapar(id, { shiny = false } = {}) {
  id = Number(id);
  const inst = { iid: uid(), id, nivel: 1, exp: 0, shiny, movs: [], creado: Date.now() };
  const arr = pc(); arr.push(inst); setPC(arr);
  addVisto(id); addCaramelos(id, CARAMELOS_POR_CAPTURA);
  return inst;
}
```

- [ ] **Step 2: Verificar** (node):
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
node --input-type=module -e "
globalThis.localStorage = { _:{}, getItem(k){return this._[k]??null}, setItem(k,v){this._[k]=v}, removeItem(k){delete this._[k]} };
const m = await import('./src/lib/coleccion.js');
const a = m.atrapar(4); const b = m.atrapar(4,{shiny:true});
const arr = m.pc();
console.log('instancias:', arr.length, '| ambas charmander:', arr.every(x=>x.id===4));
console.log('vistos tiene 4:', m.vistos().has(4));
console.log('caramelos familia 4:', m.caramelos()[4]);   // 6 (2 capturas x3)
console.log('compat atrapados[4]:', JSON.parse(localStorage.getItem('col:atrapados'))['4']); // 2
console.log('compat shiny:', JSON.parse(localStorage.getItem('col:shiny'))); // [4]
"
```
Expected: 2 instancias, vistos∋4, caramelos[4]=6, atrapados[4]=2, shiny=[4].

- [ ] **Step 3: Commit**
```bash
git add web/src/lib/coleccion.js
git commit -m "coleccion v2: pc/caramelos/vistos + atrapar(instancia) + derivarCompat"
```

---

## Task 3: `coleccion.js` — subirNivel + evolucionar (por nivel) + reconciliarPC

**Files:**
- Modify: `web/src/lib/coleccion.js`

- [ ] **Step 1: Agregar power-up, evolución por nivel y la reconciliación con conteos externos.**

```javascript
const NIVEL_MAX = 50, COSTO_EVO_CARAMELOS = 25;
export const costoSubir = (nivel) => 1 + Math.floor(nivel / 8);   // caramelos para nivel→nivel+1

const buscarInst = (arr, iid) => arr.find((m) => m.iid === iid);

// Power-Up: gasta caramelos de la familia y sube 1 nivel. Devuelve true si pudo.
export function subirNivel(iid) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m || m.nivel >= NIVEL_MAX) return false;
  const c = get('col:caramelos', {}); const f = familiaDe(m.id); const costo = costoSubir(m.nivel);
  if ((c[f] || 0) < costo) return false;
  c[f] -= costo; set('col:caramelos', c);
  m.nivel += 1; setPC(arr);
  return true;
}

// ¿esta instancia puede evolucionar? (tiene evo Y nivel suficiente Y caramelos)
export function puedeEvolucionar(iid) {
  const m = buscarInst(pc(), iid); if (!m) return null;
  const ev = (evoData[m.id]?.evos || [])[0]; if (!ev) return null;
  const c = caramelos()[familiaDe(m.id)] || 0;
  return { evo: ev.a, nivel: ev.nivel, ok: m.nivel >= ev.nivel && c >= COSTO_EVO_CARAMELOS };
}

// Evoluciona la instancia: cambia id al evo, CONSERVA nivel, gasta caramelos, el pre-evo va a vistos.
export function evolucionarInst(iid) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const p = puedeEvolucionar(iid); if (!p || !p.ok) return false;
  const c = get('col:caramelos', {}); const f = familiaDe(m.id);
  c[f] -= COSTO_EVO_CARAMELOS; set('col:caramelos', c);
  addVisto(m.id);          // el pre-evo queda "visto" en la Pokédex
  m.id = p.evo;            // misma instancia, nueva especie
  addVisto(m.id);
  setPC(arr);
  return p.evo;
}

// Reconciliar el PC con conteos AUTORITATIVOS (vienen del server tras un trade en 1a).
// Si una especie subió de cantidad → agrega instancias nivel 1; si bajó → saca (menor nivel primero).
export function reconciliarPC(atrapadosExt, shinyExt = []) {
  const arr = pc(); const objetivo = atrapadosExt || {};
  const porEsp = {}; for (const m of arr) (porEsp[m.id] ||= []).push(m);
  // bajadas / subidas
  for (const id of new Set([...Object.keys(porEsp), ...Object.keys(objetivo)])) {
    const tengo = (porEsp[id] || []).length; const quiero = objetivo[id] || 0;
    if (quiero < tengo) {
      (porEsp[id] || []).sort((a, b) => a.nivel - b.nivel).slice(0, tengo - quiero)
        .forEach((m) => { const i = arr.indexOf(m); if (i >= 0) arr.splice(i, 1); });
    } else if (quiero > tengo) {
      for (let k = 0; k < quiero - tengo; k++) arr.push({ iid: uid(), id: Number(id), nivel: 1, exp: 0, shiny: false, movs: [], creado: Date.now() });
      addVisto(id);
    }
  }
  for (const id of shinyExt) { addVisto(id); const inst = arr.find((m) => m.id === Number(id) && !m.shiny); if (inst) inst.shiny = true; }
  setPC(arr);
}
```

- [ ] **Step 2: Verificar** (node) power-up + evolución + reconcile:
```bash
node --input-type=module -e "
globalThis.localStorage = { _:{}, getItem(k){return this._[k]??null}, setItem(k,v){this._[k]=v}, removeItem(k){delete this._[k]} };
const m = await import('./src/lib/coleccion.js');
const a = m.atrapar(4); // charmander, familia 4
localStorage.setItem('col:caramelos', JSON.stringify({4: 100}));
let lvl=1; while (m.subirNivel(a.iid)) lvl=m.pc()[0].nivel;        // sube hasta poder/cap
console.log('nivel charmander:', m.pc()[0].nivel, '(>=16 para evo)');
console.log('puede evo:', JSON.stringify(m.puedeEvolucionar(a.iid)));
const evo = m.evolucionarInst(a.iid);
console.log('evoluciono a:', evo, '| sigue 1 instancia:', m.pc().length, '| nivel conservado:', m.pc()[0].nivel);
console.log('vistos charmander(4) y charmeleon(5):', m.vistos().has(4), m.vistos().has(5));
// reconcile: server dice que ahora tengo 0 charmeleon (lo regalé) y 1 squirtle (7)
m.reconciliarPC({7:1});
console.log('tras reconcile -> ids en pc:', m.pc().map(x=>x.id), '(deberia ser [7])');
"
```
Expected: nivel ≥16, puede evo ok, evoluciona a 5, 1 sola instancia con el nivel conservado, vistos∋{4,5}; tras reconcile el pc queda `[7]`.

- [ ] **Step 3: Reemplazar las funciones viejas** `evolucionesPosibles`/`evolucionar` (basadas en 3 repes) por la API nueva, y actualizar a sus consumidores (la pokédex en Task 7). Dejá las viejas exportadas como wrappers no-op si algo las importa, o quitá los imports. Buscá usos: `grep -rn "evolucionesPosibles\|evolucionar\b" src` y ajustá.

- [ ] **Step 4: Commit**
```bash
git add web/src/lib/coleccion.js
git commit -m "coleccion v2: subirNivel/evolucionarInst (por nivel+caramelos) + reconciliarPC (compat trades)"
```

---

## Task 4: `migracion-pc.js` — migración one-time

**Files:**
- Create: `web/src/lib/migracion-pc.js`
- Modify: `web/src/lib/coleccion.js` (llamar la migración en el primer acceso) o `nube.js` (boot)

- [ ] **Step 1: Crear la migración**

```javascript
// migracion-pc.js — one-time: col:atrapados {id:n} + col:shiny [ids] → col:pc/vistos/caramelos.
// Idempotente (flag col:pc:migrado). Conserva todo: cada repe = una instancia nivel 1.
const get = (k, def) => { try { return JSON.parse(localStorage.getItem(k)) ?? def; } catch { return def; } };
const set = (k, v) => localStorage.setItem(k, JSON.stringify(v));
const uid = () => Math.random().toString(36).slice(2, 10);

export function migrarPC() {
  if (localStorage.getItem('col:pc:migrado') === '1') return false;
  // si ya hay PC (cuenta nueva que arrancó en v2), solo marcar migrado
  if (Array.isArray(get('col:pc', null))) { localStorage.setItem('col:pc:migrado', '1'); return false; }
  const at = get('col:atrapados', {}); const shi = new Set(get('col:shiny', []));
  const pc = [], vistos = new Set();
  for (const [id, n] of Object.entries(at)) {
    const k = Number(id); vistos.add(k);
    for (let i = 0; i < n; i++) pc.push({ iid: uid(), id: k, nivel: 1, exp: 0, shiny: false, movs: [], creado: Date.now() });
  }
  for (const id of shi) { vistos.add(Number(id)); const inst = pc.find((m) => m.id === Number(id) && !m.shiny); if (inst) inst.shiny = true; }
  set('col:pc', pc); set('col:vistos', [...vistos]); set('col:caramelos', get('col:caramelos', {}));
  localStorage.setItem('col:pc:migrado', '1');
  return true;
}
```

- [ ] **Step 2: Llamarla antes de cualquier uso del PC.** En `coleccion.js`, al inicio (tras los imports), importá y corré la migración de forma perezosa la primera vez:
```javascript
import { migrarPC } from './migracion-pc.js';
let _migrado = false;
function asegurarMigrado() { if (!_migrado) { _migrado = true; try { migrarPC(); } catch {} } }
```
y llamá `asegurarMigrado()` al principio de `pc()`, `caramelos()`, `vistos()` y `atrapar()`. (Así corre sí o sí antes de leer/escribir el PC, sin depender del orden de carga.)

- [ ] **Step 3: Verificar** (node):
```bash
node --input-type=module -e "
globalThis.localStorage = { _:{ 'col:atrapados':JSON.stringify({4:3, 7:1}), 'col:shiny':JSON.stringify([7]) }, getItem(k){return this._[k]??null}, setItem(k,v){this._[k]=v}, removeItem(k){delete this._[k]} };
const m = await import('./src/lib/coleccion.js');
const arr = m.pc();
console.log('instancias:', arr.length, '(esperado 4: 3 charmander + 1 squirtle)');
console.log('squirtle shiny?', arr.find(x=>x.id===7).shiny);
console.log('vistos:', [...m.vistos()].sort());
console.log('re-migrar es no-op:', !(await import('./src/lib/migracion-pc.js')).migrarPC());
"
```
Expected: 4 instancias, squirtle shiny=true, vistos=[4,7], re-migrar=false.

- [ ] **Step 4: Commit**
```bash
git add web/src/lib/migracion-pc.js web/src/lib/coleccion.js
git commit -m "coleccion v2: migracion one-time conteos->instancias (idempotente, conserva todo)"
```

---

## Task 5: enganchar `reconciliarPC` a los cambios externos (trades en 1a)

**Files:**
- Modify: `web/src/lib/nube.js`

- [ ] **Step 1:** En `nube.js`, donde se aplican cambios externos del progreso (`suscribirProgreso` → `aplicarNube(estado)` por un trade), tras aplicar la nube llamá a reconciliar el PC con los conteos nuevos. Importá `reconciliarPC` de `coleccion.js`. En el handler de `rt.on('progreso', (estado) => {...})`, después de `aplicarNube(estado)`:
```javascript
try {
  const at = JSON.parse(estado['col:atrapados'] || '{}');
  const shi = JSON.parse(estado['col:shiny'] || '[]');
  reconciliarPC(at, shi);
} catch {}
```
Así, cuando un trade (resuelto por el server sobre conteos) cambia tu colección, el PC se ajusta (instancias + vistos) sin perder los niveles de lo que ya tenías.

- [ ] **Step 2: Commit**
```bash
git add web/src/lib/nube.js
git commit -m "coleccion v2: reconciliar el PC al recibir cambios externos (trades) en 1a"
```

---

## Task 6: Safari — la captura crea una instancia

**Files:**
- Modify: `web/src/pages/safari.astro`

- [ ] **Step 1:** El safari hoy usa `tirar()` que incrementa `col:atrapados`. Cambiá `tirar()` (en `coleccion.js`) para que, en vez de `at[elegido.id]++`, llame a `atrapar(elegido.id, { shiny })` y devuelva además los **caramelos** ganados y el conteo de esa especie en el PC. Mínimo: que la captura cree una instancia. Mantené el `tier` y el shiny que ya devuelve.
  En `tirar()` reemplazá el bloque que hace `at[elegido.id] = (at[elegido.id]||0)+1; ... set('col:atrapados', at)` por:
```javascript
  const inst = atrapar(elegido.id, { shiny });
  const cant = pc().filter((m) => m.id === elegido.id).length;
  // (el shiny ya lo maneja atrapar via la instancia; sacá el manejo viejo de col:shiny)
```
  y en el `return` usá `cantidad: cant` y agregá `caramelos: caramelos()[familiaDe(elegido.id)]` si querés mostrarlo.

- [ ] **Step 2:** En `safari.astro`, en el texto de captura, agregá "🍬 +3 caramelos" (de la familia). Opcional pero lindo.

- [ ] **Step 3: Verificar visual** (dev server / CDP): tirar varias veces y confirmar que se crean instancias (lo validás en la pokédex del Task 7). Build: `cd web && npm run build`.

- [ ] **Step 4: Commit**
```bash
git add web/src/lib/coleccion.js web/src/pages/safari.astro
git commit -m "safari: la captura crea una instancia (PC) + caramelos"
```

---

## Task 7: Pokédex — vistos vs PC + Power-Up / Evolucionar

**Files:**
- Modify: `web/src/pages/pokedex.astro`

- [ ] **Step 1:** La pokédex pasa a tener dos lecturas:
  - **Pokédex (completitud)**: usar `vistos()` para marcar cada especie como vista/no-vista (en vez de `col:atrapados`). El "tengo/total" por región se calcula con `vistos`.
  - **Mi PC**: listar las **instancias** (`pc()`), agrupadas por especie: cuántas tengo, con su **nivel**; botones **Power-Up** (`subirNivel(iid)`, deshabilitado si faltan caramelos) y **Evolucionar** (`evolucionarInst(iid)`, visible si `puedeEvolucionar(iid).ok`). Mostrar **caramelos por familia**.

- [ ] **Step 2:** Importar de `coleccion.js`: `pc, caramelos, vistos, subirNivel, evolucionarInst, puedeEvolucionar`. Re-render tras cada acción. Reusar el badge de tier (`tierDe`) por especie.

- [ ] **Step 3:** Quitar el uso de `evolucionesPosibles`/`evolucionar` viejos (reemplazados por la UI de instancias). El badge de rareza por especie se mantiene.

- [ ] **Step 4: Verificar visual** (CDP, ambos temas): que se vea la Pokédex (vistos) + el PC con niveles + Power-Up sube nivel gastando caramelos + Evolucionar al nivel. Screenshots oscuro/claro.

- [ ] **Step 5: Commit**
```bash
git add web/src/pages/pokedex.astro web/src/lib/coleccion.js
git commit -m "pokedex: Pokedex(vistos) + PC(instancias con nivel) + Power-Up/Evolucionar"
```

---

## Task 8: Build + deploy + verificación de compat

- [ ] **Step 1:** `cd web && npm run build` (490 páginas, sin errores).
- [ ] **Step 2:** Verificar (dev/CDP) que **intercambios siguen andando**: como el server resuelve sobre `col:atrapados` (derivado) y al recibir el cambio `reconciliarPC` ajusta el PC, un trade no rompe nada. (Test de 2 sesiones manual con el owner, o al menos que la sala de intercambio cargue sin error.)
- [ ] **Step 3:** Commit `docs/` + push (`git add docs && git commit -m "build: coleccion v2 etapa 1a" && git push origin main`).

---

## Self-review (cobertura del spec)

- **Pokédex (vistos) ≠ PC, evolución sin dejar copia:** Task 3 (`evolucionarInst` → vistos, sin copia) + Task 7 (UI). ✔
- **Instancias GO-style con nivel:** Task 2 (`pc`/`atrapar`) + Task 3 (subirNivel). ✔
- **Caramelos por familia, suben nivel:** Task 1 (familia) + Task 2 (addCaramelos) + Task 3 (subirNivel/costo). ✔
- **Evolución por nivel (PokeAPI):** Task 1 (datos) + Task 3 (`puedeEvolucionar`/`evolucionarInst`). ✔
- **Migración one-time conserva todo:** Task 4. ✔
- **Compat (no romper trades):** Task 2 (`derivarCompat`) + Task 3/5 (`reconciliarPC`). ✔
- **`movs` placeholder (Etapa 2):** schema de instancia lo incluye (`movs:[]`). ✔
- **Fuera de alcance (batalla, movimientos, 1b trades por instancia):** sin tasks. ✔

Sin placeholders en la lógica (tasks 1–5 con código + verificación node). UI (6–7) con la API concreta + verificación visual.
