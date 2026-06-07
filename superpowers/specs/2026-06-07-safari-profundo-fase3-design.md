# Safari profundo — Fase 3: EVs en PvP + reset/bayas

**Fecha:** 2026-06-07
**Estado:** diseño aprobado, pendiente plan de implementación.
**Tema:** cerrar el loop de EVs de [[identidad-pokemon]]: otorgar EVs ganando en PvP (server) y poder
**bajar/resetear** EVs con bayas (client). Última fase del [[safari-profundo]].

## Decisiones tomadas (brainstorming 2026-06-07)

1. **EVs en PvP — ambos jugadores, por rivales derrotados.** Al terminar, cada jugador suma los yields de
   los Pokémon rivales que quedaron **debilitados** (hp≤0), aplicados a los **3 Pokémon que trajo**
   (match por `iid` en el blob `col:pc`). Se calcula del estado final (sin tocar el motor). Server-side.
2. **Reset/bayas — 6 bayas (−10/stat) + Borrón total** (todos los EVs a 0). Client-side, espejo de las
   vitaminas (+10). Se compran en la tienda, se usan desde el modal Pokédex.

## Estado actual (contexto)

- **Práctica** (client) ya da EVs: `batalla.astro` llama `darEV(miAct().iid, yieldDe(def.id))` al tumbar
  un CPU ([[identidad-pokemon]]). `coleccion.js` tiene `darEV`, `evsDe`, `yieldDe`, `usarVitamina` (vitaminas
  +10, cap 100/vía). `combate-core.ts` tiene `sumarEV(evs, yields)` (cap 252/stat, 510 total).
- **PvP** (server): `insignias.premiar(progreso, estado, abandonoUid)` corre al `fin` (desde
  `salas.service.finalizar`). `aplicarUno(progreso, yo, rival, gano, …)` lee el blob de progreso de cada
  jugador (`progreso.bajar(uid)`), aplica premios (caramelos/balls/ELO `col:pvp`), persiste y devuelve
  `Premios` con el `estado` (blob) que se emite al cliente (`progreso` event → refresca su nube).
  Helpers de blob: `pObj(e,k,def)` / `setObj(e,k,v)` (valores serializados, como localStorage).
- `yields.json` YA está server-side (`api/src/batalla/data/yields.json`, en el `FILES` del sync).
  `sumarEV` YA está en el `combate-core.ts` server (sincronizado).
- Los `Combatiente` del estado PvP llevan `iid` + `id`. El blob `col:pc` = array de instancias (con `evs`).

## A. EVs en PvP (server, `insignias.ts`) — owner-gated por el deploy

- **Pura, testeable** (en `combate-core.ts`, junto a `sumarEV`):
  ```ts
  // suma de yields de los Pokémon de un equipo que quedaron debilitados (hp<=0).
  export function evPorDerrotados(equipo: { id: number; hp: number }[], yields: Record<string, number[]>): number[] {
    const out = [0, 0, 0, 0, 0, 0];
    for (const c of equipo) if (c.hp <= 0) { const y = yields[String(c.id)] || []; for (let i = 0; i < 6; i++) out[i] += (y[i] || 0); }
    return out;
  }
  ```
- **En `aplicarUno`** (después de los premios materiales), agregar:
  ```ts
  const yv = evPorDerrotados(rival.equipo, yields as any);
  if (yv.some((n) => n > 0)) {
    const pcArr = pObj(estado, 'col:pc', []);
    for (const c of yo.equipo) { const m = pcArr.find((x: any) => x.iid === c.iid); if (m) m.evs = sumarEV(m.evs || [0, 0, 0, 0, 0, 0], yv); }
    setObj(estado, 'col:pc', pcArr);
    premios.ev = yv;
  }
  ```
  (Import `yields` de `./data/yields.json`, `evPorDerrotados`/`sumarEV` de `./combate-core`. `Premios`
  gana `ev?: number[]`.) Ambos jugadores reciben (cada uno por los rivales que derrotó). Se persiste en el
  mismo flujo que ya persiste el blob; el cliente recibe el blob actualizado por el `progreso` event.
- **Cliente:** el modal de resultado del PvP (`batalla.astro`, modo En vivo) muestra "+EVs" si
  `premios.ev` trae algo (chico, opcional). El blob ya refresca la nube → la Pokédex muestra los EVs nuevos.
- **Owner-gated:** redeploy de la imagen arm64 a la Pi (cross-build + `docker save|ssh load` + `compose up`),
  como las fases PvP anteriores ([[coleccion-v2-batalla]]). ⚠️ Si cambian datos del front, correr
  `node api/scripts/sync-batalla-data.mjs` antes del re-cross-build.

## B. Reset / bayas (client)

- **Math puro** (`combate-core.ts`, espejo de `sumarEV`):
  ```ts
  // baja `n` EV de un stat (floor 0). Devuelve copia.
  export function restarEV(evs: number[], idx: number, n: number): number[] {
    const out = (evs && evs.length === 6) ? [...evs] : [0, 0, 0, 0, 0, 0];
    out[idx] = Math.max(0, out[idx] - n);
    return out;
  }
  ```
- **Items** (`items.js`, cat `'ev'`, pagan Pokébolas). 6 bayas (campo `baja: idx`, baja 10 EV de ese stat) +
  Borrón:
  ```js
  bayaps:   { nombre: 'Baya Zreza',  sprite: 'baya', cat: 'ev', baja: 0, precio: 20, desc: '−10 EV de PS.' },
  bayaatk:  { nombre: 'Baya Pomeg',  sprite: 'baya', cat: 'ev', baja: 1, precio: 20, desc: '−10 EV de Ataque.' },
  bayadef:  { nombre: 'Baya Kelpsy', sprite: 'baya', cat: 'ev', baja: 2, precio: 20, desc: '−10 EV de Defensa.' },
  bayaspa:  { nombre: 'Baya Hondew', sprite: 'baya', cat: 'ev', baja: 3, precio: 20, desc: '−10 EV de At. Esp.' },
  bayaspd:  { nombre: 'Baya Grepa',  sprite: 'baya', cat: 'ev', baja: 4, precio: 20, desc: '−10 EV de Def. Esp.' },
  bayavel:  { nombre: 'Baya Tamato', sprite: 'baya', cat: 'ev', baja: 5, precio: 20, desc: '−10 EV de Velocidad.' },
  borrador: { nombre: 'Borrón EV',   sprite: 'borrador', cat: 'ev', reset: true, precio: 60, desc: 'Pone TODOS los EVs en 0.' },
  ```
  (Las vitaminas ya en cat `'ev'` tienen campo `ev`; las bayas usan `baja`; el Borrón `reset:true`. El
  catálogo distingue por esos campos.)
- **`coleccion.js`:**
  ```js
  export function bajarEV(iid, statIdx) {
    const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
    const ev = evsDe(m); if (ev[statIdx] <= 0) return false;
    m.evs = restarEV(ev, statIdx, 10); setPC(arr); return true;
  }
  export function resetEV(iid) {
    const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
    if (evsDe(m).every((v) => v === 0)) return false;
    m.evs = [0, 0, 0, 0, 0, 0]; setPC(arr); return true;
  }
  ```
  (Import `restarEV` de `./combate-core.ts`.)
- **Modal Pokédex** (`pokedex.astro`, en `estatsBloque`): junto al botón de vitamina "+10" de cada stat,
  un botón **"−10"** si tenés la baya correspondiente (`tieneItem(bayaDe[i])` y `ev>0`) → `bajarEV(iid,i)` +
  `usarItem(baya)` + re-render. Y un botón global **"♻️ Reset EVs"** (si `tieneItem('borrador')` y hay EVs)
  → `resetEV(iid)` + `usarItem('borrador')` + re-render. Espejo exacto del flujo de vitaminas (handler
  `[data-baja-stat]` / `[data-reset-ev]` análogo a `[data-vit-stat]`).
- **Tienda** (`tienda.astro`): las bayas + Borrón aparecen en la cat `'ev'` (junto a las vitaminas), render
  existente.
- **Sprites SVG** (regla CLAUDE.md, NO emoji): `bayaSvg` (baya redonda con hoja/brillo, **color-coded por
  stat** como las vitaminas) + sprite del **Borrón** (goma de borrar / X). `itemSvg('baya', size, color)` y
  `itemSvg('borrador', size)`. `/frontend-design`, coherentes con la familia de items.

## Tests

- **`api/src/batalla/combate-core.spec.ts`** (jest, corre sobre la copia sincronizada):
  - `restarEV`: `restarEV([20,0,...],0,10) → [10,0,...]`; floor 0 (`restarEV([5,...],0,10)[0]===0`).
  - `evPorDerrotados`: equipo con 2 debilitados + 1 vivo → suma de los yields de los 2 debilitados; equipo
    todo vivo → `[0,0,0,0,0,0]`.
- `cd api && node scripts/sync-batalla-data.mjs && npx jest` verde (incluye motor + core).
- `cd web && npm run build` verde. Verificación visual (`/frontend-design`): bayas/Borrón en la tienda,
  botones −10 / Reset en el modal Pokédex, sprites coherentes — tema oscuro y claro.

## Retro-compat

- Sin migración. Instancias sin `evs` = ceros. `restarEV`/`resetEV` no fallan si faltan. El blob `col:pc`
  del server ya existe; agregar `evs` a un mon que no lo tenía = empieza en lo que `sumarEV` calcule.

## Orden sugerido / scope

- **Parte B (bayas, client)** primero — shippeable de inmediato (sin deploy).
- **Parte A (EVs en PvP, server)** después — requiere redeploy a la Pi (owner-gated); el e2e real de 2
  sesiones lo corre el dueño.

## Fuera de alcance

- EVs por PvP atribuidos por-KO real (se eligió "por rivales derrotados", sin tocar el motor). Bayas que
  además curen/confundan (acá solo bajan EV). Límite de bayas por compra.

## Archivos afectados (estimado)

- `web/src/lib/combate-core.ts` (`restarEV`, `evPorDerrotados`) + `api/.../combate-core.ts` (sync) +
  `api/src/batalla/combate-core.spec.ts` (tests).
- `api/src/batalla/insignias.ts` (EVs en PvP + `Premios.ev`).
- `web/src/lib/coleccion.js` (`bajarEV`, `resetEV`), `items.js` (bayas + Borrón), `sprites.js` (`baya`/`borrador`).
- `web/src/pages/pokedex.astro` (botones −10 / Reset), `tienda.astro` (verificar render), `batalla.astro`
  (mostrar +EVs en el resultado PvP), `ayuda.astro` (documentar).
- `web/src/styles/global.css`, `docs/` (rebuild).
