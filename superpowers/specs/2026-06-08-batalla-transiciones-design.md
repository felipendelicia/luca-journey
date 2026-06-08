# Batalla: transiciones y QoL — diseño

**Fecha:** 2026-06-08 · **Estado:** aprobado ("dale, está ok como lo planteas").
**Tres mejoras de UX en `web/src/pages/batalla.astro` (+ `global.css`). Todo client-only (sin deploy).**

## 1 · Reveal "VS" al encontrar partida
Hoy `emparejado` → `seleccionOnline(rival)` de una (crudo). Agregar un **overlay "VS" breve (~1.3s)**:
- `vsReveal(rival, done)`: overlay full-screen CRT. **Tu** nombre/avatar entra desde la izquierda, el del
  **rival** desde la derecha, un **⚡ flash de choque** en el medio con "VS" y "¡Rival encontrado!".
  Auto-cierra a ~1.3s y llama `done()` → `seleccionOnline`.
- Handler: `onBatalla('emparejado', (d) => { OS = null; vsReveal(d.rival, () => seleccionOnline(d.rival)); })`.
- Datos: mi `liga:nombre` + `col:avatar`; el rival de `d.rival` (nombre/handle/avatar si vienen).
- CSS: `.vs-reveal` (overlay), animaciones `vsIzq`/`vsDer` (slide-in) + `vsFlash`. Respeta `prefers-reduced-motion`
  (sin animación → muestra el cartel un instante y avanza).

## 2 · Animación de cambio de Pokémon
Hoy el sprite cambia de golpe. Agregar **recall (sale) → send-out (entra)**:
- Helper `swapSprite(imgId, c, back) → Promise`: el sprite actual hace **recall** (encoge + desvanece),
  se hace `setSpr` al nuevo, y **send-out** (aparece con fade+escala). ~0.5s total.
- Usar `swapSprite` en: **práctica** `cambiar(i)`, **PvP** `mostrarLado` (rama `cambiar`/`entra`/`reemplazo`
  de `animarRonda`), y el **reemplazo** tras debilitarse. (El `esperar(560)` de la rama cubre la animación.)
- CSS: `.bt-recall` (`@keyframes btRecall`: scale .55 + fade out), `.bt-sendout` (`btSendout`: fade+scale in).
  Funciona junto al posicionamiento por top/bottom/left de `.bt-sprite-*` (transform libre, como `bt-faint`).
  `prefers-reduced-motion` → sin animación (swap directo).

## 3 · Equipo al azar 🎲
Botón **"🎲 Al azar"** en la selección de equipo (práctica `pintarSeleccion` + PvP `seleccionOnline`):
- Elige **hasta 3 Pokémon random** de la lista **visible** (respeta el filtro de tipo activo; si no hay
  filtro, de toda la colección), los marca como seleccionados, re-pinta la grilla y habilita el botón de pelear.
- Reusa el `Set` de selección existente (`sel` / `selOnline`) + `pintarGrid()`. Helper `tomarRandom(lista, n)`.

## Testing
- Playwright (práctica): el botón **🎲 Al azar** selecciona 3 cards (clase `elegido`) y habilita `#bt-go`;
  un cambio de Pokémon en combate corre la animación de swap (clases `bt-recall`/`bt-sendout` aplicadas).
  La reveal VS necesita matchmaking real (mock del evento `emparejado` si se puede; si no, owner e2e).
- `npm run build` verde. Screenshots de la reveal VS (mockeada) y del swap.

## Alcance
- Solo animaciones/QoL de cliente. **No** cambia el motor, el protocolo ni el server.
- El "random" arma equipo **en la selección** (no es un movimiento random en combate).
- Archivos: `web/src/pages/batalla.astro`, `web/src/styles/global.css`.
