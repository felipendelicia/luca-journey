# Safari profundo — Fase 3 · Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cerrar el loop de EVs: otorgarlos al ganar en PvP (server) y poder bajar/resetear EVs con bayas (client).

**Architecture:** Math pura en `web/src/lib/combate-core.ts` (`restarEV`, `evPorDerrotados`), fuente única que `api/scripts/sync-batalla-data.mjs` copia a `api/src/batalla/combate-core.ts` (tests jest). Las bayas/Borrón son client (`coleccion.js`+`items.js`+`pokedex.astro`+`tienda.astro`). Los EVs en PvP van en `api/src/batalla/insignias.ts` (server-autoritativo, persiste en el blob `progreso`).

**Tech Stack:** TS (combate-core/insignias), JS módulos (coleccion/items), Astro (pokedex/tienda/batalla), Jest (tests en `api/`), SVG sprites.

**Convención:** specs/plans en `superpowers/` (raíz). Sin atribución Claude. UI/sprites → `/frontend-design`. Spec: `superpowers/specs/2026-06-07-safari-profundo-fase3-design.md`.

**Flujo de tests del core:** el spec vive en `api/src/batalla/combate-core.spec.ts` y corre contra la **copia sincronizada**. Cada tarea que toca el core: editar `web/src/lib/combate-core.ts` → `cd api && node scripts/sync-batalla-data.mjs` → editar/correr el spec en `api/`. NUNCA editar `api/src/batalla/combate-core.ts` a mano (es generado).

**Contexto (ya en main):**
- `combate-core.ts` tiene `sumarEV(evs, yields)` (cap 252/510). `web/src/data/yields.json` ya está
  sincronizado a `api/src/batalla/data/yields.json` (en el `FILES` del sync).
- `coleccion.js`: `darEV`, `evsDe(inst)`, `yieldDe(id)`, `usarVitamina(iid, statIdx)`, `pc()`, `setPC`,
  `tieneItem`, `usarItem`, `items()`.
- `items.js`: vitaminas en cat `'ev'` (`proteina/hierro/calcio/zinc/carburo/masps`, campo `ev`=statIdx,
  `evMax:100`).
- `pokedex.astro` (`estatsBloque`): botón de vitamina por stat usando `VIT_POR_STAT[i]`
  (`{}; for (const it of itemsPorCat('ev')) VIT_POR_STAT[it.ev] = it.id`), render `<button class="id-vit"
  data-vit-stat="i" ...>` y handler `[data-vit-stat]` (línea ~410) que llama `usarVitamina`+`usarItem`+re-render.
- `insignias.ts`: `aplicarUno(progreso, yo, rival, gano, …)` arma `Premios`, muta el blob `estado`
  (helpers `pObj`/`setObj`/`pNum`), y al final `await progreso.subir(yo.uid, estado)`. `Premios` interface
  (gano/caramelos/balls/insignias/rating/delta/estado).
- `sprites.js`: `itemSvg(id, size, color?)`; las vitaminas usan `vitaminaColor(statIdx)` (la tienda
  tintó `sprite==='vitamina'` con ese color).

**Orden:** Parte B (bayas, client) primero; Parte A (EVs en PvP, server) después (owner-gated por el deploy).

---

### Task 1: `combate-core.ts` — `restarEV` + `evPorDerrotados` (puro + tests)

**Files:**
- Modify: `web/src/lib/combate-core.ts`
- Test: `api/src/batalla/combate-core.spec.ts`

- [ ] **Step 1: Escribir tests (FALLAN primero)** — APPEND a `api/src/batalla/combate-core.spec.ts`:
```ts
import { restarEV, evPorDerrotados } from './combate-core';
describe('EVs Fase 3', () => {
  test('restarEV baja n EV de un stat con floor 0', () => {
    expect(restarEV([20, 0, 0, 0, 0, 0], 0, 10)).toEqual([10, 0, 0, 0, 0, 0]);
    expect(restarEV([5, 0, 0, 0, 0, 0], 0, 10)).toEqual([0, 0, 0, 0, 0, 0]);
    expect(restarEV([0, 0, 0, 0, 0, 0], 3, 10)).toEqual([0, 0, 0, 0, 0, 0]);
  });
  test('evPorDerrotados suma yields de los debilitados (hp<=0)', () => {
    const yields = { '1': [0, 0, 0, 1, 0, 0], '4': [0, 1, 0, 0, 0, 0], '7': [0, 0, 1, 0, 0, 0] };
    const equipo = [{ id: 1, hp: 0 }, { id: 4, hp: 0 }, { id: 7, hp: 12 }];   // 1 y 4 caídos, 7 vivo
    expect(evPorDerrotados(equipo, yields)).toEqual([0, 1, 0, 1, 0, 0]);
    expect(evPorDerrotados([{ id: 1, hp: 30 }], yields)).toEqual([0, 0, 0, 0, 0, 0]);
  });
});
```

- [ ] **Step 2: Correr, debe FALLAR**: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t "EVs Fase 3"` → FAIL (símbolos no existen).

- [ ] **Step 3: Implementar en `web/src/lib/combate-core.ts`** — agregar junto a `sumarEV`:
```ts
// baja `n` EV de un stat (floor 0). Devuelve copia. (Bayas Pomeg/Kelpsy/… + Borrón.)
export function restarEV(evs: number[], idx: number, n: number): number[] {
  const out = (evs && evs.length === 6) ? [...evs] : [0, 0, 0, 0, 0, 0];
  out[idx] = Math.max(0, out[idx] - n);
  return out;
}
// suma de yields de los Pokémon de un equipo que quedaron debilitados (hp<=0). Para EVs en PvP.
export function evPorDerrotados(equipo: { id: number; hp: number }[], yields: Record<string, number[]>): number[] {
  const out = [0, 0, 0, 0, 0, 0];
  for (const c of equipo) if (c.hp <= 0) { const y = yields[String(c.id)] || []; for (let i = 0; i < 6; i++) out[i] += (y[i] || 0); }
  return out;
}
```

- [ ] **Step 4: Correr, debe PASAR**: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core` → toda la suite verde.

- [ ] **Step 5: Commit** (sin atribución Claude):
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: restarEV (bayas) + evPorDerrotados (EVs en PvP) — puro + tests"
```

---

### Task 2: `coleccion.js` — `bajarEV` + `resetEV`

**Files:**
- Modify: `web/src/lib/coleccion.js`

- [ ] **Step 1: Import `restarEV`.** En el import de `./safari-core.js`/`./combate-core.ts` — `restarEV` está
  en `combate-core.ts`. Buscar el import existente de `./combate-core.ts` (donde están `sumarEV`,
  `identidad as identidadCore`, etc.) y agregar `restarEV`. (Si `sumarEV` se importa desde ahí, sumá
  `restarEV` a esa misma línea.)

- [ ] **Step 2: Agregar `bajarEV` + `resetEV`** cerca de `usarVitamina`/`darEV`:
```js
// baja 10 EV de un stat (baya). Devuelve true si bajó algo.
export function bajarEV(iid, statIdx) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
  const ev = evsDe(m); if (ev[statIdx] <= 0) return false;
  m.evs = restarEV(ev, statIdx, 10); setPC(arr); return true;
}
// pone TODOS los EVs en 0 (Borrón). Devuelve true si había algo que resetear.
export function resetEV(iid) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
  if (evsDe(m).every((v) => v === 0)) return false;
  m.evs = [0, 0, 0, 0, 0, 0]; setPC(arr); return true;
}
```

- [ ] **Step 3: Smoke-test**:
```
cd web && node --input-type=module -e "import('./src/lib/coleccion.js').then(m=>console.log('ok', typeof m.bajarEV, typeof m.resetEV)).catch(e=>console.log('ERR', e.message))"
```
Ideal: `ok function function`. (Un `ERR` por el import-attribute preexistente de `habilidades.json`/`yields.json` bajo node crudo es aceptable; si es por `restarEV`/sintaxis, arreglar.)

- [ ] **Step 4: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/coleccion.js
git commit -m "coleccion: bajarEV (−10) + resetEV (Borrón)"
```

---

### Task 3: `items.js` (6 bayas + Borrón) + `sprites.js` (`baya`/`borrador`)

**REQUIRED SUB-SKILL:** `/frontend-design` para los sprites (SVG, coherentes con la familia de items; regla CLAUDE.md: items Pokémon = sprite SVG, no emoji).

**Files:**
- Modify: `web/src/lib/items.js`
- Modify: `web/src/lib/sprites.js`

- [ ] **Step 1: Agregar items** en `items.js`, en la sección cat `'ev'` (después de `masps`):
```js
  bayaps:   { nombre: 'Baya Zreza',  sprite: 'baya', cat: 'ev', baja: 0, precio: 20, desc: '−10 EV de PS.' },
  bayaatk:  { nombre: 'Baya Pomeg',  sprite: 'baya', cat: 'ev', baja: 1, precio: 20, desc: '−10 EV de Ataque.' },
  bayadef:  { nombre: 'Baya Kelpsy', sprite: 'baya', cat: 'ev', baja: 2, precio: 20, desc: '−10 EV de Defensa.' },
  bayaspa:  { nombre: 'Baya Hondew', sprite: 'baya', cat: 'ev', baja: 3, precio: 20, desc: '−10 EV de Ataque Especial.' },
  bayaspd:  { nombre: 'Baya Grepa',  sprite: 'baya', cat: 'ev', baja: 4, precio: 20, desc: '−10 EV de Defensa Especial.' },
  bayavel:  { nombre: 'Baya Tamato', sprite: 'baya', cat: 'ev', baja: 5, precio: 20, desc: '−10 EV de Velocidad.' },
  borrador: { nombre: 'Borrón EV',   sprite: 'borrador', cat: 'ev', reset: true, precio: 60, desc: 'Pone TODOS los EVs de un Pokémon en 0.' },
```

- [ ] **Step 2: Sprites** en `sprites.js`. Agregar (mirando cómo está `vitamina`/`vitaminaColor`):
  - `baya`: una **baya redonda** (con hojita y brillo), **color-coded por stat** — soportar `itemSvg('baya',
    size, color)` igual que `vitamina`. Exportá `bayaColor(statIdx)` (podés reusar el mapeo de
    `vitaminaColor` o los colores de stat) para tintar.
  - `borrador`: un sprite de **goma de borrar** (o disquete/✗ estilizado), neutro, coherente con la familia.
  - Mapear en `itemSvg`: `'baya'`→bayaSvg (con color), `'borrador'`→borradorSvg. Mantener `itemSvg`
    backward-compatible.
  Verificá el set junto (Playwright screenshot, como en fases anteriores): las 6 bayas color-coded + el Borrón.

- [ ] **Step 3: Verificar**: `cd web && node -e "import('./src/lib/sprites.js').then(m=>console.log(m.itemSvg('baya',20,'#f5ac78').length>50, m.itemSvg('borrador',20).length>50))"` → `true true`.

- [ ] **Step 4: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/items.js web/src/lib/sprites.js
git commit -m "items+sprites: bayas (−10 EV por stat) + Borrón EV"
```

---

### Task 4: `pokedex.astro` — botones −10 (baya) + Reset EVs en el modal

**REQUIRED SUB-SKILL:** `/frontend-design` para el estilo de los botones (coherente con `.id-vit`).

**Files:**
- Modify: `web/src/pages/pokedex.astro`
- Modify: `web/src/styles/global.css`

- [ ] **Step 1: Imports.** Agregar `bajarEV, resetEV` al import de `../lib/coleccion.js` (donde están
  `usarVitamina, usarItem, tieneItem`).

- [ ] **Step 2: Mapa de bayas por stat.** Cerca de `const VIT_POR_STAT = {} …` (línea ~354), agregar:
```js
    const BAJA_POR_STAT = {}; for (const it of itemsPorCat('ev')) if (it.baja != null) BAJA_POR_STAT[it.baja] = it.id;
    const BORRADOR = (itemsPorCat('ev').find((it) => it.reset) || {}).id;   // 'borrador'
```

- [ ] **Step 3: Botón −10 por stat.** En `estatsBloque`, donde se arma el botón de vitamina (línea ~309-312),
  agregar al lado un botón de baja si tenés la baya y hay EV que bajar:
```js
        const baja = BAJA_POR_STAT[i];
        const btnBaja = (baja && tieneItem(baja) && ev > 0)
          ? '<button class="id-vit id-baja" data-baja-stat="' + i + '" title="' + ITEMS[baja].nombre + ': −10 EV de ' + lbl + '">' + itemSvg('baya', 15, ID_STAT[i]) + '<span>−10</span></button>'
          : '';
```
Y sumá `btnBaja` al HTML de la fila justo después de `btn` (el de vitamina).

- [ ] **Step 4: Botón global Reset EVs.** En `estatsBloque`, en el encabezado del panel (donde se muestra
  `EV ' + evTotal + '/510'`), agregar un botón si tenés Borrón y hay EVs:
```js
        (BORRADOR && tieneItem(BORRADOR) && evTotal > 0 ? '<button class="id-reset-ev" data-reset-ev title="Borrón EV: pone todos los EVs en 0">♻️ Reset EVs</button>' : '')
```
(Insertarlo en el header del panel junto al texto de EV total; ajustá el armado del string.)

- [ ] **Step 5: Handlers.** Junto al handler `[data-vit-stat]` (línea ~410), agregar:
```js
      $('poke-modal-cuerpo').querySelectorAll('[data-baja-stat]').forEach((b) => b.addEventListener('click', () => {
        const stat = Number(b.dataset.bajaStat); const baya = BAJA_POR_STAT[stat];
        if (!baya || !tieneItem(baya)) return;
        if (bajarEV(iid, stat)) { usarItem(baya); sonarExito(); abrirModal(iid, true); }
      }));
      const bReset = $('poke-modal-cuerpo').querySelector('[data-reset-ev]');
      if (bReset) bReset.addEventListener('click', () => {
        if (BORRADOR && tieneItem(BORRADOR) && resetEV(iid)) { usarItem(BORRADOR); sonarExito(); abrirModal(iid, true); }
      });
```
(Usar el `iid` del scope del modal, como el handler de vitamina.)

- [ ] **Step 6: Estilos** en `global.css`: `.id-baja` (como `.id-vit` pero acento "negativo", ej. rojo
  suave) y `.id-reset-ev` (botón sutil). Tema-aware.

- [ ] **Step 7: Build + screenshot** (Playwright; seedeá una instancia con `evs` altos + `col:items` con
  una baya y `borrador`): ver los botones −10 y Reset. `cd web && npm run build` → OK.

- [ ] **Step 8: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/pokedex.astro web/src/styles/global.css docs
git commit -m "pokedex: botones −10 (baya) por stat + Reset EVs (Borrón) en el modal"
```

---

### Task 5: `tienda.astro` — bayas + Borrón con su sprite

**Files:**
- Modify: `web/src/pages/tienda.astro`

- [ ] **Step 1: Tinte de las bayas.** La cat `'ev'` ya se renderiza (vitaminas). Las bayas comparten
  `sprite:'baya'` → si la tienda tintó las vitaminas con `vitaminaColor(it.ev)` para `sprite==='vitamina'`,
  hacer lo análogo para `sprite==='baya'` con `bayaColor(it.baja)` (importar `bayaColor` de `sprites.js`).
  El `borrador` (`sprite:'borrador'`) fluye con `itemSvg(it.sprite,…)` sin color. Leé `tienda.astro` para ver
  cómo arma el icono de cada item en cat `'ev'` y replicá el patrón de las vitaminas.

- [ ] **Step 2: Verificar**: `cd web && npm run build` y `grep -c 'Baya Pomeg\|Borrón EV' docs/tienda/index.html`
  → ≥ 1. Screenshot de la cat EV (vitaminas + bayas color-coded + Borrón).

- [ ] **Step 3: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/tienda.astro docs
git commit -m "tienda: bayas (−10 EV) + Borrón con sprite color-coded"
```

---

### Task 6: `insignias.ts` — EVs en PvP (server) + mostrar +EVs en el resultado

**Files:**
- Modify: `api/src/batalla/insignias.ts`
- Modify: `web/src/pages/batalla.astro` (mostrar `premios.ev`)
- Test: `api/src/batalla/combate-core.spec.ts` (ya cubierto en Task 1 por `evPorDerrotados`)

- [ ] **Step 1: Imports en `insignias.ts`.** Agregar:
```ts
import yields from './data/yields.json';
import { evPorDerrotados, sumarEV } from './combate-core';
```

- [ ] **Step 2: `Premios` gana `ev`.** En la interface `Premios`, agregar `ev?: number[];`.

- [ ] **Step 3: Otorgar EVs en `aplicarUno`.** Justo ANTES de `await progreso.subir(yo.uid, estado);` (al
  final de la función), agregar:
```ts
  // EVs en PvP: yields de los rivales debilitados → al equipo que trajo (los 3). Ambos jugadores.
  const yv = evPorDerrotados(rival.equipo, yields as any);
  if (yv.some((n) => n > 0)) {
    const pcArr = pObj(estado, 'col:pc', []);
    for (const c of yo.equipo) { const m = pcArr.find((x: any) => x.iid === c.iid); if (m) m.evs = sumarEV(m.evs || [0, 0, 0, 0, 0, 0], yv); }
    setObj(estado, 'col:pc', pcArr);
    premios.ev = yv;
  }
```
(`rival.equipo`/`yo.equipo` son los `Combatiente[]` del estado, con `hp` e `iid`.)

- [ ] **Step 4: Mostrar +EVs en el cliente** (`web/src/pages/batalla.astro`, modo En vivo). En el handler
  del evento `'fin'` que muestra los premios (`premios.caramelos`/`premios.balls`/`premios.rating`),
  agregar: si `premios.ev` trae algún valor > 0, una línea tipo `+EVs entrenados` (un resumen corto;
  podés listar los stats con `+N`). Buscá dónde se renderiza el resultado del PvP y sumalo ahí.

- [ ] **Step 5: Verificar**: `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest`
  → nest build OK, jest verde (incluye `evPorDerrotados`/`restarEV`). `cd web && npm run build` → OK.

- [ ] **Step 6: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api/src/batalla/insignias.ts web/src/pages/batalla.astro web/src/lib/combate-core.ts api/src/batalla/combate-core.ts docs
git commit -m "pvp: otorgar EVs al fin del combate (rivales derrotados → equipo, ambos) + mostrarlos"
```

- [ ] **Step 7 (owner-gated, NO automatizar): deploy a la Pi.** Anotar que el motor PvP con EVs requiere
  redeploy de la imagen arm64 a la Raspberry: `node api/scripts/sync-batalla-data.mjs` → cross-build arm64
  → `docker save | ssh load` → `docker compose up -d` (ver CLAUDE.md / [[deploy-pi-config]]). Lo corre el
  dueño; el e2e real de 2 sesiones también.

---

### Task 7: `ayuda.astro` + verificación final

**Files:**
- Modify: `web/src/pages/ayuda.astro`

- [ ] **Step 1: Documentar** en `ayuda.astro` (estilo existente, `u('/...')`): que ahora **ganás EVs también
  en PvP** (al ganar/derrotar rivales online) y que con las **bayas** (tienda) podés **bajar 10 EV** de un
  stat o **resetear** todos con el **Borrón EV**, desde el modal de la Pokédex (junto a las vitaminas).

- [ ] **Step 2: Verificación final**:
- `cd api && node scripts/sync-batalla-data.mjs && npx jest` → verde (pegá el resumen).
- `cd web && npm run build` → OK.
- E2E manual (dev): comprar una baya + Borrón; en el modal Pokédex de un Pokémon con EVs, ver/usar los
  botones −10 y Reset; verificar que la barra de EV baja.

- [ ] **Step 3: Commit final**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/ayuda.astro docs
git commit -m "docs: ayuda al día con EVs en PvP + bayas/Borrón de EV"
```

---

## Notas para el ejecutor

- **Sync obligatorio:** cambios en `web/src/lib/combate-core.ts` requieren `cd api && node scripts/sync-batalla-data.mjs` antes de jest/build de la API. `api/src/batalla/combate-core.ts` es GENERADO.
- **EVs en PvP** se otorgan server-side y se persisten en el blob `progreso`; el cliente los recibe por el
  evento `progreso` (ya implementado) y la Pokédex los muestra. **El deploy a la Pi es owner-gated** (Task 6
  Step 7) — el código queda listo; el dueño redeploya + corre el e2e de 2 sesiones.
- **Bayas vs vitaminas:** misma cat `'ev'`; las vitaminas tienen `ev` (statIdx, +10), las bayas `baja`
  (statIdx, −10), el Borrón `reset:true`. Los mapas `VIT_POR_STAT`/`BAJA_POR_STAT` los separan por esos campos.
- **Sin atribución Claude** en los commits.
```
