# Safari profundo — Fase 1 · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reemplazar la captura automática del safari por un encuentro en 2 pasos con tasación, selector de Pokéball, minijuego de tiro (anillo) y escape escalado por rareza.

**Architecture:** La matemática pura (captura/escape/tasación) vive en un módulo nuevo `web/src/lib/safari-core.js` (sin DOM/JSON), testeado con el runner nativo de Node. `coleccion.js` orquesta estado (`encontrar`/`capturar`/`companero`) reusando `safari-core` + la identidad ya existente. `safari.astro` (UI) pasa al flujo de 2 pasos. Las balls se vuelven datos (`items.js`) con modificador `catch`/condición; `BALL_BOOST`/`mejorBallTier` se retiran.

**Tech Stack:** JS módulos (ES), Astro, `node --test` (runner nativo, sin deps nuevas), SVG sprites, /frontend-design para UI.

**Convención:** specs/plans en `superpowers/` (raíz). Sin atribución Claude en commits. UI/visual → `/frontend-design`. Links internos con `u('/ruta')`. Spec: `superpowers/specs/2026-06-07-safari-profundo-fase1-design.md`.

**Contexto de datos existente:**
- `col:balls` = contador ÚNICO de Poké Ball básica (se gana con ejercicios). Super/Ultra = items en `col:items`.
- `items.js`: `superball`(tier1), `ultraball`(tier2) en cat `'ball'`; `BALL_BOOST` (se retira).
- `coleccion.js`: `tirar()` auto-captura (se reemplaza); `atrapar(id,{shiny,nivel})` rolea identidad adentro;
  `mejorBallTier()`, `usarItem()`, `items()`, `vistos()`, `tierDe(id, aparicion)`, `nivelWild(id)`,
  `regionesDesbloqueadas`, `elegirPonderado`, `identidad as identidadCore`, `ivEstrellas`, `NATURALEZAS`, `PROB_SHINY`.
- `sprites.js`: `ballSvg(tier,size)` (0/1/2); `itemSvg` mapea `ball1→ballSvg(1)` etc.
- `safari.astro`: importa `tirar as lanzar`; renderiza arena + captura.

---

### Task 1: `safari-core.js` — lógica pura + tests (`node --test`)

**Files:**
- Create: `web/src/lib/safari-core.js`
- Test: `web/src/lib/safari-core.test.mjs`

- [ ] **Step 1: Escribir el test (FALLA primero)** — `web/src/lib/safari-core.test.mjs`

```js
import test from 'node:test';
import assert from 'node:assert/strict';
import { probCaptura, pisoIV, sincronizaNat, fleeProb, baseCaptura, catchBall } from './safari-core.js';

const poke = { key: 'pokeball', catch: 1 };
const ultra = { key: 'ultraball', catch: 2 };
const master = { key: 'master' };
const veloz = { key: 'veloz' };
const turno = { key: 'turno' };
const red = { key: 'red' };
const repe = { key: 'repeticion' };
const ctx = (o = {}) => ({ tiroN: 1, calidad: 'Normal', tiposWild: [], vistoYa: false, ...o });

test('baseCaptura: comunes alto, legendarios bajo, piso 0.12', () => {
  assert.ok(baseCaptura(1) > baseCaptura(10));
  assert.ok(baseCaptura(10) >= 0.12);
});
test('probCaptura: Ultra > Poké', () => {
  assert.ok(probCaptura(5, ultra, ctx()) > probCaptura(5, poke, ctx()));
});
test('probCaptura: mejor calidad sube', () => {
  assert.ok(probCaptura(5, poke, ctx({ calidad: 'Excelente' })) > probCaptura(5, poke, ctx({ calidad: 'Normal' })));
});
test('probCaptura: Master = 1', () => {
  assert.equal(probCaptura(10, master, ctx()), 1);
});
test('probCaptura: clamp 0..1', () => {
  const p = probCaptura(1, ultra, ctx({ calidad: 'Excelente' }));
  assert.ok(p <= 1 && p >= 0);
});
test('Veloz: ×4 primer tiro, ×1 luego', () => {
  assert.equal(catchBall(veloz, ctx({ tiroN: 1 })), 4);
  assert.equal(catchBall(veloz, ctx({ tiroN: 2 })), 1);
});
test('Turno: escala con tiroN', () => {
  assert.ok(catchBall(turno, ctx({ tiroN: 3 })) > catchBall(turno, ctx({ tiroN: 1 })));
});
test('Red: ×3 vs Bicho/Agua, ×1 si no', () => {
  assert.equal(catchBall(red, ctx({ tiposWild: ['Agua'] })), 3);
  assert.equal(catchBall(red, ctx({ tiposWild: ['Fuego'] })), 1);
});
test('Repetición: ×3 si visto', () => {
  assert.equal(catchBall(repe, ctx({ vistoYa: true })), 3);
  assert.equal(catchBall(repe, ctx({ vistoYa: false })), 1);
});
test('pisoIV: Excelente sube los 2 más bajos a 31', () => {
  assert.deepEqual(pisoIV([5, 20, 2, 30, 31, 10], 'Excelente'), [31, 20, 31, 30, 31, 10]);
});
test('pisoIV: otras calidades no tocan', () => {
  assert.deepEqual(pisoIV([5, 20, 2, 30, 31, 10], 'Genial'), [5, 20, 2, 30, 31, 10]);
});
test('sincronizaNat: synchronize → nat del compañero; otra → null', () => {
  assert.equal(sincronizaNat('synchronize', 7), 7);
  assert.equal(sincronizaNat('overgrow', 7), null);
});
test('fleeProb: crece con la rareza, en [0.1, 0.5]', () => {
  assert.ok(fleeProb(10) > fleeProb(1));
  assert.ok(fleeProb(1) >= 0.1 && fleeProb(10) <= 0.5);
});
```

- [ ] **Step 2: Correr el test (debe fallar)**

Run: `cd web && node --test src/lib/safari-core.test.mjs`
Expected: FAIL (`Cannot find module './safari-core.js'`).

- [ ] **Step 3: Implementar `web/src/lib/safari-core.js`**

```js
// safari-core.js — lógica PURA del safari (captura / escape / tasación). Sin DOM, sin JSON, sin estado.
// Testeable con `node --test src/lib/safari-core.test.mjs`. La orquestación (estado) vive en coleccion.js.

export const MULT_CALIDAD = { Normal: 1.0, Bien: 1.3, Genial: 1.7, Excelente: 2.2 };

// captura base por tier de rareza (1..10): comunes alto, legendarios bajo.
export const baseCaptura = (tier) => Math.max(0.12, Math.min(0.95, 1.0 - tier * 0.08));

// modificador de captura de la ball (puede depender del contexto del encuentro).
// ctx = { tiroN, calidad, tiposWild: string[], vistoYa: boolean }
export function catchBall(ballDef, ctx) {
  switch (ballDef.key) {
    case 'master': return Infinity;
    case 'veloz': return ctx.tiroN === 1 ? 4 : 1;
    case 'turno': return 1 + ctx.tiroN * 0.3;
    case 'red': return (ctx.tiposWild || []).some((t) => t === 'Bicho' || t === 'Agua') ? 3 : 1;
    case 'repeticion': return ctx.vistoYa ? 3 : 1;
    default: return ballDef.catch ?? 1;   // poke 1, super 1.5, ultra 2, xeneize 2
  }
}

// probabilidad de captura [0..1]. Master = 1.
export function probCaptura(tier, ballDef, ctx) {
  if (ballDef.key === 'master') return 1;
  const mult = MULT_CALIDAD[ctx.calidad] ?? 1;
  const p = baseCaptura(tier) * catchBall(ballDef, ctx) * mult;
  return Math.max(0, Math.min(1, p));
}

// prob. de huida tras un fallo (raros huyen más), acotada a [0.1, 0.5].
export const fleeProb = (tier) => Math.max(0.10, Math.min(0.5, 0.10 + tier * 0.035));

// piso de IVs por Excelente: los 2 índices con menor IV → 31. Devuelve copia.
export function pisoIV(ivs, calidad) {
  if (calidad !== 'Excelente') return ivs.slice();
  const out = ivs.slice();
  const orden = out.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
  for (let k = 0; k < 2; k++) out[orden[k][1]] = 31;
  return out;
}

// Sincronía (pura): hab y nat del compañero → nat o null.
export const sincronizaNat = (compHab, compNat) => compHab === 'synchronize' ? compNat : null;
```

- [ ] **Step 4: Correr el test (debe pasar)**

Run: `cd web && node --test src/lib/safari-core.test.mjs`
Expected: PASS (todas).

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/safari-core.js web/src/lib/safari-core.test.mjs
git commit -m "safari-core: lógica pura de captura/escape/tasación + tests (node --test)"
```

---

### Task 2: `items.js` — roster de balls + retiro de `BALL_BOOST`

**Files:**
- Modify: `web/src/lib/items.js`

- [ ] **Step 1: Reescribir la sección `// ── Pokeballs ──`** con el roster nuevo (cada ball lleva `catch`/`cond`; `pokeball` es metadata del contador `col:balls`, `noVenta:true`):

```js
  // ── Pokeballs ── (la captura depende de `catch`/condición; ver safari-core.catchBall)
  pokeball:   { nombre: 'Poké Ball',  sprite: 'ball0', cat: 'ball', tier: 0, catch: 1,   noVenta: true, desc: 'La de siempre. Se gana resolviendo ejercicios. Captura estándar.' },
  superball:  { nombre: 'Super Ball', sprite: 'ball1', cat: 'ball', tier: 1, catch: 1.5, precio: 25, desc: 'Captura mejorada (×1.5). Para los que zafan un poco.' },
  ultraball:  { nombre: 'Ultra Ball', sprite: 'ball2', cat: 'ball', tier: 2, catch: 2,   precio: 60, desc: 'Captura premium (×2). Para los raros.' },
  veloz:      { nombre: 'Ball Veloz',      sprite: 'ballveloz',    cat: 'ball', cond: 'veloz',      precio: 25, desc: '×4 de captura si la tirás apenas aparece (primer tiro).' },
  turno:      { nombre: 'Ball Turno',      sprite: 'ballturno',    cat: 'ball', cond: 'turno',      precio: 25, desc: 'Mejora cuantos más tiros llevás en el encuentro.' },
  red:        { nombre: 'Ball Red',        sprite: 'ballred',      cat: 'ball', cond: 'red',        precio: 30, desc: '×3 de captura contra Pokémon de tipo Bicho o Agua.' },
  repeticion: { nombre: 'Ball Repetición', sprite: 'ballrepe',     cat: 'ball', cond: 'repeticion', precio: 30, desc: '×3 si ya tenés esa especie en la Pokédex.' },
  master:     { nombre: 'Master Ball',     sprite: 'ballmaster',   cat: 'ball', catch: 'master',    precio: 5000, desc: 'Captura 100% garantizada. Carísima: guardala para EL Pokémon.' },
  xeneize:    { nombre: 'Ball Xeneize',    sprite: 'ballxeneize',  cat: 'ball', catch: 2, boca: true, precio: 80, desc: '💙💛 Edición Boca. Captura premium (×2) + festejo azul y oro al atrapar.' },
```
(Borrar las entradas viejas `superball`/`ultraball` que tenían `ico`/desc de boost — quedan reemplazadas arriba.)

- [ ] **Step 2: Borrar `BALL_BOOST`**

Eliminar el bloque `export const BALL_BOOST = { ... };` (las 5 líneas). Quedará sin usar tras Task 3.

- [ ] **Step 3: Verificar que el front sigue compilando (parcial)**

Run: `cd web && node -e "import('./src/lib/items.js').then(m=>console.log('balls:', Object.values(m.ITEMS).filter(i=>i.cat==='ball').length, 'BALL_BOOST:', m.BALL_BOOST))"`
Expected: `balls: 9 BALL_BOOST: undefined`. (Aún NO buildear: `coleccion.js` todavía importa `BALL_BOOST` → Task 3 lo arregla.)

- [ ] **Step 4: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/items.js
git commit -m "items: roster de balls (Veloz/Turno/Red/Repetición/Master/Xeneize) + catch por ball; retira BALL_BOOST"
```

---

### Task 3: `coleccion.js` — `encontrar`/`capturar`/`companero` + `atrapar` extendido

**Files:**
- Modify: `web/src/lib/coleccion.js`

- [ ] **Step 1: Ajustar imports** (arriba del archivo)

- Quitar `BALL_BOOST` del import de `./items.js` → queda `import { ITEMS } from './items.js';`
- Agregar:
```js
import tipos from '../data/tipos.json' with { type: 'json' };
import { probCaptura, pisoIV, fleeProb, sincronizaNat } from './safari-core.js';
```
(Verificá que `identidad as identidadCore`, `NATURALEZAS`, `rolarIdentidad`, `ivEstrellas` ya estén importados/definidos — lo están desde la feature de identidad. `_DATOS_ID` ya existe.)

- [ ] **Step 2: Extender `atrapar`** para aceptar identidad + alfa ya roleados

Reemplazar la firma + las primeras líneas de `atrapar`:
```js
export function atrapar(id, { shiny = false, nivel = 1, alfa = false, ivs = null, nat = null, hab = null, gen = null } = {}) {
  id = Number(id);
  const idn = (ivs && nat != null) ? { ivs, nat, hab, gen } : rolarIdentidad(id, habilidades);
  const inst = { iid: _uid(), id, nivel, exp: 0, shiny, movs: [], creado: Date.now(),
    ivs: idn.ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen, evs: [0, 0, 0, 0, 0, 0], ...(alfa ? { alfa: true } : {}) };
```
(El resto del cuerpo de `atrapar` — `pc().push`, `setPC`, vistos, caramelos, `return inst` — queda IGUAL.)

- [ ] **Step 3: Reemplazar `tirar` por inventario de balls + `companero` + `encontrar` + `capturar`**

Borrar la función `tirar` entera y la función `mejorBallTier` (solo las usaba `tirar`). Agregar en su lugar:
```js
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
```
(Si quedó algún `export { tirar }` o referencia, eliminarla. `aparicion` ya está importado en coleccion.js.)

- [ ] **Step 4: Verificar imports/compilación**

Run: `cd web && node -e "import('./src/lib/coleccion.js').then(m=>console.log('ok', typeof m.encontrar, typeof m.capturar, typeof m.inventarioBalls, typeof m.setCompanero))"`
Expected: `ok function function function function`. (Si falla por DOM/localStorage en node, en su defecto correr `cd web && npm run build` tras Task 5; ver nota.)

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/coleccion.js
git commit -m "coleccion: encontrar/capturar (encuentro 2 pasos) + inventario de balls + compañero; atrapar acepta identidad/alfa"
```

---

### Task 4: `sprites.js` — variantes de `ballSvg` (`/frontend-design`)

**REQUIRED SUB-SKILL:** Use `/frontend-design` para los sprites (fieles + coherentes con la familia de balls; mismo contorno/brillo). Regla CLAUDE.md: balls = SVG, no emoji.

**Files:**
- Modify: `web/src/lib/sprites.js`

- [ ] **Step 1: Extender `ballSvg` + `itemSvg`** para soportar las variantes nuevas

Leé `ballSvg(tier, size)` y `itemSvg`. Agregá variantes para: `ball0` (Poké, ya = tier0), `ballveloz`, `ballturno`, `ballred`, `ballrepe`, `ballmaster`, `ballxeneize`. Opciones: (a) extender `ballSvg` para aceptar una clave string además del tier, o (b) agregar casos en `itemSvg` que devuelvan SVGs propios. Cada una mantiene la silueta de Pokéball con su color/diseño:
- Veloz: azul con rayos amarillos. Turno: con marcas/relojito. Red: azul/celeste con red. Repetición: con flechas de repetir. Master: morada con la "M" y dos puntos rosas. Xeneize: **azul (#0a2e6b) con banda amarilla/oro (#f2c200)** — colores de Boca.
- Mapear en `itemSvg`: `ball0→Poké`, `ballveloz→veloz`, …, `ballxeneize→xeneize`, manteniendo el fallback existente (`ball1→ballSvg(1)`, `ball2→ballSvg(2)`).

Verificá el set junto (screenshot, ver Task 8) para que se vea coherente.

- [ ] **Step 2: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/sprites.js
git commit -m "sprites: variantes de Pokéball (Veloz/Turno/Red/Repetición/Master/Xeneize)"
```

---

### Task 5: `safari.astro` + `global.css` — UI de encuentro en 2 pasos (`/frontend-design`)

**REQUIRED SUB-SKILL:** Use `/frontend-design`. Tema-aware (oscuro/claro), estética retro-Pokédex/CRT/FireRed, cohesiva.

**Files:**
- Modify: `web/src/pages/safari.astro`
- Modify: `web/src/styles/global.css`

- [ ] **Step 1: Reemplazar el flujo de captura por 2 pasos**

Leé `safari.astro`. Hoy importa `tirar as lanzar` y al click captura. Cambiar a:
- Importar de `coleccion.js`: `encontrar, capturar, inventarioBalls, tieneBall, companero, setCompanero, identidadDe, naturalezaDe, habMeta, ivPct, ivEstrellas`. Quitar `lanzar`/`tirar`.
- **Estado local del encuentro:** `let enc = null; let tiroN = 0; let ballSel = null;`.
- **Botón "Buscá en el pasto"** → llama `encontrar(D.pokemon, D.temas, D.pesos)` (los `pesos` de rareza ya se calculan en la página o vienen de `D`; reusar la fuente actual de `pesos`). Si `{error:'vacio'}` → mensaje. Si OK → guardar `enc`, `tiroN=0`, renderizar la **carta de encuentro**.
- **Carta de encuentro:** sprite (usar `spriteUrl(enc.id, enc.shiny)`, clase shiny si `enc.shiny`, aura/👑 si `enc.alfa`), nombre, `Nv enc.nivel`, **⭐ tasación** (`enc.estrellas` de 0-4, mostrar ★/☆), `enc.naturalezaNombre`. **Selector de balls:** `inventarioBalls().map(...)` → chips con `itemSvg(meta.sprite, 26)` + contador `×n`; al tocar uno setea `ballSel=b.key`. Botones **Tirar** (deshabilitado si `!ballSel`) y **Huir** (`enc=null`, volver a la arena).
- **Tirar** → abre el **overlay de tiro** (Step 2). Al resolver la calidad: `tiroN++`, `const r = capturar(enc, ballSel, calidad, { tiroN })`.
  - `r.ok` → animación de captura (reusar las estrellas/FX existentes; si la ball es `xeneize` → confeti azul-oro; shiny/alfa → FX épico). Mostrar resultado con `r.inst` (reusar `capIdentidad(r.inst)` que ya existe). `enc=null`.
  - `!r.ok && r.huyo` → "¡Huyó!" → `enc=null`.
  - `!r.ok && !r.huyo` → "¡Zafó! Probá de nuevo." → quedarse en la carta (otra ball; `tiroN` ya subió).
  - `r.error==='sin-ball'` → mensaje "No te quedan de esa ball".
- **Selector de compañero:** un control (botón "Compañero: X" que abre un mini-selector del PC) que llama `setCompanero(iid)`; mostrar el compañero actual (`companero()`), y si tiene Sincronía aclarar "fija la naturaleza".

- [ ] **Step 2: Minijuego de anillo (en `safari.astro`)**

Implementá el **anillo que se contrae**: un overlay sobre el sprite del salvaje con un aro SVG/CSS que se cierra desde grande hasta un radio mínimo en ~1.1s (loop o una pasada). Al tap/click se mide qué tan cerca está del anillo-blanco:
- Excelente (muy cerca del centro), Genial, Bien, Normal (si no tocás a tiempo / lejos). Mapear el radio al label de calidad (umbrales en código). Mostrar el label con feedback (color/sonido reusando `sonidos.js` si aplica). Devolver la `calidad` al flujo de Step 1.
- Mobile-first: el tap en cualquier parte del overlay cuenta. Accesible (un botón "¡Tirá!" también sirve).

- [ ] **Step 3: Estilos en `global.css`**

Agregar clases para: carta de encuentro, ⭐ tasación, chips del selector de balls (seleccionado/disabled), overlay + anillo del minijuego, marca alfa (aura), resultado. Tema-aware. Confeti azul-oro para Xeneize.

- [ ] **Step 4: Build + screenshot (ver Task 8 para verificación visual conjunta)**

Run: `cd web && npm run build` → OK.

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/safari.astro web/src/styles/global.css docs
git commit -m "safari: encuentro en 2 pasos (carta + selector de balls + minijuego de anillo + escape)"
```

---

### Task 6: `pokedex.astro` — marca alfa en el modal

**Files:**
- Modify: `web/src/pages/pokedex.astro`

- [ ] **Step 1: Mostrar 👑 alfa** en el modal de instancia

En el panel de Identidad / encabezado del modal (donde ya se muestran género ♂/♀ y shiny), agregar la marca **alfa 👑** cuando `inst.alfa` sea true (junto al nombre). Estilo coherente con las marcas existentes (chip/badge). Usar `/frontend-design` si requiere diseño.

- [ ] **Step 2: Build + Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/pokedex.astro web/src/styles/global.css docs
git commit -m "pokedex: marca alfa 👑 en el modal de instancia"
```

---

### Task 7: `tienda.astro` — balls nuevas en venta

**Files:**
- Modify: `web/src/pages/tienda.astro`

- [ ] **Step 1: Renderizar las balls vendibles**

La cat `'ball'` ya se renderiza. Asegurar que: (a) las balls nuevas (veloz/turno/red/repeticion/master/xeneize, super/ultra) aparezcan con su sprite (`itemSvg(it.sprite, …)`), precio y desc; (b) la `pokeball` (`noVenta:true`) **NO** se liste a la venta. Si el render itera `itemsPorCat('ball')`/`porCat('ball')`, filtrar `!it.noVenta`. Verificar que la Master (precio 5000) y Xeneize se vean bien.

- [ ] **Step 2: Build + Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/tienda.astro docs
git commit -m "tienda: balls especiales en venta (Veloz/Turno/Red/Repetición/Master/Xeneize), Poké Ball no se vende"
```

---

### Task 8: `ayuda.astro` + verificación visual + final

**Files:**
- Modify: `web/src/pages/ayuda.astro`
- Verify: screenshots (dev server, `/frontend-design` tooling)

- [ ] **Step 1: Documentar el Safari profundo en `ayuda.astro`**

Sección nueva (estilo existente, español argentino, links con `u('/...')`): cómo funciona el encuentro (aparece el salvaje → tasación ⭐ + naturaleza → elegís ball → minijuego de anillo → captura/escape); qué hace cada ball especial; el compañero/Sincronía; los alfa; el shiny que aparece y hay que atrapar antes de que huya; el tiro Excelente que mejora IVs.

- [ ] **Step 2: Verificación visual (screenshots)**

`cd web && npm run dev` (http://localhost:4321). Con Playwright (disponible en `web/node_modules`), capturar en tema oscuro y claro: la **carta de encuentro** (tasación + selector de balls), el **overlay del anillo**, el **selector de compañero**, la **tienda** con las balls nuevas (set de sprites coherente, Xeneize azul-oro), y la **marca alfa** en el modal Pokédex. Confirmar coherencia.

- [ ] **Step 3: Verificación funcional**

- `cd web && node --test src/lib/safari-core.test.mjs` → verde.
- `cd web && npm run build` → OK.
- `cd api && npx jest` → sin regresiones (el motor no se toca).
- E2E manual mínimo (dev): buscar → aparece salvaje → elegir ball → tirar (anillo) → captura/zafó/huyó; verificar consumo de ball y que un Excelente mejora IVs en el modal; setear compañero con Sincronía y ver naturaleza fijada; capturar un shiny/alfa.

- [ ] **Step 4: Commit final**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/ayuda.astro docs
git commit -m "docs: ayuda al día con el Safari profundo (encuentro, balls, compañero, alfa)"
```

---

## Notas para el ejecutor

- **`col:balls` vs items:** la Poké Ball básica es el contador `col:balls` (se gana con ejercicios); el resto son items de `col:items`. `inventarioBalls`/`consumirBall` ya manejan ambos.
- **`pesos` de rareza:** `encontrar` recibe los mismos `pesos` que usaba `tirar`. Reusar la fuente actual en `safari.astro` (no inventar otra).
- **Sin tocar el motor de combate** (`combate-core.ts`) ni la API. `node --test` es el único runner nuevo (nativo, sin deps).
- **Sincronía** usa la habilidad `synchronize` (key de PokeAPI; es flavor en combate pero acá tiene efecto de captura).
- **Owner-gated:** precios/obtención de Master y el deploy no aplican a esta fase (todo es front + localStorage/nube).
- **Sin atribución Claude** en los commits.
```
