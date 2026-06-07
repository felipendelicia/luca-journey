# Safari profundo — Fase 2: racha shiny, biomas/hora, Dusk Ball, alfa con tamaños

**Fecha:** 2026-06-07
**Estado:** diseño aprobado, pendiente plan de implementación.
**Tema:** segunda capa del Safari (sobre [[safari-profundo]] Fase 1). Da un loop de caza vivo:
racha de capturas (cazar shiny), biomas y hora del día automáticos, Dusk Ball y ejemplares alfa
con tamaños. Sinergia con [[identidad-pokemon]] (IVs).

## Decisiones tomadas (brainstorming 2026-06-07)

1. **Encadenado = racha SIMPLE de capturas** (no rastreo de especie): cada captura seguida sube
   `col:racha`. Cuanto más larga, más shiny + mejores IVs. Se reinicia si un salvaje **huye** (o tocás
   Huir). **Zafó** (se soltó pero sigue) NO reinicia.
2. **Biomas + hora AUTOMÁTICOS** (sin que el jugador elija): la **hora** sale del reloj real; el **bioma**
   rota en tiempo real (ciclo Hierba→Agua→Cueva). Un safari "vivo": pasás por biomas/horas distintas.
3. **Dusk Ball:** ×3.5 de captura si es **noche** o **cueva**; ×1 de día en superficie.
4. **Alfa más rico:** cada captura recibe un **tamaño**; el alfa sale grande (+sprite) con título.

## Estado actual (contexto, Fase 1)

`coleccion.js`: `encontrar(pokemon, temas, pesos)` (rolea especie del pool de regiones desbloqueadas,
identidad, shiny `PROB_SHINY=0.01`, alfa `PROB_ALFA=0.04` con 3 IVs perfectos) → `capturar(enc, ballKey,
calidad, {tiroN})`. Lógica pura en `safari-core.js` (`probCaptura`, `catchBall`, `fleeProb`, `pisoIV`,
`sincronizaNat`). `atrapar(id, {shiny,nivel,alfa,ivs,nat,hab,gen})` persiste la instancia. Balls en
`items.js` (cat `'ball'`, campo `catch`/`cond`); sprites `ballSvg`. `safari.astro` = UI de 2 pasos +
minijuego de anillo + secuencia de captura + tarjeta de resumen.

## 1. Racha de capturas (encadenado simple)

- **Estado:** `col:racha` (entero, sync nube como cualquier `col:`). Helpers en `coleccion.js`:
  `racha()`, `subirRacha()` (+1, persiste), `romperRacha()` (→0).
- **Shiny escalado** (puro, `safari-core.js`):
  `shinyChance(racha) = Math.min(0.08, 0.01 * (1 + racha * 0.12))`
  → racha 0 = 1%, 10 ≈ 2.2%, 25 = 4%, ≥58 = cap 8%. `encontrar` usa `shinyChance(racha())` en vez de
  `PROB_SHINY` fijo.
- **Piso de IV por racha** (puro): `pisoRacha(racha) = racha>=50?3 : racha>=30?2 : racha>=15?1 : 0`.
  En `encontrar`, los IVs perfectos garantizados = `max(alfa?3:0, pisoRacha(racha()))` (se combinan,
  no se suman; el Excelente del tiro sigue sumando aparte en `capturar`).
- **Romper/subir:** en `capturar`, éxito → `subirRacha()`; `huyo` → `romperRacha()`. En `safari.astro`,
  "Huir" → `romperRacha()`. (Zafó no toca la racha.)
- **UI:** badge **"🔥 Racha ×N"** en el safari (junto a Pokébolas). Al romperse: mensaje
  "💔 Se cortó la racha (iba en ×N)". El resumen de captura muestra la racha alcanzada.

## 2. Biomas + hora del día (automáticos)

- **Hora real** (puro): `esNoche(now = new Date()) = (h < 6 || h >= 19)` con `h = now.getHours()`.
  Badge **☀️ Día** (6–19h) / **🌙 Noche** (resto).
- **Bioma rotativo** (puro, determinista por el reloj):
  `biomaActual(now = Date.now()) = ['hierba','agua','cueva'][Math.floor(now / 600000) % 3]`
  (cambia cada **10 min**; igual para todas las sesiones). Badge **🌿 Hierba / 💧 Agua / 🪨 Cueva**.
- **Pool por bioma:** `biomas.json` `{ "<id>": "hierba"|"agua"|"cueva" }` (de PokeAPI `pokemon-species.
  habitat`): `waters-edge`/`sea` → agua; `cave` → cueva; el resto (`grassland`/`forest`/`mountain`/
  `rough-terrain`/`urban`/`rare`/null) → hierba. Generado por `gen-biomas.mjs`.
- **Filtro de encuentro:** `encontrar` filtra el pool de regiones desbloqueadas al bioma actual. **Si el
  bioma no tiene especies en las regiones desbloqueadas, cae al pool completo** (siempre podés encontrar
  algo). El `encuentro` devuelve `bioma` y `noche` (para Dusk Ball + display).
- **Sin selector:** el jugador no elige; los badges muestran "dónde/cuándo" está. Da razón para volver
  a distintas horas/biomas.

## 3. Dusk Ball

- **Item** (`items.js`, cat `'ball'`): `dusk: { nombre:'Dusk Ball', sprite:'balldusk', cond:'dusk',
  precio:35, desc:'×3.5 de captura de noche o en cueva.' }`.
- **Efecto** (`safari-core.catchBall`): `case 'dusk': return (ctx.noche || ctx.bioma === 'cueva') ? 3.5 : 1;`
  → `capturar` pasa `noche`/`bioma` del encuentro al `ctx`.
- **Sprite:** `ballSvg` variante (verde oscuro/negro, círculo rojo de noche).

## 4. Alfa más rico (tamaños)

- **`tam`** por instancia: categoría de tamaño. Roll (puro `rolarTam(rng)`): mayormente **Normal**;
  colas raras **XXS** (~3%) y **XXL** (~3%). El **alfa** ignora el roll y sale **XL** (grande).
- **Persistencia:** `atrapar(..., { tam })` guarda `tam` en la instancia (opcional; ausente = 'M').
- **Display:**
  - Safari/captura: si `tam` ∈ {XXS, XXL} o alfa, sprite del salvaje escalado (XXS ×0.82, XL/XXL ×1.18)
    + título ("👑 Coloso" XXL/alfa-XL, "🔬 Mini" XXS) en la tarjeta de resumen.
  - Modal Pokédex: chip de tamaño junto a género/shiny/alfa.
- **No afecta stats** (cosmético, como en la saga).

## Mecánicas puras (→ `safari-core.js`, testeable `node --test`)

```js
export const shinyChance = (racha) => Math.min(0.08, 0.01 * (1 + (racha || 0) * 0.12));
export const pisoRacha = (racha) => racha >= 50 ? 3 : racha >= 30 ? 2 : racha >= 15 ? 1 : 0;
export const esNoche = (now = new Date()) => { const h = now.getHours(); return h < 6 || h >= 19; };
export const biomaActual = (ms = Date.now()) => ['hierba', 'agua', 'cueva'][Math.floor(ms / 600000) % 3];
// catchBall: agregar  case 'dusk': return (ctx.noche || ctx.bioma === 'cueva') ? 3.5 : 1;
export function rolarTam(rng = Math.random) { const r = rng(); return r < 0.03 ? 'XXS' : r < 0.12 ? 'S' : r > 0.97 ? 'XXL' : r > 0.88 ? 'L' : 'M'; }
```

## Código / datos

- **`web/src/lib/safari-core.js`:** `shinyChance`, `pisoRacha`, `esNoche`, `biomaActual`, `rolarTam` +
  `catchBall` gana el caso `dusk`. (Funciones puras; `catchBall`/`probCaptura` ya reciben `ctx`.)
- **`web/src/lib/coleccion.js`:** `racha`/`subirRacha`/`romperRacha`; `encontrar` (filtra por bioma con
  fallback, shiny por racha, IVs perfectos = max(alfa, pisoRacha), tam, devuelve `bioma`/`noche`);
  `capturar` (subir/romper racha; pasa `noche`/`bioma` al ctx); `atrapar` acepta `tam`. Import `biomas.json`.
- **`web/scripts/gen-biomas.mjs`** → `web/src/data/biomas.json` (habitat PokeAPI, dex 1..721).
- **`web/src/lib/items.js`:** Dusk Ball. **`web/src/lib/sprites.js`:** `ballSvg` variante `balldusk`.
- **`web/src/pages/safari.astro`:** badges (🔥 Racha, bioma, día/noche) en la arena; el encuentro usa
  bioma/hora; resumen muestra racha + tamaño/título; "Huir" rompe racha.
- **`web/src/pages/pokedex.astro`:** chip de tamaño en el modal.
- **`web/src/pages/tienda.astro`:** Dusk Ball a la venta.
- **`web/src/pages/ayuda.astro`:** documentar Fase 2.

## Tests

- **`web/src/lib/safari-core.test.mjs`** (`node --test`, amplía el de Fase 1):
  - `shinyChance`: monótona creciente, racha 0 = 0.01, cap 0.08.
  - `pisoRacha`: 14→0, 15→1, 30→2, 50→3.
  - `esNoche`: hora 23 → true, hora 12 → false (construir `new Date()` con horas fijas).
  - `biomaActual`: determinista; `Math.floor(ms/600000)%3` mapea a los 3 biomas; ms y ms+599999 dan igual.
  - `catchBall` dusk: noche o cueva → 3.5; día+superficie → 1.
  - `rolarTam`: rng 0.01→'XXS', 0.5→'M', 0.99→'XXL'; siempre ∈ {XXS,S,M,L,XXL}.
- `cd web && node --test src/lib/safari-core.test.mjs` verde; `npm run build` verde; `cd api && npx jest`
  sin regresiones (no se toca el motor).
- Verificación visual (`/frontend-design`): badges del safari, resumen con racha + tamaño, Dusk Ball en
  tienda, chip de tamaño en el modal — tema oscuro y claro.

## Retro-compat

- Sin migración. `col:racha` ausente = 0. Instancias sin `tam` = 'M'. `biomas.json` nuevo (si un id falta
  → 'hierba'). Las balls/identidad de Fase 1 intactas.

## Fuera de alcance (Fase 3 / futuro)

- EVs en PvP, reset de EV / bayas (Fase 3). Rastreo de especie (DexNav) — se descartó a favor de la racha
  simple. Pools día/noche separados (acá la hora solo afecta Dusk Ball + badge). Tamaños que afecten stats.

## Archivos afectados (estimado)

- `web/src/lib/safari-core.js` (+ `.test.mjs`), `coleccion.js`, `items.js`, `sprites.js`.
- `web/scripts/gen-biomas.mjs`, `web/src/data/biomas.json`.
- `web/src/pages/safari.astro`, `pokedex.astro`, `tienda.astro`, `ayuda.astro`.
- `web/src/styles/global.css`, `docs/` (rebuild).
