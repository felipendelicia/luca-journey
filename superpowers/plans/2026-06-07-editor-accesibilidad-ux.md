# Editor a11y + UX — Implementation Plan

> **For agentic workers:** ejecución inline (executing-plans) por el controlador. Steps con checkbox.

**Goal:** maximizar accesibilidad (teclado/lector) y uso (ergonomía, móvil) del editor CodeMirror 6 compartido.

**Architecture:** todo en `web/src/lib/editor.js` (factory `editorPython`) + `global.css` + `aria-live` en las 5 páginas que lo usan. Misma firma de `editorPython` (no romper call sites).

**Tech:** CodeMirror 6 (`@codemirror/commands` 6.10.3, `@codemirror/autocomplete` 6.20.3, `@codemirror/state` Compartment), Astro, Playwright para verificar.

---

### Task 1: `editor.js` — keymaps (Tab/Esc), tema reactivo, line-wrap, aria

**Files:** Modify `web/src/lib/editor.js`.

- [ ] Imports: `import { insertTab, indentLess } from '@codemirror/commands';` `import { acceptCompletion, completionStatus } from '@codemirror/autocomplete';` `import { Compartment } from '@codemirror/state';`
- [ ] Reemplazar `keymap.of([indentWithTab])` por keymap de ALTA precedencia (antes de `basicSetup` en el array `ext`, o vía `Prec.highest`):
  ```js
  keymap.of([
    { key: 'Tab', run: (v) => (completionStatus(v.state) ? acceptCompletion(v) : insertTab(v)), shift: indentLess },
    { key: 'Escape', run: (v) => { v.contentDOM.blur(); return true; } },
  ]),
  ```
  Quitar el import de `indentWithTab` si queda sin uso. Mantener el keymap de `Mod-Enter` (correr).
- [ ] Tema reactivo: `const temaComp = new Compartment();` y en `ext` `temaComp.of(modoOscuro() ? oneDark : temaClaro)`. `modoOscuro = () => !document.body.classList.contains('claro')`. `temaClaro` = `EditorView.theme({ '&': { backgroundColor: 'var(--paper-2, #f6f7fb)', color: 'var(--ink, #1c2230)' }, '.cm-gutters': { backgroundColor: 'var(--paper-2,#eef0f6)', color: 'var(--ink-soft,#6b7280)', border: 'none' }, '.cm-activeLine': { backgroundColor: 'rgba(0,0,0,.04)' }, '.cm-activeLineGutter': { backgroundColor: 'rgba(0,0,0,.05)' }, '.cm-selectionBackground': { backgroundColor: 'rgba(80,130,255,.22)' } }, { dark: false })`. Tras crear la vista, observar cambios de tema: `new MutationObserver(() => view.dispatch({ effects: temaComp.reconfigure(modoOscuro() ? oneDark : temaClaro) })).observe(document.body, { attributes: true, attributeFilter: ['class'] })`.
- [ ] `EditorView.lineWrapping` en `ext`.
- [ ] aria: `EditorView.contentAttributes.of({ 'aria-label': 'Editor de código Python' })` en `ext`.
- [ ] Build OK: `cd web && npm run build`.
- [ ] Commit: `git add web/src/lib/editor.js && git commit -m "editor: Tab acepta sugerencia o indenta en el cursor (VS Code) + Esc suelta foco + tema claro/oscuro reactivo + line-wrap + aria-label"`

---

### Task 2: `editor.js` — barra del editor (chrome) + prefs + `global.css`

**Files:** Modify `web/src/lib/editor.js`, `web/src/styles/global.css`. (frontend-design para la barra.)

- [ ] En `editorPython`, tras crear `view`, construir una **barra** y montarla en `parent` (después del `.cm-editor`). La barra (`.ed-bar`) tiene:
  - **Símbolos** que insertan en el cursor: `:` `(` `)` `[` `]` `"` `=`. Insertar con:
    ```js
    const insertar = (t) => { const r = view.state.replaceSelection(t); view.dispatch(r); view.focus(); };
    ```
  - **⇥ / ⇤** indent/dedent: botones que ejecutan `insertTab(view)` / `indentLess(view)`.
  - **A− / A+**: cambian `editor:fontPx` (localStorage, rango 12–22). Aplicar vía CSS var en el wrapper: el `parent` (o un wrapper `.ed-wrap`) setea `style.setProperty('--cm-font', px+'px')`, y el CSS hace `.cm-editor{ font-size: var(--cm-font, 14px); }`. Aplica a TODOS los editores (todos leen `editor:fontPx` al montar + un evento `editor:font` que re-aplica en vivo).
  - **Copiar**: `navigator.clipboard.writeText(view.state.doc.toString())` + feedback.
  - **Chip "⌨" de atajos**: botón con `title`/popover: `⌘/Ctrl+Enter correr · Tab sugerencia/indent · Esc salir` (detectar Mac: `navigator.platform`).
- [ ] Prefs: leer `editor:fontPx` al montar (default 14). A−/A+ persisten + despachan `window` `editor:font` para sincronizar otros editores en la página.
- [ ] `global.css`: `.ed-bar` (flex, wrap, sticky bottom del bloque, targets ≥36px, tema-aware), `.ed-sym` botones monospace, `.ed-chip` atajos, `.cm-editor.cm-focused` outline visible, `.cm-editor{ font-size: var(--cm-font,14px); }`. `prefers-reduced-motion` → sin transición. Móvil: la barra scrollea horizontal si no entra.
- [ ] Build OK + Playwright: barra inserta `()` en el cursor, A+ agranda y persiste tras reload.
- [ ] Commit: `git add web/src/lib/editor.js web/src/styles/global.css && git commit -m "editor: barra de herramientas (símbolos móvil, A−/A+ fuente, copiar, atajos) + foco visible"`

---

### Task 3: 5 páginas — salida accesible (`aria-live`) + nombres de botones

**Files:** Modify `web/src/pages/ejercicios/[slug]/[ex].astro`, `libro/[...slug].astro`, `proyectos/[slug].astro`, `desafios/crear.astro`, `desafios/ver.astro`.

- [ ] En cada página, al contenedor donde se renderiza el resultado de correr/corregir (p.ej. `#result`, la salida del ▶), agregar `role="status" aria-live="polite"`. (Buscar el contenedor de salida en cada una.)
- [ ] Verificar que los botones de correr/corregir/ejecutar/reiniciar tengan nombre accesible (texto visible alcanza; si alguno es solo ícono, agregar `aria-label`).
- [ ] Build OK.
- [ ] Commit: `git add web/src/pages && git commit -m "ejercicios/libro/proyectos/desafios: salida del editor con aria-live (lectores anuncian el resultado) + botones con nombre accesible"`

---

### Task 4: ayuda + verificación final

**Files:** Modify `web/src/pages/ayuda.astro`.

- [ ] Nota corta en ayuda: atajos del editor (Ctrl/⌘+Enter correr, Tab sugerencia/indent, Esc salir) + barra de símbolos/tamaño.
- [ ] Verificación Playwright (dev, `/ejercicios/.../`): Tab con popup acepta; Tab sin popup inserta 4 espacios en el cursor; Esc saca el foco; `#result` tiene aria-live; modo claro usa tema claro. Screenshots claro/oscuro + móvil.
- [ ] Build OK. Commit: `git add web/src/pages/ayuda.astro docs && git commit -m "docs: ayuda con atajos y accesibilidad del editor"`

---

## Notas
- No tocar el runner (worker/pyodide) ni la corrección.
- `editor.js` es la fuente única; las 5 páginas heredan el chrome sin duplicar.
- Sin atribución Claude en commits.
