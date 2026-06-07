# Navbar "Pokédex Device" — diseño

**Fecha:** 2026-06-07 · **Estado:** aprobado en el companion visual ("perfecto" → variante **A2**).
**Objetivo:** subir la navbar a alta fidelidad: que se lea como el **bisel de hardware de un Pokédex**,
manteniendo la paleta **verde CRT** del resto de la app (cohesión), tema-aware (oscuro/claro) y con
buen colapso en móvil.

## Decisión visual (brainstorming con companion)
Dirección elegida: **A — Pokédex Device**, sub-variante **A2 (CRT verde / cohesivo)**.
- **Cluster de LEDs** a la izquierda: una **lámpara teal** (glossy, con brillo) + 3 LEDs chicos
  (rojo/amarillo/verde); el rojo **parpadea sutil**. Reemplaza la pokébola chica actual (`.pb`).
- **Marca en placa engravada** ("Pokédex **Codex**", fuente pixel; la `b` en rojo).
- **Links como botones inset/engravados** (gradiente + borde + brillo interno); **activo** = relleno
  verde-neón con texto oscuro; hover = borde/texto más claro.
- **Botones de herramientas** (tema/sonido/nube) con el mismo acabado de "botón de device".
- **Bisel:** borde superior con filo neón, sombras internas (inset), **tornillos** decorativos en las esquinas.
- **Oscuro:** device verde-negro. **Claro:** material **verde claro/menta** (placa crema, activo verde sólido).
- **Móvil:** colapsa a **☰**; lámpara + marca compactas; el menú desplegable también con estilo device.

## Arquitectura
Todo en `web/src/layouts/Base.astro` (markup del `<header class="topbar">`) + `web/src/styles/global.css`
(estilos). Es CSS + un pequeño cambio de markup en la zona de marca. **No** toca lógica/JS (el toggle de
tema/sonido, el burger y los links siguen igual).

### Markup (`Base.astro`)
La `.brand-link` pasa a contener el cluster de LEDs + la placa de marca:
```html
<a class="brand-link" href={u('/')} aria-label="Inicio — Pokédex Codex">
  <span class="dex-leds" aria-hidden="true">
    <span class="dex-lamp"></span><i class="dex-led r"></i><i class="dex-led y"></i><i class="dex-led g"></i>
  </span>
  <span class="dex-plate"><span class="brand">Pokédex <b>Codex</b></span></span>
</a>
```
- Se **reemplaza** `<span class="pb">` por el `.dex-leds`. (El `.pb` solo se usa en la navbar.)
- **Tornillos:** decorativos vía `.topbar::before/::after` (o `<i class="dex-screw l/r">`); `aria-hidden`.
- Los `.navlink`, los botones de herramientas (`#theme-toggle`, `.snd-wrap`, etc.) y el `#nav-burger`
  **no cambian de estructura** — solo de estilo.

### Estilos (`global.css`)
Consolidar/actualizar las reglas de navbar existentes (base, override CRT, claro, móvil) hacia el device:
- `.topbar`: gradiente verde-negro, filo neón superior (`::before`/box-shadow inset), sombras inset.
- `.dex-leds` / `.dex-lamp` (radial teal + brillo) / `.dex-led.r|.y|.g` (con glow; `.r` blink) /
  `.dex-screw` (radial metálico).
- `.dex-plate` (engravada) + `.brand` (pixel, `b` roja).
- `.navlink` (inset/gradiente + borde + brillo), `.navlink.activo` (relleno neón), `:hover`.
- Botones tool (`.theme-toggle`, `.snd-wrap .theme-toggle`, `#nav-burger`): acabado device redondo.
- **Claro** (`body.claro …`): material verde claro/menta (placa crema, activo verde sólido, tornillos grises).
- **Móvil** (`@media max-width:…`): links al menú desplegable; marca compacta; el burger visible.
- **`prefers-reduced-motion`:** sin parpadeo del LED.
- Mantener la **altura ~56-60px** y el `position:fixed` actuales para no romper el offset del contenido.

## Accesibilidad
- LEDs/lámpara/tornillos son **decorativos** (`aria-hidden="true"`). La `.brand-link` conserva su nombre
  accesible (link a Inicio). Links y toggles sin cambios semánticos. Contraste suficiente en ambos modos.

## Testing
- Playwright (dev): screenshots de la navbar en **oscuro**, **claro** y **móvil (≤640px, burger)**.
- Verificar que **no se rompe nada**: el toggle de tema cambia el material en vivo, el slider de sonido
  abre, el burger despliega el menú, el link activo se resalta, el offset del contenido sigue bien.
- `npm run build` verde. Comparar contra el mockup A2 aprobado.

## Alcance / no-objetivos
- Solo **estilo + markup de marca** de la navbar. **No** se tocan rutas, JS, ni otras páginas.
- **No** se agregan LEDs "funcionales" (que reflejen estado) — son decorativos (v1). Reflejar estado real
  (p.ej. LED de conexión a la nube) queda como idea futura.

## Archivos
- `web/src/layouts/Base.astro` — markup de la marca (LED cluster + placa) + tornillos decorativos.
- `web/src/styles/global.css` — estilos device de la navbar (oscuro/claro/móvil), reemplazando el look actual.
