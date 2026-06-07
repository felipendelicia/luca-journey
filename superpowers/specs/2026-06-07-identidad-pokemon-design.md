# Identidad por Pokémon — IVs + Naturalezas + Habilidades + Género + EVs (v1)

**Fecha:** 2026-06-07
**Estado:** diseño aprobado, pendiente plan de implementación.
**Tema:** profundizar lo existente — cada instancia capturada pasa a ser **única**.
Cruza **batalla + safari + pokédex** a la vez. Lo más fiel a la saga; hoy todas las
instancias de una especie al mismo nivel son idénticas.

## Objetivo

Dar identidad individual a cada Pokémon del PC:

1. **IVs** (Individual Values) — 0–31 por stat, **fijos al capturar** (fiel).
2. **Naturaleza** — 25 naturalezas; ×1.1/×0.9 sobre un par de stats (no HP); fija al capturar.
3. **Habilidad** — una de la pool de la especie; **set curado** con efecto real en combate,
   resto como flavor.
4. **Género** — ♂/♀ según ratio de especie; derivado del `iid` (cosmético/flavor v1).
5. **EVs** (Effort Values) — 0–252 por stat, cap 510 total; **se ganan peleando**
   (estado mutable). Único elemento mutable del set; el resto es fijo.

## Decisiones tomadas (brainstorming 2026-06-07)

- **Las 3 capas juntas** (IVs+naturalezas+habilidades), habilidades = subset curado. **+ género + EVs.**
- **IVs fijos al capturar** → derivables del hash del `iid` (cero migración, estables).
- **Tasación en el modal:** GO% + estrellas (header) **y** desglose por-stat + frases de "El Juez".
- **Habilidades v1:** solo combate, pasivas automáticas (no toca safari ni el reto de código).
- **EVs v1:** se ganan **solo en práctica vs CPU** (PvP los otorga en una fase futura → no toca
  premios/anti-trampa del server). Solo suben (reset/bayas = backlog).
- **Vitaminas en la tienda** como ruta rápida de EV (opcional / nice-to-have).

## Arquitectura existente (contexto)

- **Instancia** (`col:pc`, `coleccion.js`): `{iid,id,nivel,exp,shiny,movs,creado}`. Fuente de
  verdad; `col:atrapados`/`col:shiny` se derivan (`derivarCompat`). Ya sincroniza a la nube.
- **Reglas de combate puras:** `web/src/lib/combate-core.ts` = **fuente única**.
  `scripts/sync-batalla-data.mjs` la copia (con header de aviso) a `api/src/batalla/combate-core.ts`
  y copia los JSON de data a `api/src/batalla/data/`. El motor de la API (`motor.ts`) la importa.
  → **Editar el core una vez + agregar data al sync = ambos lados alineados.** Cero doble-impl manual.
- **Stats hoy** (`combate-core.ts`): `estadisticas.json` `{id:[hp,atk,def,spa,spd,spe]}` base Gen 3.
  `statEf(base,nivel)=floor(2·base·nivel/100)+5`; `hpEf(baseHp,nivel)=floor(2·baseHp·nivel/100)+nivel+10`.
  El comentario ya dice *"0 IV/EV, naturaleza neutra"* → diseñado para esta extensión.
- **Inyección de datos:** `DatosCombate` (front `batalla.js`, API `motor.ts`) inyecta los JSON.

## 1. Modelo de datos

Instancia gana 4 campos **opcionales** (escritos al capturar; EVs mutan después):

```js
{
  iid, id, nivel, exp, shiny, movs, creado,
  ivs: [h, a, d, sa, sd, sp],   // 6× 0–31, fijos
  nat: 0..24,                   // índice de naturaleza, fijo
  hab: "espesura",              // key de habilidad (de la pool de la especie), fija
  gen: "m" | "f" | null,        // género (null = sin género), fijo
  evs: [h, a, d, sa, sd, sp]    // 6× 0–252 (cap total 510), MUTABLE
}
```

### Derivación determinista (sin migración)

En `combate-core.ts`:

- `semilla(iid)` — hash estable del `iid` (string → uint32).
- `identidad(inst)` — devuelve `{ivs, nat, hab, gen}`:
  - usa los campos **explícitos si están**;
  - si no, **deriva del hash** (IVs 0–31, nat 0–24, slot de habilidad, género según ratio).
  - **EVs no se derivan** (se ganan): `inst.evs ?? [0,0,0,0,0,0]`.
- Hidden ability: ~5% al capturar (parte del hash).

→ Pokémon **viejos** obtienen identidad estable sin migración ni cambio de schema en nube.
CPU/tests siguen la misma ruta (derivan de su `iid`, ej. `'cpu0'`). Captura **nueva** persiste
los campos explícitos (robusto ante cambios de hash; viajan en trades/perfil).

## 2. Fórmula de stats (Gen 3 fiel, con IV + EV + naturaleza)

```
statEf(base, nivel, iv=0, ev=0, natMult=1) =
    floor( (floor((2·base + iv + floor(ev/4)) · nivel / 100) + 5) · natMult )
hpEf(baseHp, nivel, iv=0, ev=0) =
    floor((2·baseHp + iv + floor(ev/4)) · nivel / 100) + nivel + 10
```

- **Naturaleza:** `natMult` ∈ {1.1, 0.9, 1} por stat (no afecta HP). 25 naturalezas, 5 neutras.
  Tabla estática `NATURALEZAS` en `combate-core.ts` (no requiere PokeAPI): `{nombre, sube, baja}`.
- `combatiente(inst, d)` lee `identidad(inst)` + `inst.evs` y pasa iv/ev/natMult a `statEf`/`hpEf`.
- **Tests:** actualizar los expects de `combate-core.spec.ts` a los nuevos números deterministas
  (las instancias `'cpuX'`/test ahora derivan IVs/nat de su iid).

## 3. Motor de habilidades (Approach A — hooks)

Registro central en `combate-core.ts`:

```ts
HABILIDADES: Record<string, {
  nombre: string;
  desc: string;
  alEntrar?:    (self, rival) => Evento[];        // al entrar a pista
  modDano?:     (dmg, atacante, defensor, mov) => number;  // multiplica daño
  alContacto?:  (self, atacante, mov) => Evento[];         // al recibir físico
  inmuneTipo?:  (tipoMov) => boolean;             // anula daño de un tipo
  noEstado?:    (estado) => boolean;              // bloquea un estado
  modPrecision?:(mult) => number;
}>
```

Los orquestadores (armar combatiente, `calcularDano`, loop de turno, switch-in, aplicar estado)
llaman los hooks si la habilidad activa del combatiente los define. Cada hook devuelve texto para
el cuadro FireRed (ej. *"¡Intimidación de Gyarados! El Ataque de … bajó."*).

### Set curado v1 (~13 — cubre los 6 estados + inmunidades + on-entry + on-contact + low-HP)

| Habilidad | Hook | Efecto |
|---|---|---|
| Intimidación | `alEntrar` | baja Atk del rival 1 escalón |
| Levitación | `inmuneTipo` | inmune a Tierra |
| Robustez (Sturdy) | `modDano` | sobrevive a 1 HP un golpe letal desde full |
| Estática | `alContacto` | 30% paraliza al atacante físico |
| Cuerpo Llama | `alContacto` | 30% quema al atacante físico |
| Espesura/Mar Llamas/Torrente | `modDano` | +50% poder del tipo propio con <⅓ HP (trío inicial) |
| Agallas (Guts) | `modDano` | +50% Atk físico si tiene estado |
| Absorbe Agua | `inmuneTipo` | inmune a Agua (v1: solo anula; cura = backlog) |
| Absorbe Fuego (Flash Fire) | `inmuneTipo` | inmune a Fuego |
| Inmunidad | `noEstado` | no se envenena |
| Insomnio | `noEstado` | no se duerme |
| Armadura Magma / Cuerpo Ígneo | `noEstado` | no se congela |
| Ojo Compuesto | `modPrecision` | +30% precisión |

Resto de habilidades = **flavor**: `meta.efecto:false`, se muestran en pokédex (nombre+desc) sin
efecto en combate. El set crece en fases futuras.

## 4. EVs (entrenamiento por esfuerzo)

- `evs` por instancia (ver §1), mutable, persistido en `col:pc` (sync nube existente).
- **Yields:** `web/src/data/yields.json` `{id:[h,a,d,sa,sd,sp]}` (effort yield de PokeAPI; valores
  chicos 0–3). Generado por `gen-yields.mjs` (o fold en `gen-habilidades.mjs`).
- **Ganancia (v1, solo práctica vs CPU):** al debilitar a un rival, los Pokémon **participantes**
  del jugador ganan el yield de ese rival. Helper `darEV(iid, yields)` en `coleccion.js` (respeta
  cap 252/stat y 510 total). Llamado desde el flujo de `batalla.astro` (modo práctica). **PvP no
  otorga EVs en v1** (evita tocar premios/anti-trampa del server).
- **Vitaminas (tienda, opcional):** Proteína/Hierro/Calcio/Zinc/Carbono/Más-PS → +10 EV (cap 100
  por vía vitamina, estilo Gen 3) al stat respectivo; pagan Pokébolas. Reusa `items.js` + tienda.
- **Fórmula:** ya incluida en §2 (`+ floor(ev/4)`).

## 5. Data + sync

- `web/scripts/gen-habilidades.mjs` → `web/src/data/habilidades.json`:
  - `especies: {id: [{key, hidden}]}` (slots por especie, PokeAPI `/pokemon/{id}` abilities).
  - `meta: {key: {nombre, desc, efecto:boolean}}` (ES de PokeAPI `/ability/{name}`; `efecto:true`
    solo para el set curado).
- `web/scripts/gen-yields.mjs` → `web/src/data/yields.json` (effort yield + ratio de género;
  el género puede salir de `/pokemon-species/{id}` `gender_rate`).
- Naturalezas: tabla estática en `combate-core.ts` (no PokeAPI).
- Agregar `habilidades.json` y `yields.json` a `FILES` en `sync-batalla-data.mjs`.
- `DatosCombate` gana `habilidades` (y `yields` si el motor las necesita; el yield se usa client-side
  para `darEV`, no en el server v1). Inyección en `batalla.js` (front) y `motor.ts` (API).

## 6. Superficies de UI (→ skill `/frontend-design`, tema-aware, estética Pokédex/CRT)

- **Modal Pokédex** (`pokedex.astro`) — panel **"Identidad"**:
  - Header GO: **% IVs** (suma/186 → 0–100%) + **0–4 estrellas** + frase resumen.
  - Desglose por-stat: barra IV 0–31 + valor + frases de "El Juez"
    (*"¡fantástico!" / "notable" / "flojo"*).
  - **EVs:** barra por stat 0–252 (color distinto del IV) + total/510.
  - **Naturaleza:** nombre + stat ↑ (rojo) / ↓ (azul); neutra → "neutra".
  - **Habilidad:** nombre + descripción (las flavor sin badge de efecto).
  - **Género:** símbolo ♂/♀ junto al nombre.
- **Captura (safari):** línea rápida — `✨ ♂ · IVs 87% · Modesta · Espesura`.
- **Batalla HUD:** habilidad bajo el nombre; ♂/♀ junto al nombre; disparos al cuadro FireRed.

## 7. Tests + verificación

- `api/src/batalla/combate-core.spec.ts` (los tests viven en `api/`; jest corre la **copia
  sincronizada** del core — editar `web/src/lib/combate-core.ts`, correr el sync, luego ajustar/
  agregar tests acá):
  - `statEf/hpEf` con iv/ev/naturaleza (números fijos).
  - derivación estable por iid (mismo iid → misma identidad).
  - cada habilidad curada (intimidación baja atk al entrar, levitación inmune a tierra, sturdy a
    1 HP, estática/cuerpo-llama proc al contacto, low-HP boost del trío, guts con estado,
    inmunidades de tipo, no-estado, +precisión).
  - cap de EVs (252/stat, 510 total) en `darEV`.
- `cd api && npm test` verde (motor + core specs) + `npm run build` (web) verde.
- Verificación visual: **screenshot del modal Pokédex** (set de stats coherente, tema oscuro y
  claro) antes de cerrar.

## 8. Retro-compat

- **Sin migración:** identidad fija derivada del `iid`; EVs ausentes = ceros.
- `derivarCompat` / trades / perfil / logros intactos (campos nuevos viajan en la instancia).
- Capturas nuevas persisten campos explícitos; trades los conservan.

## 9. Fuera de alcance v1 (roadmap, cada uno su spec)

- **Habilidades flavor con efecto** (codificar las ~250 restantes; muchas piden clima/terreno).
- **Abilities en safari/captura** (Sincronía fija nature, Estático/Imán boost de spawn, Cuerpo
  Llama acelera huevos — depende de huevos).
- **Clima/terreno** (lluvia/sol/arena + terrenos; habilita Drizzle/Swift Swim/Clorofila…) →
  fase "batalla profunda".
- **Formas regionales** (Alola/Galar/Paldea) → atado al backlog gen 7-9
  ([[backlog-regiones-avanzadas]]).
- **EVs en PvP** (otorgar EVs peleando online), **reset de EVs / bayas**, **cría/huevos**,
  **IVs entrenables**.

## Archivos afectados (estimado)

- `web/src/lib/combate-core.ts` — identidad, fórmula, NATURALEZAS, HABILIDADES, hooks. **(núcleo)**
- `web/src/lib/coleccion.js` — `atrapar` escribe identidad; `darEV`; lectura `identidad`.
- `web/src/lib/batalla.js` — inyección `habilidades`; disparo de hooks en el flujo; `darEV` al ganar.
- `web/src/lib/items.js` + `tienda.astro` — vitaminas (opcional).
- `web/src/pages/pokedex.astro` — panel Identidad.
- `web/src/pages/safari.astro` — línea de identidad al capturar.
- `web/scripts/gen-habilidades.mjs`, `gen-yields.mjs` — data nueva.
- `web/src/data/habilidades.json`, `yields.json` — data.
- `api/scripts/sync-batalla-data.mjs` — agregar los 2 JSON a FILES.
- `api/src/batalla/combate-core.spec.ts` — tests (jest sobre la copia sincronizada; correr sync antes).
- `web/src/pages/ayuda.astro` — documentar identidad/EVs (regla CLAUDE.md).
- `docs/` — rebuild.
