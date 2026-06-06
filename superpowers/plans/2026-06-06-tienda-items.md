# Tienda de items — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:executing-plans. Steps con checkbox.

**Goal:** Tienda que gasta Pokébolas en items (piedras de evolución, pociones de batalla, mejores Pokéballs) que profundizan evolución/safari/batalla.

**Architecture:** `items.js` = catálogo puro. `coleccion.js` = economía (comprar/usar/dar) sobre `col:items` en localStorage (sync nube). Integraciones: evolución-por-piedra (pokédex), mejor-ball-automática (safari), mochila-pociones (batalla). `/tienda` = UI.

**Tech Stack:** Astro + JS vanilla + localStorage. Verificación: node (lógica) + CDP (UI).

**Spec:** `superpowers/specs/2026-06-06-tienda-items-design.md`

---

## Task 1: `items.js` — catálogo de items + config de balls

**Files:** Create `web/src/lib/items.js`

- [ ] **Step 1:** Crear el catálogo.

```javascript
// items.js — catálogo de la tienda (puro). El inventario vive en coleccion.js (col:items).
export const ITEMS = {
  piedra:      { nombre: 'Piedra Evolutiva', ico: '🪨', precio: 80, cat: 'evo',    desc: 'Evoluciona a los Pokémon que evolucionan por piedra (Eevee, Pikachu, Vulpix…). Se gasta 1.' },
  pocion:      { nombre: 'Poción',           ico: '🧪', precio: 15, cat: 'cura',   cura: 30,        desc: 'Cura 30 HP en batalla.' },
  superpocion: { nombre: 'Súper Poción',     ico: '⚗️', precio: 35, cat: 'cura',   cura: 70,        desc: 'Cura 70 HP en batalla.' },
  pocionmax:   { nombre: 'Poción Máxima',    ico: '💉', precio: 70, cat: 'cura',   cura: 9999,      desc: 'Cura todo el HP en batalla.' },
  superball:   { nombre: 'Super Ball',       ico: '🔵', precio: 25, cat: 'ball', tier: 1, desc: 'Mejora la captura: +shiny, +nivel, +rareza, +caramelos (moderado).' },
  ultraball:   { nombre: 'Ultra Ball',       ico: '🟡', precio: 60, cat: 'ball', tier: 2, desc: 'Mejora fuerte de captura: ++shiny, ++nivel, ++rareza, ++caramelos.' },
};
// boosts de captura por tier de ball (0 = normal). [shinyMult, nivelExtraPct, rarezaMult, caramelos]
export const BALL_BOOST = {
  0: { shiny: 1, nivelPct: 0,    rareza: 1,   caramelos: 3 },
  1: { shiny: 2, nivelPct: 0.20, rareza: 1.4, caramelos: 5 },
  2: { shiny: 4, nivelPct: 0.45, rareza: 2.0, caramelos: 8 },
};
export const itemsPorCat = (cat) => Object.entries(ITEMS).filter(([, it]) => it.cat === cat).map(([id, it]) => ({ id, ...it }));
```

- [ ] **Step 2: Verificar** (node):
```bash
cd /home/felipe/Documents/Repositories/luca-journey/web
node --input-type=module -e "import { ITEMS, BALL_BOOST, itemsPorCat } from './src/lib/items.js'; console.log('items:', Object.keys(ITEMS).length, '| balls cat:', itemsPorCat('ball').map(x=>x.nombre).join(', '), '| boost2:', JSON.stringify(BALL_BOOST[2]));"
```
Expected: items 6, balls "Super Ball, Ultra Ball", boost2 con shiny 4.

- [ ] **Step 3: Commit**
```bash
cd /home/felipe/Documents/Repositories/luca-journey && git add web/src/lib/items.js && git commit -m "items: catalogo de la tienda + config de boosts de balls"
```

---

## Task 2: `coleccion.js` — economía (inventario)

**Files:** Modify `web/src/lib/coleccion.js`

- [ ] **Step 1:** Importar ITEMS y agregar los helpers de inventario (cerca de `darBalls`).

```javascript
import { ITEMS } from './items.js' ; // (poner junto a los otros imports, sin el attribute — es .js)

export const items = () => get('col:items', {});
export function darItem(id, n = 1) { const inv = get('col:items', {}); inv[id] = (inv[id] || 0) + n; set('col:items', inv); }
export const tieneItem = (id) => (get('col:items', {})[id] || 0) > 0;
export function usarItem(id) { const inv = get('col:items', {}); if (!(inv[id] > 0)) return false; inv[id]--; if (inv[id] <= 0) delete inv[id]; set('col:items', inv); return true; }
export function comprarItem(id) {
  const it = ITEMS[id]; if (!it) return false;
  const balls = get('col:balls', 0); if (balls < it.precio) return false;
  set('col:balls', balls - it.precio); darItem(id, 1); return true;
}
```

- [ ] **Step 2: Verificar** (node):
```bash
node --input-type=module -e "
globalThis.localStorage={_:{'col:balls':'100'},getItem(k){return this._[k]??null},setItem(k,v){this._[k]=v},removeItem(k){delete this._[k]}};
const m=await import('./src/lib/coleccion.js');
console.log('comprar superpocion:', m.comprarItem('superpocion'), '| balls:', JSON.parse(localStorage.getItem('col:balls')), '| tiene:', m.tieneItem('superpocion'));
console.log('comprar caro sin saldo:', (localStorage.setItem('col:balls','5'), m.comprarItem('ultraball')));
m.darItem('piedra',2); console.log('usar piedra:', m.usarItem('piedra'), '| quedan:', m.items().piedra);
"
```
Expected: comprar true, balls 65, tiene true; comprar caro false; usar piedra true, quedan 1.

- [ ] **Step 3: Commit** `coleccion: economia de items (items/comprar/usar/dar/tiene)`

---

## Task 3: `coleccion.js` — evolución por piedra

**Files:** Modify `web/src/lib/coleccion.js`

- [ ] **Step 1:** En `opcionesEvo`, marcar que las opciones `nivel===0` requieren piedra; agregar el flag `piedra` a la opción.

```javascript
export function opcionesEvo(iid) {
  const m = buscarInst(pc(), iid); if (!m) return [];
  const car = caramelos()[familiaDe(m.id)] || 0;
  return ((evoData[m.id] && evoData[m.id].evos) || []).map((ev) => {
    const costo = costoEvo(ev.nivel);
    const piedra = ev.nivel === 0;                       // evos por piedra
    const ok = (ev.nivel > 0 ? m.nivel >= ev.nivel : tieneItem('piedra')) && car >= costo;
    return { a: ev.a, nivel: ev.nivel, costo, ok, piedra };
  });
}
```

- [ ] **Step 2:** En `evolucionarInst`, consumir la piedra si la opción es por piedra.

```javascript
export function evolucionarInst(iid, targetId) {
  const arr = pc(); const m = buscarInst(arr, iid); if (!m) return false;
  const op = opcionesEvo(iid).find((o) => o.a === Number(targetId) && o.ok); if (!op) return false;
  if (op.piedra && !usarItem('piedra')) return false;    // gasta la piedra
  const c = get('col:caramelos', {}); c[familiaDe(m.id)] -= op.costo; set('col:caramelos', c);
  addVisto(m.id); m.id = op.a; m.movs = []; addVisto(m.id); setPC(arr);
  return op.a;
}
```

- [ ] **Step 3: Verificar** (node): un evo-por-piedra (Eevee 133) sin piedra → ok=false; con piedra → evoluciona y la consume.
```bash
node --input-type=module -e "
globalThis.localStorage={_:{},getItem(k){return this._[k]??null},setItem(k,v){this._[k]=v},removeItem(k){delete this._[k]}};
const m=await import('./src/lib/coleccion.js');
const e=m.atrapar(133); localStorage.setItem('col:caramelos', JSON.stringify({133:200}));
console.log('eevee sin piedra ok?:', m.opcionesEvo(e.iid)[0].ok, '(esperado false)');
m.darItem('piedra',1);
console.log('con piedra ok?:', m.opcionesEvo(e.iid)[0].ok, '(esperado true)');
const to=m.opcionesEvo(e.iid).find(o=>o.ok).a; m.evolucionarInst(e.iid,to);
console.log('evoluciono a:', m.pc()[0].id, '| piedras restantes:', m.items().piedra||0);
"
```
Expected: sin piedra false, con piedra true, evoluciona, piedras 0.

- [ ] **Step 4: Commit** `coleccion: evolucion por piedra requiere Piedra Evolutiva (de la tienda)`

---

## Task 4: `coleccion.js` — `tirar()` usa la mejor ball

**Files:** Modify `web/src/lib/coleccion.js`

- [ ] **Step 1:** Agregar `mejorBallTier()` (ultra > super > normal según stock) e integrar en `tirar()`: consumir la ball y aplicar los boosts (shiny, nivel, rareza, caramelos).

```javascript
import { BALL_BOOST } from './items.js';
export function mejorBallTier() { const inv = items(); if (inv.ultraball) return 2; if (inv.superball) return 1; return 0; }
```
En `tirar()`, reemplazar el cómputo de shiny/captura por la versión con boost:
```javascript
  // elegir + consumir la mejor ball disponible
  const tier = mejorBallTier();
  if (tier === 2) usarItem('ultraball'); else if (tier === 1) usarItem('superball');
  const boost = BALL_BOOST[tier];
  // rareza: las mejores balls sesgan el peso hacia lo raro (peso menor = más raro → se infla)
  const pesosAjust = {}; for (const k in pesos) pesosAjust[k] = pesos[k] / boost.rareza;
  const elegido = elegirPonderado(pool, boost.rareza === 1 ? pesos : pesosAjust);
  // ... prob/cadaCuantos con 'pesos' original ...
  balls--;
  const shiny = Math.random() < PROB_SHINY * boost.shiny;
  const nivelBase = nivelWild(elegido.id);
  const nivel = Math.min(50, Math.round(nivelBase * (1 + boost.nivelPct)));
  const inst = atrapar(elegido.id, { shiny, nivel });
  // caramelos extra de la ball: ya se dieron 3 en atrapar → sumar la diferencia
  if (boost.caramelos > 3) addCaramelosPublic(elegido.id, boost.caramelos - 3);
```
Necesitás exponer `addCaramelos` para el extra: agregá `export function darCaramelosFamilia(id,n){ addCaramelos(id,n); }` y usalo (o reutilizá `darCaramelos`). Devolvé también `ball: tier` en el return para que el safari muestre qué ball usó.

- [ ] **Step 2: Verificar** (node): con ultraball en stock, tirar la consume + el nivel sube + shiny prob 4%.
```bash
node --input-type=module -e "
globalThis.localStorage={_:{'col:balls':'5','col:items':JSON.stringify({ultraball:2}),'col:pc':'[]'},getItem(k){return this._[k]??null},setItem(k,v){this._[k]=v},removeItem(k){delete this._[k]}};
const m=await import('./src/lib/coleccion.js');
const r=m.tirar([{id:6,region:'kanto'}],[{slug:'x',region:'kanto',ejercicios:[{id:1}]}],{6:1});
console.log('ball usada (2=ultra):', r.ball, '| nivel (boosteado):', r.nivel, '| ultraballs restantes:', m.items().ultraball);
"
```
Expected: ball 2, nivel ≥ Charizard min (28) ×1.45, ultraballs 1.

- [ ] **Step 3: Commit** `coleccion: tirar() usa la mejor ball del inventario (boosts shiny/nivel/rareza/caramelos)`

---

## Task 5: `/tienda` — página de la tienda (UI con /frontend-design)

**Files:** Create `web/src/pages/tienda.astro` · Modify `web/src/styles/global.css`

- [ ] **Step 1:** Página con: saldo de 🔴 Pokébolas arriba, secciones por categoría (Evolución / Curación / Pokéballs), cada item: ico, nombre, desc, precio, botón **Comprar** (deshabilitado si no alcanza), y badge "tenés N". Cohesiva con el Device OS (header tipo escáner, tema-aware). Importá `ITEMS, itemsPorCat` de `items.js` y `items, comprarItem` de `coleccion.js`. Tras comprar → re-render saldo+inventario + sonido. Diseño visual: aplicar `/frontend-design` (caja/cards estilo dispositivo, no genérico).

- [ ] **Step 2: Verificar visual** (CDP, oscuro+claro): la tienda lista los 6 items, comprar baja el saldo y sube "tenés N".

- [ ] **Step 3: Commit** `tienda: pagina /tienda (comprar con Pokebolas, inventario)`

---

## Task 6: Safari — mejor ball automática + mostrar cuál

**Files:** Modify `web/src/pages/safari.astro`

- [ ] **Step 1:** En la captura, mostrar qué ball se usó (`r.ball`: 🔴/🔵/🟡) y, si quedan pocas, un aviso. La lógica ya está en `tirar()` (Task 4); acá es display. Agregar en la barra el stock de Super/Ultra (de `items()`).
- [ ] **Step 2: Verificar visual** (CDP): con Ultra Balls, la captura muestra 🟡 + el nivel boosteado.
- [ ] **Step 3: Commit** `safari: muestra la ball usada + stock de super/ultra`

---

## Task 7: Pokédex modal — piedra para evo-por-piedra

**Files:** Modify `web/src/pages/pokedex.astro`

- [ ] **Step 1:** En `evoBloque`, si la opción es `piedra` y no hay piedra, mostrar "🪨 Necesitás una Piedra Evolutiva — Tienda" (link a `/tienda`) en vez del botón habilitado; si hay piedra, el botón dice "🧬 Evolucionar (🪨 + Ncaramelos)". Usar `opcionesEvo` (ya devuelve `piedra`) + `tieneItem('piedra')` (importar de coleccion).
- [ ] **Step 2: Verificar visual** (CDP): Eevee sin piedra muestra el aviso+link; con piedra, el botón evoluciona.
- [ ] **Step 3: Commit** `pokedex: evo-por-piedra pide Piedra Evolutiva (aviso + link a la tienda)`

---

## Task 8: Batalla — Mochila (pociones)

**Files:** Modify `web/src/pages/batalla.astro` · `web/src/styles/global.css`

- [ ] **Step 1:** Botón **🎒 Mochila** en los controles. Abre un mini-panel con tus pociones (de `items()` cat 'cura', con stock). Tocar una: cura el activo (`miAct().hp = min(hpMax, hp + cura)`), consume el item (`usarItem`), **gasta el turno** (el rival ataca: `turnoRival` + el flujo de turno). Límite 2 usos de item por combate (contador en G). Cancela/rearma el timer como `turno`.
- [ ] **Step 2: Verificar visual** (CDP): con pociones, la mochila cura el activo y el rival ataca después.
- [ ] **Step 3: Commit** `batalla: mochila — usar pociones (cura el activo, cuesta turno, limite 2)`

---

## Task 9: Acceso + build + deploy

**Files:** Modify `web/src/pages/safari.astro` / `pokedex.astro` (acceso) · `web/src/pages/ayuda.astro`

- [ ] **Step 1:** Acceso a `/tienda`: botón "🛒 Tienda" en el hero del safari y de la pokédex (con `u('/tienda')`). Actualizar `ayuda.astro` con la tienda.
- [ ] **Step 2:** `cd web && npm run build` (sin errores).
- [ ] **Step 3:** Commit `docs/` + push (`git add docs && git commit -m "build: tienda de items" && git push origin main`).

---

## Self-review (cobertura del spec)

- Moneda Pokébolas: Task 2 (comprarItem usa col:balls). ✔
- Items piedras/pociones/balls: Task 1 (catálogo). ✔
- Evo-por-piedra requiere piedra: Task 3 + Task 7. ✔
- Balls automáticas + boosts (shiny/nivel/rareza/caramelos): Task 4 + Task 6. ✔
- Pociones en batalla (cuesta turno, límite): Task 8. ✔
- Inventario nube (col:items): Task 2 (col:items va en el blob de progreso por write-through). ✔
- /tienda + acceso + ayuda: Task 5 + Task 9. ✔
- Out of scope (caramelo raro, piedras por tipo, stock limitado): sin tasks. ✔
