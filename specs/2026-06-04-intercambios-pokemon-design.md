# Diseño — Intercambios (trades) de Pokémon

**Fecha:** 2026-06-04
**Estado:** aprobado (pendiente de plan de implementación)

## Contexto

Plataforma "Python con Pokémon": app Astro estática en GitHub Pages + Supabase para
persistencia. La colección de Pokémon de cada usuario vive en `localStorage` y se
sincroniza a Supabase (tabla `progreso`, un blob `jsonb` por usuario, RLS solo-tu-fila,
login magic-link). Modelo de sync: al iniciar sesión, la cuenta manda (importa la nube;
si es nueva, la siembra con lo local).

**Objetivo:** permitir que dos usuarios intercambien Pokémon de sus colecciones, en vivo.

## Decisiones (del brainstorming)

- **Audiencia:** círculo privado (hermano + amigos). Coordinan por fuera (WhatsApp).
  → sin tablón público, sin usernames, sin moderación.
- **Modelo:** sala **en vivo** (Supabase Realtime), ambos online al mismo tiempo. Estilo
  "cuarto de intercambio" del juego.
- **Unidad:** **lote** — cada lado pone varios Pokémon; se intercambia el lote completo
  (permite 2×1, etc.). Shiny cuenta como distinto.
- **Qué se puede ofrecer:** **cualquiera**, incluso el único ejemplar (con aviso de que
  desaparece de la Pokédex si das el último).
- **Arquitectura:** estado de la sala en una fila de la base; Realtime empuja los cambios;
  el swap lo hace una función Postgres `SECURITY DEFINER` (atómica, server-validada).

## Modelo de datos

### Tabla `intercambios`

| Columna | Tipo | Notas |
|---|---|---|
| `id` | uuid PK (`gen_random_uuid()`) | id de la sala |
| `codigo` | text único | código corto para unirse (6–7 chars, aleatorio) |
| `creador_id` | uuid → auth.users (cascade) | A |
| `invitado_id` | uuid → auth.users (cascade), null | B (se setea al unirse) |
| `creador_nombre` / `invitado_nombre` | text | nombre de entrenador (de `liga:nombre`) para mostrar |
| `creador_lote` / `invitado_lote` | jsonb, default `[]` | lista `[{id:int, shiny:bool}]` |
| `creador_ok` / `invitado_ok` | bool, default false | confirmación de cada lado |
| `estado` | text, default `'abierta'` | `abierta` · `completada` · `cancelada` |
| `creado` / `actualizado` | timestamptz | |

### RLS

- **SELECT:** permitido si `auth.uid() in (creador_id, invitado_id)`. (Realtime respeta RLS,
  así que ambos participantes reciben los `postgres_changes` de su fila.)
- **Sin** INSERT/UPDATE/DELETE directos. Toda mutación pasa por RPCs (ver abajo).

### Realtime

- Habilitar la tabla `intercambios` en la publicación de Realtime.
- Cada cliente se suscribe a `postgres_changes` filtrando por `id = <sala>`.

## Funciones del servidor (RPC `SECURITY DEFINER`)

Todas chequean `auth.uid()` para saber qué lado es el que llama. Las escrituras van solo
por acá → control a nivel de **columna** (cada uno solo toca su lado), que la RLS sola no da.

- `crear_intercambio(mi_nombre text) → {id, codigo}`
  Inserta sala con `creador_id = auth.uid()`, `creador_nombre = mi_nombre`, `codigo` aleatorio.

- `unirse(codigo text, mi_nombre text) → {id}`
  Si existe sala con ese `codigo`, `estado='abierta'`, `invitado_id is null` y el que llama
  no es el creador → setea `invitado_id = auth.uid()`, `invitado_nombre`. Si no, error.

- `poner_lote(id uuid, lote jsonb)`
  Si el que llama es participante → guarda el lote en SU columna (`creador_lote` o
  `invitado_lote`) y **resetea ambos OK** (`creador_ok = false`, `invitado_ok = false`).
  (Cualquier cambio invalida confirmaciones → evita el cambiazo.)

- `confirmar(id uuid)`
  Marca el OK del que llama. Si quedaron ambos OK → llama internamente a `ejecutar_intercambio(id)`.

- `cancelar(id uuid)`
  Si participante y `estado='abierta'` → `estado='cancelada'`.

- `ejecutar_intercambio(id uuid)` (privada / interna)
  El swap atómico (ver abajo).

## El swap atómico — `ejecutar_intercambio`

1. `SELECT ... FOR UPDATE` de la fila; chequear `estado='abierta'` y `creador_ok AND invitado_ok`.
2. Cargar las dos filas `progreso.estado` (creador + invitado).
   La colección vive como **strings** dentro del jsonb:
   `estado->>'col:atrapados'` = `'{"6":2}'`, `estado->>'col:shiny'` = `'[6]'`.
   Parsear esos strings a jsonb.
3. **Validar** cada lote contra la colección real de su dueño:
   - Para cada `{id, shiny}` del `creador_lote`: el creador debe tener `atrapados[id] >=`
     (cantidad de ese id en su lote); si `shiny`, `id ∈ shiny`.
   - Ídem `invitado_lote` contra el invitado.
   - Si algo falla → `raise exception` → aborta la transacción (sin swap parcial).
4. **Aplicar** sobre las colecciones parseadas:
   - Creador: por cada item de `creador_lote` → `atrapados[id] -= 1` (borrar la clave si llega
     a 0); si `shiny` → sacar `id` del set `col:shiny`. Sumar cada item de `invitado_lote` →
     `atrapados[id] += 1`; si `shiny` → agregar `id` al set.
   - Invitado: inverso.
5. Re-stringificar `col:atrapados` y `col:shiny` y guardarlos de vuelta en ambos
   `progreso.estado` (con `jsonb_set`).
6. `estado='completada'`, `actualizado=now()`.
7. Todo en una transacción (la función es atómica) → o pasa todo, o nada. **One-shot**: el
   guard `estado='abierta'` evita replay / doble ejecución.

### Detalle del shiny

El modelo guarda shiny como **presencia** (`col:shiny` = set de especies; no cuenta cuántos).
- Dar un item `shiny:true` → sacar la especie del set (se asume que diste tu shiny) + bajar
  conteo 1.
- Dar un item `shiny:false` → no tocar el set; solo bajar conteo.
- Recibir `shiny:true` → agregar especie al set (idempotente) + subir 1.
Si alguien tenía 2 shinies de la misma especie, es aproximado (el modelo no lo distingue).
Aceptable para v1.

## Cliente — página `/intercambio`

**Requiere sesión.** Sin login → "Iniciá sesión para intercambiar" + abre el modal de login.

### Estados

1. **Inicio** (logueado, sin sala): **Crear sala** | **Unirse con código** (input).
   Si la URL trae `?codigo=XXXX` → se une solo.
2. **Esperando** (creaste): muestra `codigo` + botón copiar link (`…/intercambio?codigo=XXXX`)
   + "esperando al otro…". Suscripto por Realtime.
3. **Sala activa** (los dos dentro): dos paneles (Vos / el otro).
   - **Tu panel:** "Elegir Pokémon" abre tu colección (grid de los que tenés, leídos de
     `col:atrapados`/`col:shiny`). Tocás uno → suma al lote; toggle ✨ si tenés el shiny;
     podés sumar hasta tu cantidad. → `poner_lote`.
   - **Panel del otro:** su lote en vivo (Realtime).
   - Estado de confirmación por lado. Botón **Confirmar** → `confirmar`. Cualquier cambio de
     lote (de cualquiera) resetea ambos OK.
   - Botón **Cancelar** → `cancelar`.
   - **Presencia** (mínima): 🟢/🔴 del otro vía Realtime presence en el canal.
4. **Completado:** al llegar el evento `estado='completada'` → "🎉 ¡Intercambio listo!",
   resumen "diste X · recibiste Y", y refresco de la colección desde la nube.

### Refresco — `nube.js`

Nuevo `refrescarDesdeNube()`: baja `progreso.estado`, lo aplica a `localStorage`, setea
`_ultima` (para que el watcher no re-suba lo viejo) y re-renderiza. Se llama al completarse
el intercambio (la nube ya cambió por el swap del server).

### Acceso

Botón **"🔄 Intercambiar"** en la Pokédex. La nav (6 ítems) no se toca.

## Seguridad / anti-trampa

- Escrituras solo por RPC → control por columna (cada uno solo su lado).
- RLS SELECT solo participantes; Realtime la respeta.
- `codigo` aleatorio difícil de adivinar (la sala solo expone Pokémon, nada sensible).
- El swap valida contra las filas **reales** de `progreso` (no podés dar lo que no tenés) y es
  atómico + one-shot (no duplica, no replay).
- **Caveat aceptado:** como el usuario puede falsear su propia colección (localStorage→sync),
  podría fabricar un Pokémon y comerciarlo. Para círculo privado, aceptado (decisión previa:
  no se hace corrección server-side de la colección).

## Casos límite

- B nunca se une → A espera o cancela.
- Alguien se va a mitad → presencia 🔴; el otro cancela.
- Validación falla al ejecutar (la colección cambió justo) → error claro, sin swap.
- Ambos confirman a la vez → lock + guard `estado='abierta'` → se ejecuta una sola vez.
- Reconexión → el estado vive en la fila; se relee y sigue.
- No logueado → no entra a la sala.
- Lote vacío de un lado = regalo (permitido).

## Alcance v1 (YAGNI)

NO se hace: tablón público, usernames, chat, historial de intercambios, auto-expiración de
salas (solo cancelar manual), validación de "valor" del lote (cualquier lote por cualquiera).

## Archivos que se tocan

- **Supabase:** migración nueva (`intercambios` + RLS + RPCs) → `supabase db push`; habilitar
  Realtime en la tabla.
- **Nuevo** `web/src/lib/trades.js` — wrapper de RPCs + suscripción Realtime + presencia.
- `web/src/lib/nube.js` — agregar `refrescarDesdeNube()`.
- **Nuevo** `web/src/pages/intercambio.astro` — la sala.
- `web/src/pages/pokedex.astro` — botón "🔄 Intercambiar".
- `web/src/styles/global.css` — estilos de la sala/picker.
