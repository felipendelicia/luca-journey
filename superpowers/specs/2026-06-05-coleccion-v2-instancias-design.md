# Diseño — Colección v2: instancias estilo Pokémon GO (Etapa 1)

Fecha: 2026-06-05
Estado: aprobado (dirección); pendiente review del spec

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).

## Contexto y objetivo

Fundación para el juego de **batallas PvP** (Etapa 2, su propio ciclo). Esta etapa rehace el
modelo de colección al estilo **Pokémon GO**, sin tocar la batalla todavía. Cierra el loop:
**atrapás (safari) → caramelos → subís nivel → evolucionás (por nivel) → [batallás, Etapa 2]**.

Hoy la colección es `col:atrapados = { id: cantidad }` (conteos por especie) + `col:shiny =
[ids]`, y la evolución consume 3 repetidos dejando 1 copia del pre-evo. Problemas que resuelve
esta etapa (pedidos del owner):
1. **Pokédex (vistos) ≠ PC (los que tenés).** Vistos = todo lo que tuviste alguna vez (Pokédex
   completa, no se pierde). PC = inventario real usable. Ej.: tenés un Zubat, evoluciona → en la
   Pokédex quedan **Zubat y Golbat**; en el PC queda **solo 1 Golbat** (el Zubat se consumió).
2. **Instancias GO-style.** El PC es una **bolsa de Pokémon individuales**: podés tener 3
   Pikachus distintos, cada uno con su **nivel** (y en Etapa 2, sus 4 ataques).
3. **Caramelos + nivel + evolución por nivel.** Atrapar repetidos da **caramelos** (por familia
   evolutiva, como GO). Los caramelos **suben el nivel**. Al llegar al **nivel de evolución**
   (de PokeAPI), evolucionás (consume caramelos; la instancia conserva su nivel).

## Decisiones

- **PC = array de instancias.** Una bolsa; se permiten varias de la misma especie.
- **Caramelos por FAMILIA evolutiva** (especie base de la línea), compartidos — GO-style.
- **Vistos = set de especies** alguna vez poseídas (Pokédex completa).
- **Niveles 1–50.** Subir nivel cuesta caramelos (curva creciente). El safari hace crecer al
  Pokémon ya en esta etapa (las batallas darán caramelos en Etapa 2).
- **Evolución por nivel** (cadena + `min_level` de PokeAPI). Cuesta caramelos. Conserva el nivel.
- **Shiny** pasa a ser propiedad de la instancia.
- **Movimientos**: campo de la instancia, **se llena en Etapa 2** (learnsets de PokeAPI). En esta
  etapa la instancia solo tiene `nivel` (placeholder `movs: []`).
- **Capa de compatibilidad** durante la migración: se deriva `col:atrapados`/`col:shiny` desde
  `col:pc` para que el código viejo (intercambios, perfil, logros) siga andando hasta adaptarlo.

## Modelo de datos (localStorage / blob de progreso)

```
col:pc        = [ { iid, id, nivel, exp, shiny, movs:[], creado }, ... ]
                iid   = id de instancia (uuid corto, único)
                id    = especie (id PokeAPI)
                nivel = 1..50
                movs  = []  (se llena en Etapa 2)
col:caramelos = { familiaBaseId: cantidad }     // por familia evolutiva
col:vistos    = [ especieId, ... ]              // Pokédex completa (nunca se quita)
```

Claves viejas (`col:atrapados`, `col:shiny`) quedan **derivadas** (no fuente de verdad):
`col:atrapados[id]` = nº de instancias de esa especie en el PC; `col:shiny` = especies con al
menos una instancia shiny. Se recalculan al mutar el PC, para no romper consumidores actuales.

## Datos (PokeAPI, scripts gen-*)

- **`evoluciones.json` enriquecido** (regenerar con `gen-evoluciones.mjs`):
  ```
  { "<id>": { evos: [ { a:<evoId>, nivel:<min_level|null> } ], familia:<baseId> } }
  ```
  `familia` = id base de la cadena (para agrupar caramelos). `nivel` = `min_level` del trigger
  `level-up` (si la evo no es por nivel —piedra, intercambio, amistad— se mapea a un **nivel
  equivalente** configurable, ej. 30, para mantener todo "por nivel" en esta app). Documentar el
  fallback en el script.
- Tipos / learnsets / stats: **NO** en esta etapa (son de la batalla, Etapa 2).

## Componentes / archivos

| Archivo | Cambio |
|---|---|
| `web/src/lib/coleccion.js` | Modelo v2: `pc()`, `caramelos()`, `vistos()`, `atrapar(id,{shiny})` (crea instancia + vistos + caramelos), `subirNivel(iid)`, `evolucionar(iid)` (por nivel + caramelos), `derivarCompat()` (recalcula `col:atrapados`/`col:shiny`). Reemplaza la evolución por-3-repes. |
| `web/src/lib/migracion-pc.js` | NUEVO. Migración one-time: `col:atrapados`+`col:shiny` → `col:pc`/`col:vistos`/`col:caramelos`. Idempotente (flag `col:pc:migrado`). |
| `web/scripts/gen-evoluciones.mjs` | agrega `nivel` (min_level) + `familia` (especie base). |
| `web/src/pages/safari.astro` | la captura crea una **instancia** + muestra caramelos ganados; usa `atrapar()`. |
| `web/src/pages/pokedex.astro` | dos vistas: **Pokédex (vistos)** = completitud por especie; **PC** = tus instancias (por especie: cuántas, niveles) con **Power-Up** (caramelos→nivel) y **Evolucionar** (al nivel). |
| `web/src/lib/coleccion.js` (swap) | la lógica de captura por hitos (`sincronizar`) crea instancias en vez de incrementar conteos. |

**Diseño por unidades:** `coleccion.js` v2 expone una API chica y testeable (pc/caramelos/
vistos/atrapar/subirNivel/evolucionar) sin DOM. La migración vive aislada en `migracion-pc.js`.
La UI (safari/pokedex) solo consume esa API.

## Sub-etapas (orden de build)

- **1a — Modelo + safari + pokédex + evolución + migración + compat.** Shippable: el juego
  anda con instancias/niveles/caramelos, trades siguen funcionando vía la capa de compat
  (operan sobre el `col:atrapados` derivado).
- **1b — Intercambios por instancia.** Adaptar trades en vivo y ofertas async para mover
  **instancias** (con su nivel/shiny) en vez de "especie + cantidad". Toca el cliente
  (`trades.js`/`social.js` + UI de `intercambio.astro`/`amigos.astro`) **y el servidor** (el
  swap atómico en `api/src/intercambios/ofertas`): hoy manipula `col:atrapados`/`col:shiny`;
  pasa a mover objetos de `col:pc`. Es la parte más pesada; se hace después de 1a.

## Migración (1a, one-time, cliente)

En el boot, si no hay `col:pc:migrado`:
1. Por cada `col:atrapados[id] = n`: crear **n instancias** de esa especie (nivel 1, `movs:[]`);
   si `id ∈ col:shiny`, marcar **1** de esas instancias `shiny:true`.
2. `col:vistos` = claves de `col:atrapados` ∪ ids en `col:shiny`.
3. `col:caramelos` = 0 por familia (los repes ya quedaron como instancias; no se "queman" en
   caramelos al migrar para no sorprender al usuario). El owner puede sembrar caramelos a mano si
   quiere (one-off en el progreso).
4. `derivarCompat()` y marcar `col:pc:migrado = 1`.

Corre client-side; el progreso se sube a la nube como siempre (write-through). Aplica a los
usuarios reales (felipo/lucario/natalu) en su primer boot tras el deploy.

## Reglas de juego (esta etapa)

Constantes (configurables en `coleccion.js`):

- **Atrapar** (safari): nueva instancia nivel 1 + especie a vistos + **+3 caramelos** a la familia.
  Shiny por el roll actual (1%).
- **Power-Up** (L → L+1): cuesta **`1 + Math.floor(L/8)`** caramelos de la familia (1 hasta nivel
  8, 2 hasta 16, …). Sube `nivel` de la instancia. Cap nivel **50**.
- **Evolucionar** una instancia: requiere `nivel ≥ nivel_evo` (de PokeAPI) **+ 25 caramelos** de
  la familia. Cambia `id` al evo, **conserva el nivel**, agrega el pre-evo a **vistos**. No deja
  copia del pre-evo en el PC (fix del comportamiento actual).

## Testing

- **Unit** (node, como `rareza`): `migracion-pc` (atrapados+shiny → pc/vistos correctos);
  `evolucionar` (sube de especie, conserva nivel, pre-evo a vistos, no deja copia); `subirNivel`
  (gasta caramelos, respeta cap); `derivarCompat` (pc → atrapados/shiny equivalentes).
- **Manual/visual**: safari (captura crea instancia + caramelos), pokédex (vistos vs PC,
  power-up, evolucionar), y que **intercambios sigan andando** vía compat (1a).

## Fuera de alcance (Etapa 2) — registrado para no perderlo

- Batalla PvP en vivo, equipos de 3, combate por turnos, recompensas (ganador: caramelos de los
  que pelearon; perdedor: Pokébolas).
- Tipos, stats de combate (HP/CP por nivel), el **súper por código** (formatos fáciles a/b/c/d
  escalados al nivel del jugador).
- **Modelo de movimientos** (confirmado con el owner): cada instancia tiene un **pool de
  desbloqueados** = ataques del learnset (PokeAPI) con `nivel_aprende ≤ instancia.nivel`; el
  usuario elige **4 activos** de ese pool y **puede recambiarlos cuando quiera** (no se "olvidan",
  GBA-relajado). El campo `instancia.movs` (ya en el schema v2) guarda los 4 activos; el pool se
  deriva de nivel + learnset. Datos nuevos en Etapa 2: `learnsets.json` (moves por nivel/especie)
  y `movimientos.json` (tipo/poder/efecto de cada move).
- (En 1b —parte de esta etapa— sí entra adaptar los intercambios a instancias.)
