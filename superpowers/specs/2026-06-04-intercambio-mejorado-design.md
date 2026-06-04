# Diseño — Intercambio mejorado (ver colección, pedir, quitar del lote)

Fecha: 2026-06-04
Estado: aprobado · implementado

> Ubicación: `superpowers/` (raíz), NO `docs/` — `docs/` es el output del build de Astro y
> se regenera/limpia en cada `npm run build`.

## Problema

El flow de intercambio actual (`web/src/pages/intercambio.astro` + `web/src/lib/trades.js`
+ `supabase/migrations/20260604120000_intercambios.sql`) tiene tres dolores:

1. **No ves la colección del compañero.** Solo ves lo que pone en su lote.
2. **No se puede pedir.** No hay forma de que el otro te solicite Pokémon específicos.
3. **No se puede quitar del lote.** El selector solo agrega (`miLote.push`).

## Decisiones (del brainstorming)

- **Colección visible:** ambos ven la colección completa del otro **con cantidades** y
  shinies, mientras el trade está abierto (privacidad acotada a los dos participantes de un
  trade `abierta`).
- **Pedidos:** cada uno marca "deseados" desde la colección del otro = su **pedido**.
- **Consentimiento:** el dueño **acepta cada pedido**; al aceptar, ese Pokémon entra a su
  lote. Puede no aceptar; el que pide controla su propia wishlist.
- **Layout A — "Mesa arriba":** el trato (das ⇄ recibís) siempre visible arriba; "te
  piden" en el medio; colección del otro abajo (expandible + buscador).

## Modelo de datos

Tabla `public.intercambios` — dos columnas nuevas:

| Columna | Tipo | Significado |
|---|---|---|
| `creador_pedido`  | `jsonb` default `[]` | qué quiere el creador DEL invitado: `[{id:int, shiny:bool}]` |
| `invitado_pedido` | `jsonb` default `[]` | qué quiere el invitado DEL creador |

`*_lote` (existente) = lo que cada uno **da**. `*_pedido` (nuevo) = lo que cada uno
**quiere del otro**. La tabla ya tiene `replica identity full` y está en la publicación
`supabase_realtime`, así que las columnas nuevas viajan por el canal existente.

## RPCs (`supabase/migrations/20260604130000_intercambios_pedidos.sql`)

### `coleccion_del_otro(p_id uuid) returns jsonb` — `SECURITY DEFINER`
Devuelve `{ "atrapados": {<id>:<cant>}, "shiny": [<id>...] }` del **otro** participante.
- Si `auth.uid()` no es participante de `p_id` → excepción.
- Si el trade no está `abierta` → excepción.
- Lee de `progreso.estado` respetando que los valores se guardan como **string JSON**
  (igual que `ejecutar_intercambio`: `(estado->>'col:atrapados')::jsonb`).

### `poner_pedido(p_id uuid, p_pedido jsonb) returns void` — `SECURITY DEFINER`
Setea el pedido del que llama. **No** resetea `creador_ok`/`invitado_ok` (el pedido no
mueve bienes hasta que el dueño acepta).

### Sin cambios
`poner_lote`, `confirmar`, `ejecutar_intercambio`, `crear_intercambio`, `unirse`,
`cancelar`. **Aceptar un pedido** y **quitar del lote** se resuelven en el cliente:
recomputa `miLote` y llama `poner_lote` (que ya resetea confirmaciones).

## Cliente

### `web/src/lib/trades.js`
- `coleccionOtro(id)` → `rpc('coleccion_del_otro', { p_id })`
- `ponerPedido(id, pedido)` → `rpc('poner_pedido', { p_id, p_pedido })`

### `web/src/pages/intercambio.astro` — sala Layout A
Estado nuevo: `miPedido`, `otroColeccion` (cache), `ocultos` (Set local). Secciones:
1. Header — nombres, presencia, estado de confirmación.
2. El trato — `Vos das` = `miLote` (chips con ✕ → `ponerLote`); `Recibís` = lote del otro.
3. Te piden (N) — desde el `*_pedido` del otro; fila con **Aceptar** (suma a `miLote`) / ✕.
4. Colección de [otro] — grid desde `coleccionOtro`: `xN`, ✨ si tiene shiny, ❤ para pedir
   (`ponerPedido`). Buscador + expandible (abierto si `miLote` vacío).
5. Footer — Confirmar / Cancelar.

La colección del otro se baja una vez cuando el otro está presente (no cambia durante un
trade abierto).

## Bordes
- **Shiny:** `{id, shiny:true}`; `ejecutar_intercambio` ya valida disponibilidad.
- **Cantidades:** no se puede pedir/ofrecer más que el conteo del dueño.
- **Rechazar:** no existe borrado del deseo ajeno; ✕ del dueño oculta la fila localmente.
- **Reset de oks:** solo cambios de lote; el pedido no.

## Verificación
- No hay runner JS (los tests son ejercicios Python en Pyodide). Verificación: `npm run
  build` + screenshot del layout + prueba manual de **dos sesiones** logueadas.
- La migración se aplica con `supabase db push --yes` (CLI linkeada).

## Estado
Implementado en `main` el 2026-06-04. Migración aplicada al remoto. Pendiente: prueba real
de dos sesiones.
