# Intercambio mejorado — Plan (ejecutado)

> Ubicación en `superpowers/` (raíz), NO `docs/` (output del build). Ver diseño:
> `superpowers/specs/2026-06-04-intercambio-mejorado-design.md`.

Plan ya **ejecutado** en `main` el 2026-06-04. El código completo vive en el source; acá
queda el checklist de tareas como registro.

- [x] **Task 1 — Migración SQL** `supabase/migrations/20260604130000_intercambios_pedidos.sql`:
  columnas `creador_pedido`/`invitado_pedido` + RPCs `coleccion_del_otro`, `poner_pedido`.
  Aplicada al remoto con `supabase db push --yes`.
- [x] **Task 2 — `web/src/lib/trades.js`**: `coleccionOtro()`, `ponerPedido()`.
- [x] **Task 3 — `web/src/styles/global.css`**: estilos Layout A (`.tr-trato`, `.tr-piden`,
  `.tr-colec`, `.tr-cell`, `.tr-pedir`, …) + media query single-column.
- [x] **Task 4 — `web/src/pages/intercambio.astro` (markup)**: sección `#tr-sala` Layout A
  (trato / te piden / colección / botones).
- [x] **Task 5 — `intercambio.astro` (script)**: estado `miPedido`/`otroColeccion`/`ocultos`;
  `pintarLoteYo` (con ✕), `pintarLoteOtro`, `pintarPiden` (Aceptar/✕), `pintarColeccion`
  (❤/✨ + buscador), `bajarColeccionOtro`; hidratar lote/pedido al entrar; listeners.

## Verificación hecha
- `npm run build` OK (432 páginas).
- Screenshot del Layout A (desktop + mobile) con CSS real.
- Migración confirmada en remoto (`supabase migration list`: Local = Remote).

## Pendiente
- Prueba real en **dos sesiones** logueadas: crear/unirse → pedir → aceptar → quitar →
  confirmar → colecciones actualizadas.
