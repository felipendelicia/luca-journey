# Batalla v2 — estados alterados, fallar y música — Diseño

> Estado: aprobado (brainstorm 2026-06-06). Toca DOS motores (cliente `batalla.js` + server
> `motor.ts`); el PvP requiere redeploy de la Pi (owner-gated para ir live, pero el agente puede
> deployar con el pipeline ya probado).

## Objetivo

Acercar las batallas (práctica vs CPU y PvP en vivo) a la experiencia Pokémon Rojo Fuego:
1. **Música de fondo** de batalla (chiptune original, sintetizada).
2. Los ataques pueden **fallar** (precisión).
3. **Estados alterados**: Envenenado, Quemado, Paralizado, Dormido, Congelado, Confuso.

## Contexto

- `web/src/data/movimientos.json` ya tiene `{nombre,tipo,poder,precision,pp,categoria,desc}`.
  **Falta** `ailment` (estado que causa) — disponible en PokeAPI `move.meta.ailment` + `ailment_chance`.
- Motor cliente: `web/src/lib/batalla.js` (puro) + orquestación en `web/src/pages/batalla.astro`
  (async, con animaciones). Motor server: `api/src/batalla/motor.ts` (autoritativo) + `salas.service.ts`.
  Son duplicados por diseño (el server no confía en el cliente).
- Audio: `web/src/lib/sonidos.js` = synth Web Audio con mute (`muteado`/`toggleSonido`/`sonidoActivo`).
- `api/src/batalla/data/` es copia de `web/src/data` (Docker buildea solo `./api`); la regenera
  `api/scripts/sync-batalla-data.mjs`.

## A. Data — `ailment` en los movimientos

Extender `gen-movimientos-detalle.mjs`: por cada move agregar, si aplica, `ailment` (id ES) y
`ailmentChance` (0-100) desde `mv.meta`. Mapa PokeAPI→id:
`poison→veneno, burn→quemadura, paralysis→paralisis, sleep→sueno, freeze→congelado, confusion→confusion`.
Otros/none → sin campo. Regenerar (PokeAPI) y commitear `movimientos.json` + `learnsets.json`; correr
`node api/scripts/sync-batalla-data.mjs`.

## B. Fallar (precisión)

En ambos motores, al usar un move (de daño o de estado): `acierta = rng()*100 < (precision ?? 100)`.
Si falla → no hay daño ni efecto; mensaje "¡{Pokémon} falló el ataque!". Determinista vía `rng`
inyectable (el server ya lo soporta; los tests lo usan).

## C. Estados (6) — modelo compartido

Cada combatiente gana `estado` (`null | 'veneno' | 'quemadura' | 'paralisis' | 'sueno' | 'congelado'
| 'confusion'`) y `estadoT` (contador de turnos para sueño/confusión). **Un solo estado a la vez.**

Reglas (idénticas en `batalla.js` y `motor.ts`):
- **veneno / quemadura:** al final de SU turno pierde `floor(hpMax/8)` HP. Quemadura además aplica
  **×0.5 al daño físico** (categoría 'Físico') que hace.
- **paralisis:** al tocarle el turno, 25% de "no se puede mover" (pierde el turno).
- **sueno:** no actúa; `estadoT` 1-3 al dormirse, baja 1 por turno; al llegar a 0 despierta ese turno.
- **congelado:** no actúa; 20%/turno de descongelar. Recibir un move de **Fuego** lo descongela.
- **confusion:** `estadoT` 1-4 al confundirse; cada turno 33% de pegarse a sí mismo (daño fijo
  chico) en vez de actuar; baja el contador; a 0 se despeja.
- **Aplicar:** si el move tiene `ailment` y `rng()*100 < ailmentChance` y el objetivo `estado===null`
  → set estado (+ `estadoT` para sueño/confusión). Mensajes: "¡{X} fue envenenado/quemado/…!".

Helpers puros (en cada motor):
- `puedeActuar(c, rng)` → `{ actua:boolean, texto:string, autogolpe?:number }` (resuelve para/sueño/
  congelado/confusión, decrementa contadores, descongela, etc.).
- `aplicarAilment(mov, atacante, defensor, rng)` → texto|'' (set estado en defensor si corresponde;
  Fuego descongela al defensor antes).
- `tickEstado(c)` → `{ dmg, texto }` (DOT de veneno/quemadura al final del turno).
- daño físico: si `atacante.estado==='quemadura'` y `mov.categoria==='Físico'` → ×0.5.

### Integración

- **Práctica (`batalla.astro`):** el flujo `turno`/`turnoRival` consulta `puedeActuar` antes de
  actuar (si no, mensaje + cede turno), aplica `aplicarAilment` al pegar, y corre `tickEstado` al
  cierre del turno de cada lado (mensaje + animación de daño). Chips de estado en el HUD.
- **PvP (`motor.ts`):** `Combatiente` gana `estado`/`estadoT`. En `aplicarAccion` (mover/super):
  `puedeActuar` al inicio (si no actúa, igual pasa turno + tick), `aplicarAilment` al pegar,
  `tickEstado` del que actuó al final. `snapshot()` incluye `estado`/`estadoT` por combatiente.

## D. Música (chiptune original)

`sonidos.js`: componer un loop 8-bit original (bajo en triangle + melodía en square, ~8-16s),
agendado con lookahead sobre el `AudioContext` existente. API: `iniciarMusicaBatalla()`,
`detenerMusicaBatalla()`. Respeta `muteado()`; el `toggleSonido` existente la corta/reanuda.
- Arranca en el **gesto** de empezar la pelea (práctica: `empezar()`; PvP: al entrar a combate).
  Para en `terminar`/`fin`/salir del combate. Botón 🔊/🔇 en el HUD de batalla.
- Cliente puro → práctica y PvP, sin redeploy.

## E. UI

Chip de estado junto a la barra de HP de cada activo: ☠️ veneno, 🔥 quemadura, ⚡ paralisis,
💤 sueno, ❄️ congelado, 💫 confusion (color por estado). Mensajes en el textbox. Animación de daño
por DOT (flash del sprite). En PvP el cliente lee `estado` del snapshot.

## F. Tests + deploy

- `motor.spec.ts`: miss (precision 0 → falla), veneno/quemadura restan HP al cierre, dormido saltea
  y despierta, quemadura ×0.5 al físico, paralizado saltea (rng), congelado saltea + deshiela con
  Fuego, confusión auto-golpe. Todos con `rng` fijo.
- `web build` + `nest build` + `jest` verdes → cross-build arm64 + redeploy Pi (`docker save|ssh load`
  + `compose up`) + `node api/scripts/sync-batalla-data.mjs` antes del build + push de `docs/`.

## Fases

1. **F1 data:** ailment en `movimientos.json` (regen + sync).
2. **F2 práctica:** helpers en `batalla.js` + integración + UI en `batalla.astro`.
3. **F3 PvP:** `motor.ts` + snapshot + UI online + `motor.spec.ts`.
4. **F4 música:** `sonidos.js` + wiring + botón.
5. **F5:** build + redeploy Pi + push + verificación.

## No-objetivos (YAGNI)

- Tóxico escalonado (badly poison) — el veneno es 1/8 fijo.
- Estados múltiples simultáneos / estados de campo (clima, pantallas).
- Cambios de prioridad/velocidad por parálisis (solo el skip-chance).
- Música por región/escena; un solo loop de batalla.
