# Editor de código — accesibilidad + UX — diseño

**Fecha:** 2026-06-07
**Estado:** diseño aprobado ("avanza"). Pendiente plan + implementación.
**Tema:** maximizar accesibilidad (teclado/lector) + uso (ergonomía, móvil) del editor de código
(CodeMirror 6) que se usa en libro, ejercicios, proyectos y desafíos. Fuente única: la factory
`web/src/lib/editor.js` (`editorPython`). Relacionado: [[libro-activo-visualizador]].

## Problema

`editorPython` hoy:
- **Tab atrapa**: `keymap.of([indentWithTab])` hace que Tab SIEMPRE indente (reindenta el inicio de
  la línea) y **nunca acepte el autocompletado**. Queja directa del usuario.
- **Tema siempre oscuro** (`oneDark`), aun en modo claro de la página → contraste/consistencia.
- **Sin salida accesible**: el resultado de correr no se anuncia a lectores de pantalla.
- **Sin ayudas móviles**: teclados de celular no tienen `:`, `()`, `[]`, comillas a mano.
- **Sin control de tamaño de fuente**, sin ajuste de línea, sin atajos visibles.

## Decisiones (brainstorming 2026-06-07)

Prioridades elegidas: **A11y formal (teclado/lector)**, **Ergonomía de uso**, **Móvil/principiantes**.
- **Tab = estilo VS Code:** popup abierto ⇒ **acepta** la sugerencia; si no ⇒ inserta indentación
  **en el cursor** (inline, no al inicio de línea). Shift+Tab = dedent.

## Arquitectura

Todo cuelga de `web/src/lib/editor.js`. `editorPython({ doc, parent, onRun, onChange, extra })` se
amplía para: (a) arreglar el keymap de Tab; (b) tema claro/oscuro reactivo; (c) line-wrap; (d) Esc para
soltar el foco; y para **montar una barra de herramientas** (chrome) alrededor del editor con: barra de
símbolos (móvil), A−/A+, copiar, y un chip de atajos. La barra se inserta en el `parent` junto al
`EditorView` (un wrapper). Las 5 páginas no cambian su llamada (misma firma); solo se les agrega
`aria-live` al contenedor de resultados.

Unidades:
- `editor.js` — factory + chrome + tema + keymaps + helpers de preferencias. (Crece, pero es la unidad
  natural del editor; si queda muy grande, separar `editor-chrome.js`.)
- Páginas (`ejercicios/[slug]/[ex].astro`, `libro/[...slug].astro`, `proyectos/[slug].astro`,
  `desafios/crear.astro`, `desafios/ver.astro`) — agregar `aria-live`/`role` al área de salida y
  nombres accesibles a los botones. La barra del editor la inyecta `editor.js` (no duplicar en cada page).
- `global.css` — estilos de la barra del editor, chip de atajos, foco visible, tema claro de CM.

## Componentes / detalle

### 1. Tecla Tab (fix) + keymaps
En `editorPython`, reemplazar `keymap.of([indentWithTab])` por (precedencia ALTA, antes de basicSetup):
```js
import { insertTab, indentLess } from '@codemirror/commands';
import { acceptCompletion, completionStatus } from '@codemirror/autocomplete';
keymap.of([
  { key: 'Tab', run: (v) => (completionStatus(v.state) ? acceptCompletion(v) : insertTab(v)), shift: indentLess },
  { key: 'Escape', run: (v) => { v.contentDOM.blur(); return true; } },   // a11y: soltar el foco del editor
]);
```
`insertTab` inserta `indentUnit` (4 espacios) **en el cursor** cuando no hay selección (VS Code), e
indenta el bloque cuando hay selección multilínea. Mantener `Mod-Enter` (correr) como está.

### 2. Tema reactivo claro/oscuro
- `Compartment` para el tema. En modo oscuro → `oneDark`; en claro → un tema CM claro (default de
  basicSetup o un `EditorView.theme` claro propio que matchee `--paper`/`--ink`). Detectar el modo por
  `document.body.classList.contains('claro')` y reaccionar con un `MutationObserver` sobre `body[class]`
  (el toggle de Base.astro togglea `body.claro`). `view.dispatch({ effects: temaComp.reconfigure(...) })`.

### 3. Accesibilidad (teclado/lector)
- **Esc** suelta el foco (arriba). Pista visible "Esc para salir" en la barra.
- `contentDOM` con `aria-label="Editor de código Python"` (vía `EditorView.contentAttributes`).
- **Foco visible**: outline claro en `.cm-editor.cm-focused` (CSS).
- **Salida accesible**: en cada página, el contenedor de resultado (`#result`, etc.) lleva
  `role="status" aria-live="polite"` → el lector anuncia "✓ tests pasados" / el error al correr.
- Botones con texto/`aria-label` claros (ya tienen texto visible; verificar Ejecutar/Corregir/Reiniciar).

### 4. Barra del editor (chrome) — ergonomía + móvil
Una barra (debajo del editor, sticky) que `editor.js` inyecta:
- **Símbolos** (insertan en el cursor con `view.dispatch(insertText)`): `:` `(` `)` `[` `]` `"` `=`
  y **⇥ indent / ⇤ dedent**. Targets táctiles ≥ 36px.
- **A− / A+**: tamaño de fuente del editor (compartment de `EditorView.theme({ '&': { fontSize } })` o
  CSS var en el wrapper). Rango p.ej. 12–22px. Persistir `editor:fontPx` (localStorage), aplica a TODOS
  los editores.
- **Copiar**: copia el contenido al portapapeles (`navigator.clipboard`).
- **Chip de atajos "⌨"**: tooltip/popover con `Ctrl/Cmd+Enter` correr · `Tab` sugerencia/indent · `Esc`
  salir. (Detectar Mac para mostrar ⌘.)
- **Line wrap** on por defecto (`EditorView.lineWrapping`) — sin scroll horizontal en celu.

### 5. Preferencias
`editor:fontPx` (y, si se agrega toggle de wrap, `editor:wrap`) en localStorage; se leen al crear cada
editor y la barra las cambia en vivo para el editor activo (font aplica a todos los montados vía un
pequeño registro de vistas o un CSS var global `--cm-font`).

### 6. reduce-motion / alto contraste
Sin animaciones de la barra si `prefers-reduced-motion`. El tema claro/oscuro ya da buen contraste; foco
visible con outline grueso.

## Testing
- No hay unit test de CodeMirror. Verificación con **Playwright** (dev) en `/ejercicios/.../`:
  - Tab con popup abierto **acepta** la sugerencia; Tab sin popup inserta 4 espacios **en el cursor**.
  - `Escape` saca el foco del editor (document.activeElement deja de ser `.cm-content`).
  - El `#result` tiene `aria-live="polite"`.
  - La barra de símbolos inserta `()` en el cursor; A+ agranda la fuente y persiste tras recargar.
  - Modo claro → el editor usa tema claro (no oneDark); modo oscuro → oneDark.
- `cd web && npm run build` verde. Screenshots: editor en claro y oscuro, barra en móvil (viewport angosto).

## Compat / alcance
- Misma firma de `editorPython` → las 5 páginas siguen andando; solo se agrega chrome + aria.
- **Fuera de alcance:** linusing/diagnostics de Python en vivo, multi-cursor avanzado, minimapa,
  formateo automático (autopep8). El toggle de wrap puede quedar para después (wrap on por defecto).
- **No** se toca el runner (worker/pyodide) ni la lógica de corrección.

## Archivos afectados
- `web/src/lib/editor.js` — keymaps (Tab/Esc), tema reactivo (Compartment + MutationObserver), lineWrapping,
  chrome (barra símbolos/font/copiar/atajos), prefs, `contentAttributes` aria.
- `web/src/styles/global.css` — barra del editor, chip atajos, foco visible, tema claro CM.
- 5 páginas — `role="status" aria-live="polite"` en el contenedor de resultados + verificar nombres de
  botones. (Sin cambiar la llamada a `editorPython`.)
- `web/src/pages/ayuda.astro` — nota corta de los atajos/accesibilidad del editor.
