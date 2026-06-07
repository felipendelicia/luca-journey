# Safari profundo — Fase 2 · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Sumar al Safari una racha simple de capturas (caza shiny), biomas y hora del día automáticos, la Dusk Ball y ejemplares alfa con tamaños.

**Architecture:** La matemática pura (racha→shiny/IV, hora/bioma deterministas por reloj, dusk, tamaños) va en `web/src/lib/safari-core.js` (sin DOM/JSON, testeada con `node --test`). `coleccion.js` orquesta estado (`col:racha`, filtro de bioma, tam) reusando safari-core. Data nueva `biomas.json` (habitat de PokeAPI). UI en `safari.astro`/`pokedex.astro`/`tienda.astro` con `/frontend-design`.

**Tech Stack:** JS módulos ES, Astro, `node --test` (runner nativo), SVG sprites, Node gen-script.

**Convención:** specs/plans en `superpowers/` (raíz). Sin atribución Claude. UI → `/frontend-design`. Links con `u('/...')`/`window.__BASE`. Spec: `superpowers/specs/2026-06-07-safari-profundo-fase2-design.md`.

**Contexto (Fase 1, ya en main):**
- `safari-core.js` exporta `MULT_CALIDAD, baseCaptura, catchBall, probCaptura, fleeProb, pisoIV, sincronizaNat`.
- `coleccion.js`: `encontrar(pokemon, temas, pesos)` (rolea especie del pool de regiones desbloqueadas +
  identidad + shiny `PROB_SHINY=0.01` + alfa `PROB_ALFA=0.04` con `forzarPerfectos(ivs,3)`); `capturar(enc,
  ballKey, calidad, {tiroN})`; `atrapar(id, {shiny,nivel,alfa,ivs,nat,hab,gen})`; `BALL_KEYS` array;
  `inventarioBalls/tieneBall/consumirBall/companero`. Importa `aparicion`, `habilidades`, `tipos`.
- `items.js`: balls en cat `'ball'` (`pokeball/superball/ultraball/veloz/turno/red/repeticion/master/xeneize`),
  campo `catch`/`cond`. `sprites.js`: `ballSvg` por variante; `itemSvg` mapea sprite→ballSvg.
- `safari.astro`: barra superior `.safari-barra` con `.ss-item` (#balls), `refrescar()` actualiza contadores.

---

### Task 1: `safari-core.js` — racha/shiny, hora/bioma, dusk, tamaños (puro + tests)

**Files:**
- Modify: `web/src/lib/safari-core.js`
- Test: `web/src/lib/safari-core.test.mjs`

- [ ] **Step 1: Agregar tests (FALLAN primero)** — APPEND a `web/src/lib/safari-core.test.mjs`:

```js
import { shinyChance, pisoRacha, esNoche, biomaActual, rolarTam } from './safari-core.js';

test('shinyChance: racha 0 = 0.01, crece, cap 0.08', () => {
  assert.equal(shinyChance(0), 0.01);
  assert.ok(shinyChance(25) > shinyChance(10));
  assert.equal(shinyChance(1000), 0.08);
});
test('pisoRacha: umbrales 15/30/50', () => {
  assert.equal(pisoRacha(14), 0);
  assert.equal(pisoRacha(15), 1);
  assert.equal(pisoRacha(30), 2);
  assert.equal(pisoRacha(50), 3);
});
test('esNoche: 23h noche, 12h día', () => {
  assert.equal(esNoche(new Date(2026, 0, 1, 23, 0)), true);
  assert.equal(esNoche(new Date(2026, 0, 1, 12, 0)), false);
  assert.equal(esNoche(new Date(2026, 0, 1, 5, 0)), true);
});
test('biomaActual: determinista, rota cada 10 min', () => {
  assert.equal(biomaActual(0), 'hierba');
  assert.equal(biomaActual(599999), 'hierba');
  assert.equal(biomaActual(600000), 'agua');
  assert.equal(biomaActual(1200000), 'cueva');
  assert.equal(biomaActual(1800000), 'hierba');
});
test('catchBall dusk: noche o cueva → 3.5; día+superficie → 1', () => {
  const dusk = { key: 'dusk' };
  assert.equal(catchBall(dusk, ctx({ noche: true, bioma: 'hierba' })), 3.5);
  assert.equal(catchBall(dusk, ctx({ noche: false, bioma: 'cueva' })), 3.5);
  assert.equal(catchBall(dusk, ctx({ noche: false, bioma: 'hierba' })), 1);
});
test('rolarTam: extremos y rango', () => {
  assert.equal(rolarTam(() => 0.01), 'XXS');
  assert.equal(rolarTam(() => 0.5), 'M');
  assert.equal(rolarTam(() => 0.99), 'XXL');
  ['XXS', 'S', 'M', 'L', 'XXL'].forEach((t) => assert.ok(typeof t === 'string'));
});
```
(El `ctx` helper y el import de `catchBall` ya existen en el archivo de tests de Fase 1; si `catchBall` no estuviera importado, agregalo al import de arriba.)

- [ ] **Step 2: Correr, debe FALLAR**: `cd web && node --test src/lib/safari-core.test.mjs` → FAIL (símbolos no existen).

- [ ] **Step 3: Implementar en `web/src/lib/safari-core.js`** — agregar al final:

```js
// ───────────────────────── Fase 2: racha / hora / bioma / tamaños ─────────────────────────
// chance de shiny según la racha de capturas seguidas. Base 1%, cap 8%.
export const shinyChance = (racha) => Math.min(0.08, 0.01 * (1 + (racha || 0) * 0.12));
// IVs perfectos garantizados por racha alta.
export const pisoRacha = (racha) => racha >= 50 ? 3 : racha >= 30 ? 2 : racha >= 15 ? 1 : 0;
// ¿es de noche? (reloj del dispositivo). Noche = antes de las 6 o desde las 19.
export const esNoche = (now = new Date()) => { const h = now.getHours(); return h < 6 || h >= 19; };
// bioma actual: rota Hierba→Agua→Cueva cada 10 min, determinista por el reloj.
export const biomaActual = (ms = Date.now()) => ['hierba', 'agua', 'cueva'][Math.floor(ms / 600000) % 3];
// tamaño del ejemplar (cosmético). Casi siempre Normal; colas raras XXS/XXL.
export function rolarTam(rng = Math.random) {
  const r = rng();
  return r < 0.03 ? 'XXS' : r < 0.12 ? 'S' : r > 0.97 ? 'XXL' : r > 0.88 ? 'L' : 'M';
}
```
Y en `catchBall`, agregar el caso `dusk` (antes del `default`):
```js
    case 'dusk': return (ctx.noche || ctx.bioma === 'cueva') ? 3.5 : 1;
```

- [ ] **Step 4: Correr, debe PASAR**: `cd web && node --test src/lib/safari-core.test.mjs` → todas verdes (Fase 1 + Fase 2).

- [ ] **Step 5: Commit** (sin atribución Claude):
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/safari-core.js web/src/lib/safari-core.test.mjs
git commit -m "safari-core: racha→shiny/IV, hora/bioma deterministas, dusk ball, tamaños (puro + tests)"
```

---

### Task 2: `gen-biomas.mjs` + `biomas.json` (habitat de PokeAPI)

**Files:**
- Create: `web/scripts/gen-biomas.mjs`
- Create: `web/src/data/biomas.json` (salida del script)

- [ ] **Step 1: Escribir `web/scripts/gen-biomas.mjs`**

```js
// gen-biomas.mjs — mapea cada especie a un bioma (hierba/agua/cueva) por su habitat en PokeAPI.
// Salida: web/src/data/biomas.json {id: "hierba"|"agua"|"cueva"}. Correr: node scripts/gen-biomas.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'biomas.json');
const MAX = 721;
const get = async (u) => {
  for (let i = 0; i < 4; i++) { try { const r = await fetch(u); if (r.ok) return r.json(); } catch {} await new Promise((s) => setTimeout(s, 400 * (i + 1))); }
  throw new Error('fallo ' + u);
};
const BIOMA = (hab) => hab === 'waters-edge' || hab === 'sea' ? 'agua' : hab === 'cave' ? 'cueva' : 'hierba';

const out = {};
for (let id = 1; id <= MAX; id++) {
  const sp = await get(`https://pokeapi.co/api/v2/pokemon-species/${id}`);
  out[id] = BIOMA(sp.habitat && sp.habitat.name);
  if (id % 50 === 0) console.log('… biomas', id);
}
fs.writeFileSync(OUT, JSON.stringify(out));
const c = Object.values(out).reduce((a, b) => ((a[b] = (a[b] || 0) + 1), a), {});
console.log('✓ biomas.json', Object.keys(out).length, 'especies', JSON.stringify(c));
```

- [ ] **Step 2: Correr el script** (desde `web/`): `node scripts/gen-biomas.mjs`
Expected: crea `web/src/data/biomas.json` (~721 entradas). Loguea el conteo por bioma. (Si PokeAPI falla por red, reintentar.)

- [ ] **Step 3: Verificar la forma**:
```
cd web && node -e "const b=require('./src/data/biomas.json'); console.log('n', Object.keys(b).length, '| ej 1:', b['1'], '| 7:', b['7'], '| 74:', b['74'])"
```
Expected: `n 721 | ej 1: hierba | 7: agua | 74: cueva` (Bulbasaur=hierba, Squirtle=agua, Geodude=cueva; valores reales pueden variar según habitat).

- [ ] **Step 4: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/scripts/gen-biomas.mjs web/src/data/biomas.json
git commit -m "data: biomas.json (hierba/agua/cueva por habitat de PokeAPI)"
```

---

### Task 3: `coleccion.js` — racha, bioma/hora en el encuentro, tamaños, dusk en ctx

**Files:**
- Modify: `web/src/lib/coleccion.js`

- [ ] **Step 1: Imports.** Agregar arriba (junto a los otros `with { type: 'json' }`):
```js
import biomas from '../data/biomas.json' with { type: 'json' };
```
Y al import de `./safari-core.js` agregar `shinyChance, pisoRacha, esNoche, biomaActual, rolarTam`:
```js
import { probCaptura, pisoIV, fleeProb, sincronizaNat, shinyChance, pisoRacha, esNoche, biomaActual, rolarTam } from './safari-core.js';
```

- [ ] **Step 2: Helpers de racha** — agregar cerca de los otros helpers de safari (después de `setCompanero`):
```js
// racha de capturas seguidas (sube odds de shiny / IVs). col:racha.
export const racha = () => get('col:racha', 0);
export const subirRacha = () => { const n = get('col:racha', 0) + 1; set('col:racha', n); return n; };
export const romperRacha = () => set('col:racha', 0);
```

- [ ] **Step 3: `BALL_KEYS` gana `dusk`.** Buscar la línea `const BALL_KEYS = [...]` y agregar `'dusk'` (antes de `'master'`):
```js
const BALL_KEYS = ['pokeball', 'superball', 'ultraball', 'veloz', 'turno', 'red', 'repeticion', 'dusk', 'xeneize', 'master'];
```

- [ ] **Step 4: Reescribir `encontrar`** (filtro de bioma + fallback, shiny por racha, IVs perfectos = max(alfa, racha), tam, devuelve bioma/noche). Reemplazar la función entera:
```js
export function encontrar(pokemon, temas, pesos = {}) {
  const regiones = regionesDesbloqueadas(temas);
  const enRegion = pokemon.filter((p) => regiones.has(p.region));
  if (!enRegion.length) return { error: 'vacio' };
  const bioma = biomaActual(), noche = esNoche();
  // filtro por bioma; si el bioma no tiene especies acá, cae al pool completo
  const delBioma = enRegion.filter((p) => (biomas[String(p.id)] || 'hierba') === bioma);
  const pool = delBioma.length ? delBioma : enRegion;
  const elegido = elegirPonderado(pool, pesos);
  const id = elegido.id;
  const idn = rolarIdentidad(id, habilidades);
  const comp = companero();
  if (comp) { const ci = identidadCore(comp, _DATOS_ID); const ns = sincronizaNat(ci.hab, ci.nat); if (ns != null) idn.nat = ns; }
  const alfa = Math.random() < PROB_ALFA;
  const nPerf = Math.max(alfa ? 3 : 0, pisoRacha(racha()));
  const ivs = nPerf ? forzarPerfectos(idn.ivs, nPerf) : idn.ivs;
  const tam = alfa ? 'XL' : rolarTam();
  return {
    id, nivel: nivelWild(id), ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen,
    shiny: Math.random() < shinyChance(racha()), alfa, tam,
    rarezaTier: tierDe(id, aparicion).nivel, estrellas: ivEstrellas(ivs),
    naturalezaNombre: NATURALEZAS[idn.nat].nombre,
    tiposWild: tipos[String(id)] || [], vistoYa: vistos().has(id),
    bioma, noche, pokemon: elegido,
  };
}
```

- [ ] **Step 5: `capturar`** — pasar `noche`/`bioma` al ctx + subir/romper racha + guardar tam. Reemplazar:
```js
export function capturar(enc, ballKey, calidad = 'Normal', extra = {}) {
  if (!tieneBall(ballKey)) return { error: 'sin-ball' };
  consumirBall(ballKey);
  const ballDef = { key: ballKey, ...ITEMS[ballKey] };
  const tiroN = extra.tiroN || 1;
  const ctx = { tiroN, calidad, tiposWild: enc.tiposWild, vistoYa: enc.vistoYa, noche: enc.noche, bioma: enc.bioma };
  const prob = probCaptura(enc.rarezaTier, ballDef, ctx);
  if (Math.random() < prob) {
    const ivs = pisoIV(enc.ivs, calidad);
    const inst = atrapar(enc.id, { shiny: enc.shiny, nivel: enc.nivel, alfa: enc.alfa, tam: enc.tam, ivs, nat: enc.nat, hab: enc.hab, gen: enc.gen });
    const nracha = subirRacha();
    return { ok: true, inst, prob, calidad, ball: ballKey, racha: nracha };
  }
  const huyo = Math.random() < fleeProb(enc.rarezaTier);
  if (huyo) romperRacha();
  return { ok: false, huyo, prob, calidad, ball: ballKey, racha: racha() };
}
```

- [ ] **Step 6: `atrapar`** — aceptar y guardar `tam`. Reemplazar la firma + creación del inst:
```js
export function atrapar(id, { shiny = false, nivel = 1, alfa = false, tam = 'M', ivs = null, nat = null, hab = null, gen = null } = {}) {
  id = Number(id);
  const idn = (ivs && nat != null) ? { ivs, nat, hab, gen } : rolarIdentidad(id, habilidades);
  const inst = { iid: _uid(), id, nivel, exp: 0, shiny, movs: [], creado: Date.now(),
    ivs: idn.ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen, evs: [0, 0, 0, 0, 0, 0],
    ...(alfa ? { alfa: true } : {}), ...(tam && tam !== 'M' ? { tam } : {}) };
```
(El resto de `atrapar` —`pc().push`, `setPC`, `addVisto`, `addCaramelos`, `return inst`— igual.)

- [ ] **Step 7: Smoke-test** (best-effort):
```
cd web && node --input-type=module -e "import('./src/lib/coleccion.js').then(m=>console.log('ok', typeof m.encontrar, typeof m.subirRacha, typeof m.racha)).catch(e=>console.log('ERR', e.message))"
```
Ideal: `ok function function function`. Si imprime `ERR` por `localStorage`/DOM o por el import-attribute de `habilidades.json`/`yields.json` (preexistente bajo node crudo), es aceptable — la validación real es el build (Task 5). No corras `npm run build` todavía (la UI vieja del safari aún no usa lo nuevo; igual compila, pero el flujo se cierra en Task 5).

- [ ] **Step 8: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/coleccion.js
git commit -m "coleccion: racha (shiny/IV), filtro de bioma + hora en el encuentro, tamaños, dusk en ctx"
```

---

### Task 4: Dusk Ball — item + sprite

**REQUIRED SUB-SKILL:** `/frontend-design` para el sprite (coherente con la familia de balls).

**Files:**
- Modify: `web/src/lib/items.js`
- Modify: `web/src/lib/sprites.js`

- [ ] **Step 1: Item Dusk Ball** en `items.js` (en la sección `'ball'`, después de `xeneize`):
```js
  dusk: { nombre: 'Dusk Ball', sprite: 'balldusk', cat: 'ball', cond: 'dusk', precio: 35, desc: '×3.5 de captura de noche o en cueva.' },
```

- [ ] **Step 2: Sprite `balldusk`** en `sprites.js`: agregar la variante en el mapa de `ballSvg` (o en `itemSvg` según cómo se hizo el roster de Fase 1) — **Dusk Ball**: cúpula verde oscuro/negra con un círculo rojo/luna. Mapear `itemSvg('balldusk', …)`. Mantener contorno/brillo de la familia. Verificar junto a las otras (screenshot rápido con Playwright, como en Fase 1).

- [ ] **Step 3: Verificar**: `cd web && node -e "import('./src/lib/sprites.js').then(m=>console.log(m.itemSvg('balldusk',24).length>50))"` → `true`.

- [ ] **Step 4: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/items.js web/src/lib/sprites.js
git commit -m "items+sprites: Dusk Ball (×3.5 noche/cueva)"
```

---

### Task 5: `safari.astro` + `global.css` — badges (racha/bioma/hora) + resumen + Huir rompe racha

**REQUIRED SUB-SKILL:** `/frontend-design`. Tema-aware, estética CRT/FireRed.

**Files:**
- Modify: `web/src/pages/safari.astro`
- Modify: `web/src/styles/global.css`

- [ ] **Step 1: Importar lo nuevo** de `coleccion.js`: agregar `racha, romperRacha` (y, de `safari-core.js` via coleccion no se exponen; usar `biomaActual, esNoche` importándolos de `../lib/safari-core.js`) — agregá `import { biomaActual, esNoche } from '../lib/safari-core.js';`.

- [ ] **Step 2: Badge de ambiente + racha.** En la barra `.safari-barra` (línea ~22), agregar un `.ss-item` para la racha:
```html
<div class="ss-item ss-racha" id="ss-racha" hidden><span class="ss-ico">🔥</span><b id="rachaN">0</b><span class="ss-lbl">Racha</span></div>
```
Y bajo `.safari-barra`, un strip de ambiente:
```html
<div class="safari-amb" id="amb"></div>
```
En `refrescar()` (donde se setea `#balls`), actualizar también:
```js
const rN = racha();
$('ss-racha').hidden = rN < 1;
$('rachaN').textContent = rN;
const b = biomaActual(), noche = esNoche();
const BIOMAS = { hierba: '🌿 Hierba', agua: '💧 Agua', cueva: '🪨 Cueva' };
$('amb').innerHTML = '<span class="amb-chip">' + BIOMAS[b] + '</span><span class="amb-chip">' + (noche ? '🌙 Noche' : '☀️ Día') + '</span>';
```
Y agregar un `setInterval(refrescar, 30000)` (cerca del init) para que bioma/hora se actualicen solos. (Importar `racha` de coleccion.)

- [ ] **Step 3: Huir rompe la racha.** En el handler de `#enc-huir` (`renderCarta`), antes de `renderCarta()`:
```js
$('enc-huir').addEventListener('click', () => { romperRacha(); enc = null; $('msg').textContent = 'Te alejaste sin tirar. 🌿'; refrescar(); renderCarta(); });
```

- [ ] **Step 4: Resumen muestra racha + tamaño.** En `resumenCaptura`, agregar a la tarjeta:
  - si `r.racha >= 2`: una línea "🔥 Racha ×N" (cuanto más alta, color más cálido).
  - tamaño/título: si `enc.tam` ∈ {'XXS','XXL','XL'} o alfa → mostrar título ("👑 Coloso" para XL/XXL, "🔬 Mini" para XXS) y escalar el sprite del salvaje (`.cap-r-sprite`/el sprite que muestre) ×1.18 (XL/XXL) o ×0.82 (XXS). Si querés, mostrar `enc.tam` como chip.
  Usar `/frontend-design` para el estilo. Si la captura **rompe** record de racha, un detalle visual.

- [ ] **Step 5: Mensaje de racha rota** (zafó vs huyó): en `tirar()`, en la rama `r.huyo`, sumar al mensaje "💔 Se cortó la racha". (La racha ya se rompió en `capturar`.)

- [ ] **Step 6: Estilos** en `global.css`: `.ss-racha`, `.safari-amb`/`.amb-chip`, las líneas de racha/tamaño del resumen, escalado del sprite por tamaño. Tema-aware.

- [ ] **Step 7: Build + screenshot** (Playwright, como en Fase 1): badges de ambiente + racha, resumen con racha/tamaño. `cd web && npm run build` → OK.

- [ ] **Step 8: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/safari.astro web/src/styles/global.css docs
git commit -m "safari: badges de racha/bioma/hora + resumen con racha y tamaño; Huir rompe la racha"
```

---

### Task 6: `pokedex.astro` — chip de tamaño en el modal

**Files:**
- Modify: `web/src/pages/pokedex.astro`

- [ ] **Step 1: Mostrar el tamaño.** En el modal de instancia (donde están los chips de género/shiny/alfa — helpers `generoChip`/`alfaChip`), agregar un `tamChip(m)`:
```js
const TAM_LBL = { XXS: '🔬 XXS', S: 'S', L: 'L', XL: '🔶 XL', XXL: '👑 XXL' };
const tamChip = (m) => (m && m.tam && m.tam !== 'M') ? '<span class="id-tam" title="Tamaño del ejemplar">' + (TAM_LBL[m.tam] || m.tam) + '</span>' : '';
```
Renderizarlo junto a `generoChip(idn.gen) + alfaChip(m)` en el header del panel y/o en la línea del nombre. CSS `.id-tam` (tema-aware, chip sutil) en `global.css`.

- [ ] **Step 2: Build + Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/pokedex.astro web/src/styles/global.css docs
git commit -m "pokedex: chip de tamaño del ejemplar en el modal"
```

---

### Task 7: `tienda.astro` — Dusk Ball a la venta

**Files:**
- Modify: `web/src/pages/tienda.astro` (verificar; quizá no haga falta editar)

- [ ] **Step 1: Verificar render.** La cat `'ball'` ya itera `!it.noVenta`. La Dusk Ball (sin `noVenta`) debería aparecer sola con su `itemSvg(it.sprite,…)`, precio y desc. Confirmar con un grep del HTML buildeado que `dusk`/`Dusk Ball` aparece en `docs/tienda/index.html` y que el sprite `balldusk` renderiza (no el comodín). Si la tienda mapea sprites con un caso especial (como pasó con las balls de Fase 1), agregar `balldusk` ahí. Si ya fluye por `it.sprite`, no tocar nada.

- [ ] **Step 2: Build + Commit** (si hubo cambios; si no, saltar):
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/tienda.astro docs
git commit -m "tienda: Dusk Ball a la venta"
```

---

### Task 8: `ayuda.astro` + verificación final

**Files:**
- Modify: `web/src/pages/ayuda.astro`

- [ ] **Step 1: Documentar Fase 2** en `ayuda.astro` (estilo existente, links `u('/...')`): la **racha** (capturas seguidas → más shiny + mejores IVs; se corta si uno huye), los **biomas y la hora** (rotan solos; aparecen distintos Pokémon; de noche/en cueva conviene la **Dusk Ball**), y los **tamaños** (los alfa salen grandes).

- [ ] **Step 2: Verificación final**:
- `cd web && node --test src/lib/safari-core.test.mjs` → todas verdes (pegá el resumen).
- `cd web && npm run build` → OK.
- `cd api && npx jest` → sin regresiones (el motor no se tocó).
- E2E manual (dev): la racha sube al capturar y se ve el badge; al huir se corta; el badge de bioma/hora cambia (probá biomaActual con el reloj); la Dusk Ball aparece en la tienda; un alfa se ve grande con título; el chip de tamaño en el modal.

- [ ] **Step 3: Commit final**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/ayuda.astro docs
git commit -m "docs: ayuda al día con Safari Fase 2 (racha, biomas/hora, Dusk Ball, tamaños)"
```

---

## Notas para el ejecutor

- **`node --test`** es el runner de la lógica pura (sin deps nuevas). El motor de combate (`combate-core.ts`/
  jest) NO se toca en esta fase.
- **`biomas.json`** se baja una vez (Task 2, red a PokeAPI). Si falta un id → tratar como `'hierba'`.
- **Bioma/hora** son deterministas por el reloj real: para testear visualmente un bioma puntual, podés
  cambiar la hora del sistema o stubear `Date.now()` en el browser; en prod rota solo.
- **Shiny en el encuentro:** desde Fase 1 el shiny se decide y se revela al aparecer; la racha solo cambia
  la probabilidad en `encontrar` (no en el tiro).
- **Sin atribución Claude** en los commits.
```
