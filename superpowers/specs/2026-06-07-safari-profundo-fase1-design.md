# Safari profundo — Fase 1: encuentro con destreza + decisión informada

**Fecha:** 2026-06-07
**Estado:** diseño aprobado, pendiente plan de implementación.
**Tema:** profundizar el Safari. Reemplaza la captura auto por un **encuentro en 2 pasos** con
tasación, selección de ball, minijuego de tiro y escape. Sinergia directa con
[[identidad-pokemon]] (cazar el "perfecto").

Parte de un roadmap en 3 fases (decompuesto en brainstorming 2026-06-07):
- **Fase 1 (este spec):** encuentro con destreza + decisión informada + roster de balls + selector.
- **Fase 2 (spec futuro):** encadenado shiny (sube odds shiny/IV), biomas/hora del día, Dusk Ball, alfa más rico.
- **Fase 3 (spec futuro, chico):** EVs en PvP, reset de EV / bayas.

## Estado actual (contexto)

`web/src/lib/coleccion.js` → `tirar(pokemon, temas, pesos)`: filtra pool por regiones desbloqueadas,
elige por peso de rareza (`elegirPonderado`), aplica `BALL_BOOST[mejorBallTier()]` (shiny/nivel/rareza/
caramelos) y **captura automático** (1 ball = 1 captura, sin escape). `safari.astro` revela y captura.
Balls actuales (`items.js`, cat `'ball'`): `pokeball`(t0), `superball`(t1=Great), `ultraball`(t2);
`BALL_BOOST` da multiplicadores de aparición. Shiny base `PROB_SHINY=0.01`.
Identidad: `rolarIdentidad(id, habilidades)` ya existe ([[identidad-pokemon]]).

## Decisiones tomadas (brainstorming 2026-06-07)

1. **Escape escalado por rareza**, mitigado por ball + calidad de tiro. Comunes casi siempre caen;
   raros/legendarios pueden zafar y huir. La ball y el skill importan, sin frustrar el grind común.
2. **Reveal pre-captura:** tasación **aproximada** (⭐0-4 IV) + naturaleza + marca alfa + nivel.
   **Shiny SÍ se revela en el encuentro** (✨ + sprite shiny) → tensión "atrapalo antes de que huya".
   IVs exactos recién post-captura (modal Pokédex, ya existe).
3. **Minijuego:** **anillo que se contrae** (GO-style) → Excelente / Genial / Bien / Normal.
4. **La calidad de tiro afecta:** prob. de captura ↑ + **piso de IVs en Excelente** (los 2 IVs más
   bajos suben a 31). **NO** afecta shiny (el shiny ya se vio en el encuentro).
5. **Shiny:** determinado/revelado en el encuentro, odds base `PROB_SHINY`. El boost de odds va por
   **encadenado (Fase 2)**, no por ball/tiro.
6. **Alfa** (~4% de encuentros): **3 IVs perfectos garantizados** + flag `alfa:true` en la instancia +
   marca 👑 en tasación/captura/modal.
7. **Compañero** (`col:companero` = iid; selector en safari): si su habilidad es **Sincronía**
   (`synchronize`), la naturaleza del salvaje = la del compañero (**100%**, QoL). Base para Buddy futura.
8. **Selector de ball:** elegís cuál tirar de tu inventario; se consume **esa** (no `mejorBallTier`
   automático). Roster nuevo: **Veloz, Turno, Red, Repetición, Master, Xeneize (Boca 💙💛)**.

### Cambio de semántica de balls (importante)

Como la ball se elige **después** del encuentro, los boosts de **aparición** (rareza/nivel/shiny) de
`BALL_BOOST` ya no tienen dónde aplicarse. → **Las balls pasan a afectar SOLO la captura** (campo
`catch` + condición). El encuentro (especie/nivel/shiny/identidad) es **independiente de la ball**.
Super/Ultra dejan de "subir rareza/shiny" y pasan a "mejor captura" (×1.5 / ×2), que ahora importa
porque la captura es mecánica real. `BALL_BOOST` se retira; se reemplaza por `catch`/`cond` por ball.

## Flujo (reemplaza `tirar()` auto)

```
[arena] → encontrar()
  ├─ rolea especie (pool ponderado por rareza, regiones desbloqueadas)
  ├─ rolea identidad (rolarIdentidad → ivs/nat/hab/gen)
  ├─ rolea shiny (PROB_SHINY) y alfa (~4%)
  ├─ alfa → pisoIV garantizado (3 perfectos)
  ├─ Sincronía: si compañero tiene 'synchronize' → nat = nat(compañero)
  └─ devuelve `encuentro` (transitorio, NO persistido)
        ↓
[carta de encuentro] sprite(shiny✨/alfa👑) · Nv · ⭐tasación IV · naturaleza · [selector de ball] · [Tirar][Huir]
        ↓ Tirar (con ball elegida)
[overlay de tiro] anillo que se contrae → calidad (Excelente/Genial/Bien/Normal)
        ↓ capturar(encuentro, ballKey, calidad, ctx)
  ├─ consume 1 de ballKey
  ├─ prob = probCaptura(rarezaTier, ballDef, {tiroN, calidad, tiposWild, vistoYa})   (Master → 1)
  ├─ éxito → pisoIV(ivs, calidad) [Excelente] → persiste instancia (con alfa) → resultado captura
  └─ fallo → ¿huye? (fleeProb por rareza) → sí: encuentro termina (perdido) · no: tiroN++ (re-tirar, otra ball)
```

## Mecánicas (puras → `safari-core.js`)

```js
// captura base por tier de rareza (1..10): comunes alto, legendarios bajo.
baseCaptura(tier) = clamp(1.0 - tier*0.08, 0.12, 0.95)
// multiplicador por calidad de tiro
MULT_CALIDAD = { Normal: 1.0, Bien: 1.3, Genial: 1.7, Excelente: 2.2 }
// modificador de la ball (puede depender del contexto)
catchBall(ballDef, ctx) =
  master → Infinity (captura segura)
  veloz  → ctx.tiroN === 1 ? 4 : 1
  turno  → 1 + ctx.tiroN * 0.3
  red    → (ctx.tiposWild ∩ {Bicho, Agua}) ? 3 : 1
  repeticion → ctx.vistoYa ? 3 : 1
  else   → ballDef.catch   // poke 1, super 1.5, ultra 2, xeneize 2
probCaptura(tier, ballDef, ctx) = ballDef.key==='master' ? 1
  : clamp(baseCaptura(tier) * catchBall(ballDef, ctx) * MULT_CALIDAD[ctx.calidad], 0, 1)

// huida tras fallo (raros huyen más)
fleeProb(tier) = clamp(0.10 + tier*0.035, 0.10, 0.5)

// piso de IVs por Excelente: los 2 índices con menor IV → 31
pisoIV(ivs, calidad) = calidad==='Excelente' ? (subir los 2 mínimos a 31) : ivs

// Sincronía (pura): hab y nat del compañero → nat o null
sincronizaNat(compHab, compNat) = compHab === 'synchronize' ? compNat : null
```

## Roster de balls (`items.js`, cat `'ball'`)

| key | nombre | catch | cond / nota | precio |
|---|---|---|---|---|
| pokeball | Poké Ball | 1 | base (existente) | — |
| superball | Super Ball | 1.5 | (existente; era Great) | 25 |
| ultraball | Ultra Ball | 2 | (existente) | 60 |
| veloz | Ball Veloz | — | ×4 primer tiro, ×1 luego | 25 |
| turno | Ball Turno | — | ×(1+tiroN·0.3) | 25 |
| red | Ball Red | — | ×3 vs Bicho/Agua | 30 |
| repeticion | Ball Repetición | — | ×3 si especie en `vistos` | 30 |
| master | Master Ball | ∞ | captura 100%; **no venta normal** (premio raro / precio altísimo, ej. 5000) | — |
| xeneize | Ball Xeneize 💙💛 | 2 | cosmética Boca (azul/oro) + FX confeti azul-oro al capturar | 80 |

(El owner ajusta precios / cómo se consigue la Master.)

## Superficies de UI (→ skill `/frontend-design`, tema-aware, retro-Pokédex/CRT)

- **`safari.astro`** — encuentro en 2 pasos:
  - **Carta de encuentro:** sprite (shiny ✨ / alfa 👑 con aura), nivel, **⭐ tasación IV** (0-4),
    naturaleza, + **selector de balls** (chips con sprite + contador; deshabilita las que no tenés) +
    **Tirar** (con la ball elegida) / **Huir**.
  - **Overlay de tiro:** **anillo que se contrae** sobre el Pokémon; tap/click → calidad
    (Excelente/Genial/Bien/Normal con feedback). Resultado: captura (FX por rareza/shiny/alfa; confeti
    azul-oro si Xeneize) / "¡Zafó!" / "¡Huyó!".
  - **Selector de compañero:** elegís un Pokémon del PC como compañero (para Sincronía). Persistente.
- **`pokedex.astro`** — marca **alfa 👑** en el modal de instancia (junto al género/shiny).
- **`tienda.astro`** — las balls nuevas en la cat `'ball'` (reusa el render existente).
- **`sprites.js`** — `ballSvg` gana variantes: veloz, turno, red, repeticion, master, xeneize.
  Fieles + coherentes con la familia de balls (mismo contorno/brillo). Xeneize = azul/oro.

## Código / datos

- **`web/src/lib/safari-core.js`** (NUEVO, puro — sin DOM, sin import de JSON): `baseCaptura`,
  `MULT_CALIDAD`, `catchBall`, `probCaptura`, `fleeProb`, `pisoIV`, `sincronizaNat`, `calidadDeAnillo`
  (radio del anillo → calidad). Testeable con el runner nativo de Node.
- **`web/src/lib/coleccion.js`**:
  - `encontrar(pokemon, temas, pesos)` → objeto encuentro `{id, nivel, ivs, nat, hab, gen, shiny, alfa,
    rarezaTier, estrellas, naturalezaNombre, tiposWild, vistoYa}`. No persiste. Aplica Sincronía
    (vía `companero()`) y alfa-pisoIV.
  - `capturar(enc, ballKey, calidad, ctx)` → consume `ballKey` (valida tenencia), `probCaptura`,
    en éxito aplica `pisoIV` y persiste la instancia (reusa la lógica de `atrapar`, sumando
    `alfa`). Devuelve `{ok, inst?, huyo?, calidad, prob}`.
  - `companero()` / `setCompanero(iid)` (`col:companero`, sync nube como el resto de `col:*`).
  - `tirar` queda **deprecado** (o se elimina su uso; safari pasa al flujo nuevo).
- **`web/src/lib/items.js`**: balls nuevas con `catch`/`cond`; retirar `BALL_BOOST` (o vaciarlo).
  Reconciliar `mejorBallTier`/usos: el safari ya no auto-elige; otros usos (si los hay) se revisan.
- **`web/src/lib/sprites.js`**: variantes de `ballSvg`.
- `atrapar(id, {shiny, nivel, alfa, ivs, nat, hab, gen})` — extender para aceptar identidad+alfa ya
  roleados por `encontrar` (hoy rolea adentro). Mantener compat (si no se pasan, rolea).

## Tests

- **`web/src/lib/safari-core.test.mjs`** (`node --test`, runner nativo, sin deps nuevas):
  - `probCaptura`: comunes alta / leg baja; ×ball; ×calidad; Veloz (tiro 1 vs 2); Turno (escala);
    Red (Bicho/Agua vs no); Repetición (visto vs no); Master = 1; clamp 0..1.
  - `pisoIV`: Excelente sube los 2 IVs más bajos a 31; otras calidades no tocan.
  - `sincronizaNat`: `synchronize` → nat del compañero; otra hab → null.
  - `fleeProb`: monótona creciente con la rareza, dentro de [0.1, 0.5].
- `node --test web/src/lib/safari-core.test.mjs` verde.
- `cd web && npm run build` verde; `cd api && npx jest` sin regresiones (no se toca el motor).
- Verificación visual (`/frontend-design`): screenshot de la carta de encuentro, el overlay de tiro
  (anillo), el selector de balls y el de compañero — tema oscuro y claro.

## Retro-compat / migración

- Sin migración de datos. `col:companero` ausente = sin Sincronía. Instancias sin `alfa` = no alfa.
- Las balls existentes en inventario siguen sirviendo (ahora vía `catch`). Quien tenía Super/Ultra ya
  no obtiene boost de aparición pero sí mejor captura.
- `derivarCompat`/perfil/logros intactos (la captura sigue llamando la lógica de `atrapar`).

## Fuera de alcance Fase 1 (→ Fase 2/3)

- Encadenado shiny (odds shiny/IV por cadena), biomas/hora del día, **Dusk Ball** (necesita hora),
  alfa más rico (tamaños/marcas múltiples) → **Fase 2**.
- EVs en PvP, reset de EV / bayas → **Fase 3**.
- Feature **Buddy** completa (corazones/perks) — el compañero acá es solo para Sincronía.

## Archivos afectados (estimado)

- `web/src/lib/safari-core.js` (+ `.test.mjs`) — NUEVO, lógica pura + tests.
- `web/src/lib/coleccion.js` — `encontrar`/`capturar`/`companero`/`setCompanero`; `atrapar` extendido.
- `web/src/lib/items.js` — roster de balls + retiro de `BALL_BOOST`.
- `web/src/lib/sprites.js` — variantes `ballSvg`.
- `web/src/pages/safari.astro` — UI de encuentro 2 pasos + selectores.
- `web/src/pages/pokedex.astro` — marca alfa.
- `web/src/pages/tienda.astro` — balls nuevas.
- `web/src/styles/global.css` — estilos de encuentro/tiro/selectores.
- `web/src/pages/ayuda.astro` — documentar el Safari profundo (regla CLAUDE.md).
- `docs/` — rebuild.
