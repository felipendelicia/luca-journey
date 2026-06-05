# Diseño — Nube como única fuente de verdad (login obligatorio)

Fecha: 2026-06-04
Estado: aprobado

> Ubicación `superpowers/` (raíz), NO `docs/` (el build limpia `docs/`).

## Objetivo
Eliminar los bugs de sincronización del modelo híbrido haciendo la **nube la única fuente
de verdad**, con **login obligatorio**. localStorage queda solo como **cache de arranque
descartable** (nunca manda). No se reescribe la app a async: los reads siguen síncronos
desde el cache.

## Decisiones
- **Login obligatorio**: sin sesión no se usa la app (gate a pantalla completa). Se gatea
  **todo** (incluido el libro).
- **La nube siempre pisa el cache en el boot** (sin reconciliación de dos vías).
- **Cache descartable**: en cada boot la nube manda; las escrituras son write-through.
- Se pierde el juego anónimo y offline (el boot necesita la nube). Aceptado.

## Arquitectura / flujo

### Boot (por carga de página)
1. Overlay *"Cargando…"* cubre la app por defecto (opaco, full-screen, z-index alto).
2. `nube.js` escucha auth:
   - **Sin sesión** → el overlay muestra la **pantalla de login** (botón Google). Fin.
   - **Con sesión** → `boot()`: baja `estado` de la nube e hidrata el cache.
3. Hidratación robusta (mata el loop):
   - `antes = serial(snapshot())`; `aplicarNube(cloud)`; si **cambió** (`antes !==
     serial(snapshot())`) y no se hidrató ya esta sesión → **recarga UNA vez** (acotada por
     `sessionStorage 'nube:hidratado'`), tapada por el overlay. Si no cambió → dispatch
     `nube:listo`.
   - `aplicarNube` setea `_ultima = serial(snapshot())` (del cache real, no del crudo) →
     elimina la asimetría de `null` que causaba reloads infinitos.
4. Cuenta nueva / migración: si la nube está vacía pero el cache tiene datos (jugaste
   anónimo antes) → se **sube una vez** como semilla; luego la nube manda.
5. Al terminar: `sessionStorage 'nube:hidratado'='1'` + dispatch `nube:listo` → Base saca
   el overlay. La app debajo ya quedó con datos correctos (por la recarga o porque no había
   cambio).

### Escrituras (write-through)
Sin cambios respecto a hoy: cada cambio actualiza el cache (síncrono) y el watcher lo sube
(debounce 1.5s + flush en `pagehide`/`visibilitychange`). El cache es espejo; en el próximo
boot la nube manda.

### Realtime (ya existe)
Suscripción a tu propia fila de `progreso`: cambios externos (intercambios) entran en vivo
al cache + UI (toast), sin recargar.

## Componentes a tocar
- **`web/src/lib/nube.js`** (reescritura del boot):
  - `init()`: registra auth; con sesión → `suscribirProgreso` + `boot()`; sin sesión →
    dispatch `nube:sinsesion`.
  - `boot()`: guard de módulo `_booteado` (corre una vez por página aunque se llame init()
    varias veces) + `sessionStorage 'nube:hidratado'` (acota la recarga entre cargas).
    Hidrata, decide recarga, dispatch `nube:listo`.
  - `aplicarNube`: `_ultima = serial(snapshot())`.
  - `logout()`: limpia `nube:hidratado` (+ `nube:fusionado` viejo), `_booteado=false`,
    signOut, reload.
- **`web/src/layouts/Base.astro`**:
  - Overlay `#boot-overlay` (loader + caja de login con botón Google). Visible por defecto.
  - Script: `nube:listo` → ocultar overlay; `nube:cambio`/`nube:sinsesion` → si no hay
    usuario, mostrar la caja de login; si hay, mostrar el loader.
  - El botón ☁️ existente queda para ver sesión / cerrar sesión (logout).
- **`coleccion.js`, páginas, lógica de juego**: **sin cambios** (siguen leyendo el cache
  síncrono). El overlay las tapa hasta que el cache está correcto.

## Bordes
- Doble `init()` (Base + alguna página) → `boot()` corre una vez por el guard de módulo.
- OAuth redirect: tras volver de Google, `onAuthStateChange` dispara `SIGNED_IN` → boot.
- Recarga acotada: tras la primera hidratación de la sesión, `nube:hidratado` evita
  re-recargas; además `antes==despues` en cargas siguientes (cache ya == nube).
- Sin red / sin sesión: overlay queda en login o loader; la app no entra (esperado).

## Verificación
- `npm run build` OK. Screenshots del overlay (login + loader). Prueba manual: login →
  carga progreso; cambio en una sesión se refleja por realtime; cerrar/abrir sin re-login
  innecesario y sin loop de recarga.
- No hay runner JS. Sin migración SQL nueva (usa tablas/realtime existentes).
