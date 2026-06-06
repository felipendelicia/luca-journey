# Diseño — Tienda de items

Fecha: 2026-06-06
Estado: alcance definido con el owner (3 rondas de preguntas); pendiente review al despertar.

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).
> Sub-proyecto 1 de 2 (el otro: `2026-06-06-pvp-en-vivo-design.md`). Se construye PRIMERO (100% shippable).

## Objetivo

Una **Tienda** donde el jugador gasta **Pokébolas** en items que profundizan los sistemas que ya
existen (evolución, safari, batalla). Cierra economía: ejercicios/regalo/batallas → Pokébolas → items.

## Decisiones (del owner)

- **Moneda: solo Pokébolas** (`col:balls`). Una sola moneda, sin agregar otra.
- **Items que vende:** Piedras de evolución · Pociones · mejores Pokéballs (Super/Ultra).
- **Evolución por piedra:** los Pokémon que evolucionan por piedra (los `nivel:0` del learnset/evo,
  ej. Eevee, Pikachu, Vulpix) ahora **REQUIEREN una Piedra Evolutiva** (comprada) **+ caramelos**.
  Cambia el comportamiento actual (hoy esos evos son solo caramelos).
- **Mejores Pokéballs: automáticas** — el safari usa la mejor ball que tengas en stock; cuando se
  acaban, vuelve a la normal. Suben (todas a la vez, escaladas por tier): **shiny, nivel del salvaje,
  rareza y caramelos**.
- **Pociones:** se usan **en batalla** (práctica y PvP), desde una **Mochila**; **usar una cuesta el
  turno** (el rival ataca). Límite razonable por combate.
- **Inventario en la nube:** `col:items` va en el blob de progreso (write-through como todo).

## Items (definición; precios/magnitudes = default, el owner puede tunear)

| id | nombre | ico | precio (🔴) | efecto |
|---|---|---|---|---|
| `piedra` | Piedra Evolutiva | 🪨 | 80 | Habilita evolucionar a los Pokémon que evolucionan por piedra (genérica: sirve para cualquiera). Se consume 1 al evolucionar. |
| `pocion` | Poción | 🧪 | 15 | Cura 30 HP en batalla. |
| `superpocion` | Súper Poción | ⚗️ | 35 | Cura 70 HP. |
| `pocionmax` | Poción Máxima | 💉 | 70 | Cura todo el HP. |
| `superball` | Super Ball | 🔵 | 25 | Mejora moderada de captura (ver abajo). |
| `ultraball` | Ultra Ball | 🟡 | 60 | Mejora fuerte de captura. |

**Mejores Pokéballs — efecto (multiplicadores, default):**

| | shiny | nivel salvaje | rareza (peso↓ de raros) | caramelos |
|---|---|---|---|---|
| Pokéball normal | ×1 (1%) | normal | normal | +3 |
| Super Ball | ×2 (2%) | +20% sobre el mínimo | ×1.4 chance de raro | +5 |
| Ultra Ball | ×4 (4%) | +45% | ×2 chance de raro | +8 |

(Implementación: `tirar()` recibe el tier de ball usado y ajusta `PROB_SHINY`, el `nivelWild`, el
peso de `elegirPonderado` hacia lo raro, y los caramelos. La ball se consume 1 por tiro.)

## Componentes / archivos

| Archivo | Responsabilidad |
|---|---|
| `web/src/lib/items.js` | NUEVO. `ITEMS` (catálogo) + helpers puros de inventario. |
| `web/src/lib/coleccion.js` | `items()`, `comprarItem(id)`, `usarItem(id)`, `tieneItem(id)`, `darItem(id,n)`; integrar piedra en `opcionesEvo`/`evolucionarInst`; `tirar()` toma el tier de ball + lo consume. |
| `web/src/pages/tienda.astro` | NUEVO. UI de la tienda (categorías, precio, comprar, tu saldo de Pokébolas + inventario). |
| `web/src/pages/safari.astro` | usa la mejor ball automáticamente; muestra qué ball usó; el badge de stock. |
| `web/src/pages/pokedex.astro` | en el modal, los evo-por-piedra piden Piedra Evolutiva (botón claro + link a la tienda si no tenés). |
| `web/src/pages/batalla.astro` | botón **🎒 Mochila** → usar Poción (cura el activo, cuesta turno). |
| `web/src/layouts/Base.astro` | acceso a la tienda (botón en el hero de safari/pokédex; o item de nav). |

**Diseño por unidades:** `items.js` = catálogo + inventario puro (testeable en node). `coleccion.js`
expone la economía (comprar/usar/dar). La UI sólo consume esa API. El diseño visual de `/tienda`
se hace con `/frontend-design` (cohesivo con el Device OS / estética retro-Pokédex; tema-aware).

## Reglas

- **Comprar:** `comprarItem(id)` → si `balls >= precio`, descuenta y suma 1 al inventario. Stock infinito.
- **Evolución por piedra:** en `opcionesEvo`, una opción con `nivel===0` es `ok` sólo si además
  `tieneItem('piedra')`. `evolucionarInst` consume la piedra (+ los caramelos). Si no tenés piedra,
  el modal muestra "🪨 Necesitás una Piedra Evolutiva (Tienda)".
- **Mejores balls (safari):** al tirar, se elige la mejor ball del inventario (ultra > super > normal),
  se consume 1, y se aplican sus boosts. La normal es infinita (las que ya ganás).
- **Pociones (batalla):** Mochila lista tus pociones; usar una cura el activo y **gasta el turno**
  (el rival ataca). Límite: **2 usos de items por combate** (default).

## Migración / compat

- `col:items` arranca `{}` (nadie tiene items). Sin migración. Los evo-por-piedra que antes se podían
  hacer con caramelos ahora piden piedra → es un cambio de regla, no rompe datos.

## Testing

- **Unit (node):** `items.js` (catálogo), `comprarItem` (descuenta/suma, falla sin saldo),
  `usarItem`/`tieneItem`, evolución por piedra (requiere y consume piedra), `tirar()` con ball tier
  (consume + aplica boosts).
- **Visual (CDP):** /tienda (comprar, saldo baja, inventario sube) en oscuro/claro; safari usando
  Ultra Ball; modal de pokédex pidiendo piedra; mochila en batalla curando.

## Fuera de alcance

- Caramelo Raro (el owner no lo eligió). MO/TM/vitaminas. Stock limitado / ofertas diarias.
- Piedras específicas por tipo (Fuego/Agua/…): por ahora **una piedra genérica** sirve para todos.
