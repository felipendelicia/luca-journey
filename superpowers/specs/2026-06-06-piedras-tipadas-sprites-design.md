# Piedras evolutivas tipadas + sprites originales — Diseño

> Estado: aprobado (brainstorm 2026-06-06). Verificable 100% local (build + screenshot).

## Objetivo

1. **Piedras evolutivas por tipo** (Fuego, Agua, Trueno, Hoja, Lunar, Solar, Día, Alba, Noche),
   compradas en la Tienda, cada una usable solo en las evoluciones reales que la requieren.
2. **Sprites originales (SVG)** fieles al canon Pokémon para: piedras, Pokéballs y las **48
   medallas** de `/liga` (hoy todo emoji).

## Contexto (estado actual)

- `web/src/lib/items.js`: una sola `piedra` genérica (item de tienda, cat `evo`).
- `web/src/lib/coleccion.js`: `opcionesEvo`/`evolucionarInst`. Las evos "por piedra" son las de
  `evoData[id].evos[].nivel === 0` y consumen 1 `piedra` genérica.
- `web/src/data/evoluciones.json`: generado por `scripts/gen-evoluciones.mjs` desde **PokeAPI**;
  hoy guarda solo `{a, nivel}` y **descarta el método** (item/trigger/held/happiness).
- `nivel === 0` mezcla TODO lo no-nivel: piedra (41), intercambio (25), amistad (16), otras (29).
- Pokeballs: emoji `🔴🔵🟡` en safari/tienda. Existe un pokeball CSS-art para la animación de tiro
  (`global.css:509`).
- Medallas: `liga.astro` `BADGES` = 48 pares `[nombre, emoji]` (6 regiones × 8).
- Repo: 1 solo SVG (favicon); el resto emoji.

## Datos reales (PokeAPI, dex 1–721)

Evos por **use-item** (piedra), con el `item.name` exacto:
`fire-stone(4) water-stone(6) thunder-stone(3) leaf-stone(5) moon-stone(6) sun-stone(5)
shiny-stone(4) dusk-stone(4) dawn-stone(2)` → **9 piedras**. (`black-augurite`/`peat-block` son de
Legends-Arceus y apuntan a dex >721 → se excluyen.)
Triggers no-piedra: `trade` (25, con/ sin held-item), `min_happiness` (16), `otros` (location/move…).

## Diseño

### 1. Data — método de evolución

Extender `gen-evoluciones.mjs`: por cada evo, además de `nivel`, derivar `req` (item id requerido)
y `m` (tag de método) desde `evolution_details[0]`:

- `trigger === 'use-item'` → `req = MAP_STONE[item.name]`, `m = 'piedra'`.
- `trigger === 'trade'` → `req = 'discoenlace'`, `m = 'trade'`.
- `min_happiness` → `m = 'amistad'`, `req` ausente.
- resto no-nivel → `m = 'otro'`, `req` ausente.
- nivel-up (`min_level`) → `nivel = min_level`, sin `req`.

`MAP_STONE`: `fire-stone→piedrafuego, water-stone→piedraagua, thunder-stone→piedratrueno,
leaf-stone→piedrahoja, moon-stone→piedraluna, sun-stone→piedrasol, shiny-stone→piedradia,
dawn-stone→piedraalba, dusk-stone→piedranoche`.

Filtrar evos con `a > 721` (targets inexistentes en `pokemon.json`). Regenerar y commitear
`evoluciones.json`. Shape nuevo: `{a, nivel, req?, m?}` (retrocompatible: `nivel` sigue).

### 2. Tienda — `items.js` + `tienda.astro`

Reemplazar `piedra` por 9 piedras tipadas (cat `evo`) + 1 `discoenlace`:

| id | nombre | precio |
|---|---|---|
| piedrafuego | Piedra Fuego | 80 |
| piedraagua | Piedra Agua | 80 |
| piedratrueno | Piedra Trueno | 80 |
| piedrahoja | Piedra Hoja | 80 |
| piedraluna | Piedra Lunar | 80 |
| piedrasol | Piedra Solar | 80 |
| piedradia | Piedra Día | 80 |
| piedraalba | Piedra Alba | 80 |
| piedranoche | Piedra Noche | 80 |
| discoenlace | Disco de Enlace | 80 |

- `piedra` legacy = **comodín** (no listada en tienda, no comprable): sirve para cualquier evo cuyo
  `req` empiece con `piedra`. Migra el stock existente sin pérdida.
- `tienda.astro`: la sección `evo` lista las 10 nuevas con su sprite SVG. Cada `desc` aclara qué
  evoluciona (ejemplos canónicos).

### 3. Lógica evo — `coleccion.js`

`opcionesEvo(iid)` devuelve por opción: `{a, nivel, costo, ok, req}` donde `req = ev.req || null`.
`ok = (ev.nivel>0 ? m.nivel>=ev.nivel : true) && tieneReq(req) && car>=costo`.

`tieneReq(req)`: `!req || tieneItem(req) || (esPiedra(req) && tieneItem('piedra'))`.
`esPiedra(req)`: `req && req.startsWith('piedra')`.

`evolucionarInst`: si `req`, consumir: `usarItem(req) || (esPiedra(req) && usarItem('piedra'))`;
si no se pudo, abortar.

`pokedex.astro` modal: usa `req` para mostrar el sprite + nombre de la piedra concreta que falta y el
link a Tienda (en vez del genérico "Piedra Evolutiva").

### 4. Sprites — `src/lib/sprites.js`

Módulo único que exporta builders que devuelven **string de SVG** (usable tanto en `.astro` inline
como en scripts cliente que arman DOM por `innerHTML`):

- `stoneSvg(itemId, size?)` — 9 piedras (gema tallada fiel: llama naranja, lágrima azul, rayo
  amarillo, hoja verde, luna oscura con creciente, sol radiante, brillo/diamante, alba turquesa,
  noche violácea) + comodín genérico para `piedra`.
- `ballSvg(tier, size?)` — `0` Poké, `1` Super, `2` Ultra (rojo/azul/amarillo fieles, con brillo).
- `badgeSvg(region, i, ganada, size?)` — **48 medallas únicas** fieles por gimnasio; `ganada=false`
  → silueta apagada.

Theme-aware (usa `currentColor`/gradientes propios; legibles en oscuro y claro). Reemplazan emoji en:
`tienda.astro` (sección evo + saldo de balls), `safari.astro` (icono de ball + saldo), `liga.astro`
(`BADGES`), `pokedex.astro` (modal evo: piedra que falta), e inventarios.

### 5. Ayuda

`ayuda.astro`: actualizar la mención de "Piedra Evolutiva" → piedras por tipo + Disco de Enlace;
explicar qué evoluciona cada una y dónde se usan (Pokédex).

## Fases de implementación

- **F1 — funcional:** data (§1) → items (§2) → lógica evo (§3) → wiring tienda/pokedex.
- **F2 — sprites:** `sprites.js` (§4): piedras → balls → 48 medallas; wiring en las 4 páginas.
- **F3:** ayuda + `npm run build` + screenshots (tienda, liga, safari, pokedex) + commit.

## No-objetivos (YAGNI)

- No rastrear amistad real (las evos por amistad siguen siendo solo-caramelos).
- No Ice Stone (no aparece en dex 1–721 vía use-item).
- No Master Ball (no está en la economía actual).
- No tocar el balance de caramelos (`costoEvo` queda igual).
