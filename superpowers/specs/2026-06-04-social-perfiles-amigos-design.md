# Diseño — Aspecto social: perfiles, amigos e intercambios asíncronos

Fecha: 2026-06-04
Estado: aprobado

> Ubicación: `superpowers/` (raíz), NO `docs/` (output del build, se limpia en cada `npm run build`).

## Objetivo

Pasar el juego de single-player a social, en 3 etapas que se construyen una sobre otra:
1. **Perfiles + identidad** — handle único `@usuario` + código de amigo; página pública
   compartible (`/u?h=<handle>`) sin login.
2. **Amigos + búsqueda** — solicitud → aceptar (mutuo), bandeja, lista, buscar usuarios.
3. **Intercambios asíncronos** — proponer un trade a un amigo (doy X ↔ pido Y) sin estar
   los dos conectados; el otro acepta/rechaza cuando entra.

Hoy lo único social es el intercambio en vivo. `progreso` es privado por usuario (RLS).

## Decisiones (brainstorming)
- Identidad: **handle único** `@usuario` (URL pública + búsqueda) **+ código de amigo** (alta rápida).
- Amistad: **solicitud + aceptar** (mutuo).
- Perfil público muestra: medallas/títulos, conteos, **Pokédex completa**, logros.
- Async: **oferta directa** (doy X ↔ pido Y); el otro solo acepta/rechaza.
- Defaults: async **solo entre amigos**; **sin lock** de ofrecidos (validar al aceptar);
  avisos **in-app**; perfil **opt-in** (sin @ no estás en lo social), buscable por cualquiera.

## Arquitectura
- Sitio estático (GitHub Pages) + Supabase (Postgres + Auth + Realtime).
- `progreso` sigue **privado**. La data mostrable vive en un **snapshot público** en la
  tabla `perfiles`, que la app mantiene al día (igual que `nube.js` sincroniza el progreso).
- La página pública es **client-rendered**: una ruta estática `/u` lee `?h=<handle>` y
  baja el perfil por handle con la anon key (policy de select público). No requiere login.
- Las mutaciones sensibles (aceptar amistad, ejecutar oferta) van por **RPCs `security
  definer`**, como el sistema de intercambio actual.

## Modelo de datos (migración nueva)

### `perfiles`
`user_id uuid PK → auth.users`, `handle text unique` (regex `^[a-z0-9_]{3,20}$`),
`nombre text`, `avatar int`, `codigo_amigo text unique`, `publico jsonb` (snapshot:
`{ atrapados, shiny, conteos:{unicos,total,shinies,ejercicios}, medallas, titulos, logros }`),
`actualizado timestamptz`.
- RLS: **select público** (`using (true)`); insert/update **solo el dueño** (`auth.uid() = user_id`).

### `amistades`
`id uuid PK`, `de_id uuid`, `a_id uuid`, `estado text` (`pendiente`|`aceptada`),
`creado timestamptz`. Único `(de_id, a_id)`.
- RLS: select si `auth.uid() in (de_id, a_id)`; el resto por RPC.

### `ofertas` (async)
`id uuid PK`, `de_id uuid`, `a_id uuid`, `doy jsonb` (`[{id,shiny}]`, lo que da `de_id`),
`pido jsonb` (lo que da `a_id`), `estado text` (`pendiente`|`aceptada`|`rechazada`|`cancelada`),
`creado`, `resuelto`.
- RLS: select si `auth.uid() in (de_id, a_id)`; el resto por RPC.
- `replica identity full` + publicación realtime (para que el inbox se actualice en vivo).

## RPCs (`security definer`)
- `guardar_perfil(p_handle, p_nombre, p_avatar, p_publico)` — upsert del perfil propio;
  valida formato/unicidad del handle; genera `codigo_amigo` si falta. Devuelve el perfil.
- `buscar_perfiles(q text)` — público; `ilike` sobre handle/nombre; devuelve
  `{handle, nombre, avatar}` (máx 20). No expone el snapshot completo en la búsqueda.
- `solicitar_amistad(p_handle text, p_codigo text)` — crea `amistades` pendiente hacia el
  usuario resuelto por handle **o** código. Idempotente; si ya hay relación, no duplica.
- `responder_amistad(p_id uuid, p_aceptar bool)` — solo `a_id`; aceptar → `aceptada`,
  rechazar → borra la fila.
- `quitar_amigo(p_id uuid)` — participante borra la amistad.
- `crear_oferta(p_a_id uuid, p_doy jsonb, p_pido jsonb)` — solo si son **amigos**; crea
  oferta pendiente.
- `responder_oferta(p_id uuid, p_aceptar bool)` — solo `a_id`. Aceptar **valida y ejecuta**
  el swap sobre `progreso` de ambos (misma lógica que `ejecutar_intercambio`: valida
  cantidades/shiny, mueve, marca `aceptada`). Si falla la validación → error claro, queda
  pendiente. Rechazar → `rechazada`.
- `cancelar_oferta(p_id uuid)` — solo `de_id`, si está `pendiente`.

El swap async reutiliza los helpers `_mapa_inc/_mapa_dec/_arr_add/_arr_del` ya existentes.
La ejecución lee/escribe `progreso` (autoritativo), no el snapshot público. Tras ejecutar,
ambos snapshots `publico` se re-sincronizan desde el cliente al próximo load (o el RPC
los refresca).

## Cliente

### `web/src/lib/social.js` (nuevo)
API sobre Supabase: `miPerfil()`, `guardarPerfil()`, `perfilPublico(handle)`,
`buscar(q)`, `solicitar()`, `responder()`, `quitar()`, `amigos()`, `solicitudes()`,
`crearOferta()`, `responderOferta()`, `cancelarOferta()`, `ofertas()`, y
`snapshotPublico()` (arma el blob `publico` desde el estado local + logros + medallas).

### `web/src/lib/nube.js` (modificar)
Tras subir el progreso, **también** actualizar `perfiles.publico` (mismo trigger de cambio)
para que el snapshot público no quede viejo. Reutiliza el watcher existente.

### Páginas
- **`web/src/pages/liga.astro` (modificar)** — hub del usuario: setear/editar `@`, nombre,
  avatar; mostrar `codigo_amigo` + botón copiar link a `/u?h=<handle>`; CTA a `/amigos`.
- **`web/src/pages/u.astro` (nuevo)** — perfil público read-only (`?h=<handle>`): tarjeta,
  medallas/títulos, conteos, Pokédex, logros. Botones según sesión: **Agregar amigo**
  (si logueado y no sos vos), **Proponer intercambio** (si son amigos), **Copiar link**.
- **`web/src/pages/amigos.astro` (nuevo)** — buscar usuarios; solicitudes entrantes
  (aceptar/rechazar); lista de amigos (link a perfil, proponer intercambio); **ofertas**
  entrantes/salientes (aceptar/rechazar/cancelar). Badge de pendientes.
- **Nav (`Base.astro`)** — entrada "Amigos" (con badge de pendientes).

### Componente de oferta
Reutiliza el picker del intercambio: elegir `doy` de tu colección, `pido` de la Pokédex
pública del amigo. Mismo shape `{id, shiny}`.

## Bordes / privacidad
- Sin `@` no hay perfil → no aparecés en búsqueda ni tenés link (opt-in).
- El snapshot público expone Pokédex y conteos a cualquiera con el link/handle: es la
  intención (opción "perfil público"). `progreso` crudo (claves `ej:*`) **no** se expone.
- Async sin lock: doble oferta posible; gana el primero que acepta; el resto falla con
  aviso "ya no tiene los Pokémon".
- Handle: minúsculas/números/`_`, 3–20; único; inmutable-ish (se puede cambiar, libera el viejo).
- Realtime en `ofertas` para inbox en vivo; amistades se releen al entrar a `/amigos`.

## Verificación
- No hay runner JS. Verificación: `npm run build` + screenshots (perfil público, amigos) +
  prueba manual de **dos sesiones** (solicitar/aceptar amistad, proponer/aceptar oferta).
- La migración se aplica con `supabase db push --yes` (CLI linkeada, ref `cvknrqphepwzpdqdyegv`).

## Despliegue
`npm run build` regenera `docs/`. Commitear `web/` + `docs/` + `supabase/migrations/`.
Migración aparte en Supabase.
