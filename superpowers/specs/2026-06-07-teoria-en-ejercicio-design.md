# Teoría en el ejercicio (sin salir) — diseño

**Fecha:** 2026-06-07 · **Estado:** aprobado ("dale avanza").
**Problema:** al hacer un ejercicio, si el alumno no recuerda algo tiene que **salir** al Libro (recarga,
pierde su código y su lugar). Solución: ver la teoría **sin salir del ejercicio**.

## Decisiones (brainstorming 2026-06-07)
- **Forma:** **ventana modal centrada** con fondo oscurecido.
- **Contenido:** el **capítulo del libro de ese tema** (mismo slug — `tema.slug` ↔ capítulo del libro,
  verificado **72/72**). Reusa el contenido existente, **cero autoría extra**, siempre al día.
- **Volver = cerrar:** ✕ / `Esc` / tocar el fondo → vuelve al ejercicio con el **código intacto** (nunca
  navegó: la modal es una capa sobre la misma página).
- **Modo lectura:** ejemplos de código **estáticos** (sin editores ni Pyodide en la modal); las **quizzes**
  (práctica) se ocultan — en la modal va solo la teoría.
- **Mini-índice:** los títulos `##`/`###` del capítulo, para saltar sin scrollear todo.

## Arquitectura
Todo en `web/src/pages/ejercicios/[slug]/[ex].astro` + `global.css`. El libro es una **content collection**
de Astro (`getCollection('libro')`, `cap.render()` → `<Content/>`). En el frontmatter del ejercicio traigo
la entrada del libro cuyo `slug === tema.slug` y **renderizo su `<Content/>` dentro de la modal** (oculta por
defecto). Se **inlinea** el HTML del capítulo en la página (offline-friendly; ~10 KB por página, aceptable).

### Componentes
- **Frontmatter `[ex].astro`:** `const cap = (await getCollection('libro')).find(c => c.slug === payload.slug);`
  `const Teoria = cap ? (await cap.render()).Content : null;`
- **Botón `📖 Teoría`** en `.ejer-acciones` (junto a Corregir/Ejecutar/Reiniciar). Solo si `cap` existe.
- **Modal** (`#teoria-modal`, `role="dialog" aria-modal="true"`, oculta): cabecera con título del capítulo +
  ✕ + un **mini-índice** (se arma client-side de los headings); cuerpo `.teoria-cont.book` con `<Teoria />`;
  link al pie "Ver capítulo completo en el Libro ↗" (`/libro/<slug>`, por si quieren ir igual).
- **Client JS (en el `<script>` del ejercicio):**
  - abrir: el botón muestra la modal, guarda el foco previo, enfoca la modal, arma el TOC, oculta quizzes.
  - cerrar: ✕ / `Esc` / click en backdrop → oculta la modal y **devuelve el foco** al botón. Sin tocar el editor.
  - **TOC:** recorre `#teoria-cont h2, h3`, les pone `id`, y arma una lista que scrollea a cada uno.
  - **ocultar quizzes:** `#teoria-cont pre.astro-code` cuyo texto empieza con `P:` (o `data-language="quiz"`)
    → `display:none` (son práctica, no teoría).
- **CSS (`global.css`):** `.teoria-modal` (centrada, backdrop, animación de entrada, `prefers-reduced-motion`),
  `.teoria-card` (max-width ~860px, max-height ~85vh, scroll interno), `.teoria-cont.book` (reusa la
  tipografía/código del libro; código estático), `.teoria-toc` (chips/lista de saltos). Tema-aware.

## Accesibilidad
- `role="dialog" aria-modal="true" aria-label="Teoría: <título>"`; foco al abrir, `Esc` cierra, foco vuelve
  al botón al cerrar. Backdrop clickeable. Botones con nombre accesible.

## Testing
- Playwright (`/ejercicios/python-introduccion/saludo`): el botón 📖 Teoría existe; al click la modal muestra
  el contenido del capítulo (texto del cap. `python-introduccion`); `Esc`/✕/backdrop cierran; el **código del
  editor queda intacto** tras abrir/cerrar; el TOC saltea; las quizzes no se ven en la modal.
- `npm run build` verde. Screenshot de la modal (claro y oscuro).

## Alcance / no-objetivos
- **No** se corre Python en la modal (solo lectura). **No** se hace deep-link a la sección puntual por
  ejercicio (v1 = capítulo completo + TOC; el deep-link por ejercicio sería autoría extra → futuro).
- **No** se toca el runner ni la corrección. Aplica a los **72 temas** automáticamente por el slug.

## Archivos
- `web/src/pages/ejercicios/[slug]/[ex].astro` — entrada del libro + botón + modal + JS de apertura/cierre/TOC.
- `web/src/styles/global.css` — estilos de la modal de teoría.
- `web/src/pages/ayuda.astro` — nota corta ("📖 Teoría: repasá sin salir del ejercicio").
