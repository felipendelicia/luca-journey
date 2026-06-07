// editor.js — fábrica del editor de código (CodeMirror 6) usado en libro, playground
// y ejercicios. Autocompletado Python rico, indentación de 4 espacios, cierre de
// brackets, y atajo Ctrl/Cmd+Enter para correr.
import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { Prec, Compartment } from '@codemirror/state';
import { indentMore, indentLess } from '@codemirror/commands';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { indentUnit } from '@codemirror/language';
import { snippetCompletion as snip, acceptCompletion, completionStatus } from '@codemirror/autocomplete';
import { linter, lintGutter } from '@codemirror/lint';
import { checkSintaxis } from './pyrun.js';

const kw = (label, info) => ({ label, type: 'keyword', info });
const bi = (label, info) => ({ label, type: 'function', info });
const mt = (label, info) => ({ label, type: 'method', info });

// palabras clave + funciones built-in (se sugieren al escribir)
const PALABRAS = [
  kw('def', 'definir una función'), kw('return', 'devolver un valor'),
  kw('if', 'condición'), kw('elif', 'si no, si...'), kw('else', 'si no'),
  kw('for', 'bucle sobre una secuencia'), kw('while', 'bucle mientras'),
  kw('in', 'pertenece a'), kw('not', 'negación'), kw('and', 'y'), kw('or', 'o'), kw('is', 'es'),
  kw('None', 'nada'), kw('True', 'verdadero'), kw('False', 'falso'),
  kw('class', 'definir una clase'), kw('self', 'el objeto actual'),
  kw('import', 'importar un módulo'), kw('from', 'desde un módulo'), kw('as', 'apodo'),
  kw('try', 'intentar'), kw('except', 'atrapar un error'), kw('finally', 'al final'),
  kw('raise', 'lanzar un error'), kw('with', 'context manager'), kw('lambda', 'función de una línea'),
  kw('pass', 'no hacer nada'), kw('break', 'cortar el bucle'), kw('continue', 'saltar al siguiente'),
  kw('yield', 'generador'), kw('global', 'variable global'), kw('assert', 'afirmar'), kw('del', 'borrar'),
  bi('print', 'imprimir en pantalla'), bi('len', 'longitud'), bi('range', 'rango de números'),
  bi('int', 'a entero'), bi('str', 'a texto'), bi('float', 'a decimal'), bi('bool', 'a booleano'),
  bi('list', 'a lista'), bi('dict', 'a diccionario'), bi('set', 'a conjunto'), bi('tuple', 'a tupla'),
  bi('sum', 'suma'), bi('min', 'mínimo'), bi('max', 'máximo'), bi('abs', 'valor absoluto'),
  bi('round', 'redondear'), bi('sorted', 'ordenar'), bi('reversed', 'invertir'),
  bi('enumerate', 'pares (índice, valor)'), bi('zip', 'combinar listas'),
  bi('map', 'aplicar a cada uno'), bi('filter', 'filtrar'), bi('type', 'tipo de dato'),
  bi('isinstance', 'es de un tipo'), bi('input', 'pedir texto al usuario'), bi('open', 'abrir un archivo'),
  bi('any', 'alguno es True'), bi('all', 'todos son True'), bi('super', 'la clase padre'),
  bi('Exception', 'error genérico'), bi('ValueError', 'valor inválido'),
  bi('TypeError', 'tipo inválido'), bi('KeyError', 'clave inexistente'),
  bi('IndexError', 'posición inexistente'), bi('ZeroDivisionError', 'división por cero'),
];

// snippets (plantillas que se completan con Tab entre los huecos)
const SNIPPETS = [
  snip('def ${nombre}(${parametros}):\n\t${cuerpo}', { label: 'def', type: 'keyword', detail: 'función', boost: 1 }),
  snip('for ${x} in ${iterable}:\n\t${cuerpo}', { label: 'for', type: 'keyword', detail: 'bucle', boost: 1 }),
  snip('if ${condicion}:\n\t${cuerpo}', { label: 'if', type: 'keyword', detail: 'condición', boost: 1 }),
  snip('while ${condicion}:\n\t${cuerpo}', { label: 'while', type: 'keyword', detail: 'bucle' }),
  snip('try:\n\t${cuerpo}\nexcept ${Error}:\n\t${manejo}', { label: 'try', type: 'keyword', detail: 'manejo de error' }),
  snip('class ${Nombre}:\n\tdef __init__(self${parametros}):\n\t\t${cuerpo}', { label: 'class', type: 'keyword', detail: 'clase' }),
];

// métodos comunes (se sugieren después de un punto)
const METODOS = [
  mt('append', 'agregar al final'), mt('extend', 'agregar varios'), mt('insert', 'insertar en una posición'),
  mt('remove', 'quitar un valor'), mt('pop', 'sacar y devolver'), mt('sort', 'ordenar'),
  mt('reverse', 'invertir'), mt('index', 'posición de un valor'), mt('count', 'contar apariciones'),
  mt('copy', 'copiar'), mt('clear', 'vaciar'),
  mt('keys', 'claves del dict'), mt('values', 'valores del dict'), mt('items', 'pares (clave, valor)'),
  mt('get', 'obtener con default'), mt('update', 'actualizar'),
  mt('upper', 'a MAYÚSCULAS'), mt('lower', 'a minúsculas'), mt('strip', 'sacar espacios'),
  mt('split', 'partir el texto'), mt('join', 'unir una lista'), mt('replace', 'reemplazar'),
  mt('startswith', '¿empieza con?'), mt('endswith', '¿termina con?'), mt('find', 'buscar'),
  mt('format', 'formatear'), mt('capitalize', 'primera en mayúscula'), mt('title', 'cada palabra capitalizada'),
  mt('isdigit', '¿son dígitos?'), mt('add', 'agregar a un set'),
  // pandas / numpy
  mt('mean', 'promedio'), mt('std', 'desvío estándar'), mt('head', 'primeras filas'), mt('tail', 'últimas filas'),
  mt('sort_values', 'ordenar por columna'), mt('groupby', 'agrupar'), mt('value_counts', 'contar por valor'),
  mt('dropna', 'quitar NaN'), mt('fillna', 'rellenar NaN'), mt('drop', 'quitar columna/fila'),
  mt('drop_duplicates', 'quitar duplicados'), mt('rename', 'renombrar'), mt('apply', 'aplicar a cada uno'),
  mt('astype', 'cambiar de tipo'), mt('reshape', 'cambiar la forma'), mt('flatten', 'aplanar'),
  mt('shape', 'forma (filas, columnas)'), mt('columns', 'las columnas'), mt('idxmax', 'índice del máximo'),
  // sqlite
  mt('execute', 'ejecutar SQL'), mt('executemany', 'ejecutar varios'), mt('fetchone', 'traer una fila'),
  mt('fetchall', 'traer todas'), mt('cursor', 'crear un cursor'), mt('commit', 'guardar cambios'),
  // sklearn
  mt('fit', 'entrenar'), mt('predict', 'predecir'), mt('predict_proba', 'probabilidades'),
  mt('score', 'exactitud'), mt('fit_transform', 'ajustar y transformar'),
  mt('labels_', 'grupos asignados'), mt('feature_importances_', 'importancia de features'),
];

function fuentePython(context) {
  const punto = context.matchBefore(/\.\w*/);
  if (punto) return { from: punto.from + 1, options: METODOS, validFor: /^\w*$/ };
  const palabra = context.matchBefore(/\w+/);
  if (!palabra && !context.explicit) return null;
  return { from: palabra ? palabra.from : context.pos, options: [...SNIPPETS, ...PALABRAS], validFor: /^\w*$/ };
}

// tema claro del editor (modo claro de la página); en oscuro usamos oneDark.
const temaClaro = EditorView.theme({
  '&': { backgroundColor: 'var(--paper-2, #f6f7fb)', color: 'var(--ink, #1c2230)' },
  '.cm-gutters': { backgroundColor: 'var(--paper-2, #eef0f6)', color: 'var(--ink-soft, #6b7280)', border: 'none' },
  '.cm-activeLine': { backgroundColor: 'rgba(0,0,0,.045)' },
  '.cm-activeLineGutter': { backgroundColor: 'rgba(0,0,0,.06)' },
  '.cm-selectionBackground, &.cm-focused .cm-selectionBackground': { backgroundColor: 'rgba(80,130,255,.22)' },
  '.cm-cursor': { borderLeftColor: 'var(--ink, #1c2230)' },
}, { dark: false });

// inserta la indentación (4 espacios = indentUnit) EN EL CURSOR (estilo VS Code);
// si hay selección multilínea, indenta el bloque. NO inserta un tab literal.
function insertIndent(view) {
  const { state } = view;
  if (state.selection.ranges.some((r) => !r.empty)) return indentMore(view);
  view.dispatch(state.update(state.replaceSelection(state.facet(indentUnit)), { userEvent: 'input', scrollIntoView: true }));
  return true;
}

// mensajes cortos en español para los SyntaxError más comunes (si no matchea, el detalle de Python).
const TRAD_SINTAXIS = [
  [/expected ':'/i, "falta el ':' al final (después de if/for/while/def…)"],
  [/was never closed|unexpected EOF/i, "quedó un ( [ { o una comilla sin cerrar"],
  [/inconsistent use of tabs/i, 'mezclaste tabs y espacios — usá solo espacios'],
  [/unexpected indent/i, 'hay espacios de más al principio de la línea'],
  [/expected an indented block/i, "después de ':' la línea va con 4 espacios de sangría"],
  [/unindent does not match/i, 'la sangría no coincide con ningún bloque de afuera'],
  [/invalid syntax/i, 'algo está mal escrito (¿falta : , ) o usaste = en vez de ==?)'],
];
const traducirSintaxis = (m) => { for (const [re, es] of TRAD_SINTAXIS) if (re.test(m)) return es; return m || 'revisá esta línea'; };

// linter inline: subraya el SyntaxError exacto (Pyodide compile(), sin ejecutar), estilo VS Code.
const pyLinter = linter(async (view) => {
  const code = view.state.doc.toString();
  if (!code.trim()) return [];
  let info = null;
  try { info = await checkSintaxis(code); } catch { info = null; }
  if (!info || !info.lineno) return [];
  const doc = view.state.doc;
  const lineObj = doc.line(Math.min(Math.max(1, info.lineno), doc.lines));
  let from = lineObj.from + Math.max(0, (info.offset || 1) - 1);
  let to = lineObj.to;
  // si end_offset cae en la MISMA línea, ajustamos el final; si no, subrayamos hasta el fin de la línea.
  if (info.end_lineno === info.lineno && info.end_offset) to = lineObj.from + Math.max(0, info.end_offset - 1);
  // mantener el rango DENTRO de la línea del error y garantizar ≥1 carácter subrayado (visible).
  from = Math.max(lineObj.from, Math.min(from, lineObj.to));
  to = Math.min(Math.max(to, from), lineObj.to);
  if (to <= from) { from = Math.max(lineObj.from, lineObj.to - 1); to = lineObj.to; }
  const esIndent = info.type === 'IndentationError' || info.type === 'TabError';
  return [{ from, to, severity: 'error', source: 'Python',
    message: (esIndent ? 'Indentación: ' : 'Sintaxis: ') + traducirSintaxis(info.msg || '') }];
}, { delay: 700 });

const modoOscuro = () => !document.body.classList.contains('claro');
const esMac = typeof navigator !== 'undefined' && /Mac|iPhone|iPad/.test(navigator.platform || '');
const fontPx = () => { const n = parseInt(localStorage.getItem('editor:fontPx'), 10); return n >= 12 && n <= 22 ? n : 14; };

// registro de editores montados → A−/A+ aplica el tamaño de fuente a TODOS en vivo (CSS var por wrapper).
const _wraps = new Set();
function aplicarFont() { const px = fontPx() + 'px'; _wraps.forEach((w) => w.style.setProperty('--cm-font', px)); }
if (typeof window !== 'undefined') window.addEventListener('editor:font', aplicarFont);

// Crea el editor. opts: { doc, parent, onRun, onChange, extra, barra=true }
export function editorPython({ doc = '', parent, onRun, onChange, extra = [], barra = true } = {}) {
  const py = python();
  const temaComp = new Compartment();
  const ext = [
    basicSetup,
    py,
    py.language.data.of({ autocomplete: fuentePython }),
    temaComp.of(modoOscuro() ? oneDark : temaClaro),
    indentUnit.of('    '),
    EditorView.lineWrapping,
    EditorView.contentAttributes.of({ 'aria-label': 'Editor de código Python' }),
    pyLinter, lintGutter(),   // subrayado de errores de sintaxis (inline, estilo VS Code)
    // Tab: acepta la sugerencia si el popup está abierto; si no, indenta EN EL CURSOR (estilo VS Code).
    // Esc suelta el foco del editor (accesibilidad de teclado). Alta precedencia para ganarle a basicSetup.
    Prec.highest(keymap.of([
      { key: 'Tab', run: (v) => (completionStatus(v.state) ? acceptCompletion(v) : insertIndent(v)), shift: indentLess },
      { key: 'Escape', run: (v) => { v.contentDOM.blur(); return true; } },
    ])),
  ];
  if (onRun) ext.push(keymap.of([{ key: 'Mod-Enter', preventDefault: true, run: () => { onRun(); return true; } }]));
  if (onChange) ext.push(EditorView.updateListener.of((v) => { if (v.docChanged) onChange(v.state.doc.toString()); }));
  ext.push(...extra);

  const view = new EditorView({ doc, parent, extensions: ext });
  parent.style.setProperty('--cm-font', fontPx() + 'px');   // el .cm-editor hereda font-size: var(--cm-font)
  _wraps.add(parent);

  // tema reactivo: re-configura al cambiar la página entre claro/oscuro
  new MutationObserver(() => view.dispatch({ effects: temaComp.reconfigure(modoOscuro() ? oneDark : temaClaro) }))
    .observe(document.body, { attributes: true, attributeFilter: ['class'] });

  if (barra) montarBarra(view, parent);
  return view;
}

// barra de herramientas: símbolos (móvil), tamaño de fuente, copiar, atajos.
function montarBarra(view, parent) {
  const insertar = (t) => { view.dispatch(view.state.replaceSelection(t)); view.focus(); };
  const SIM = [':', '(', ')', '[', ']', '"', "'", '='];
  const q = (s) => (s === '"' ? '&quot;' : s);
  const simBtns = SIM.map((s) => `<button type="button" class="ed-sym" data-ins="${q(s)}" tabindex="-1" aria-label="Insertar ${s === '"' ? 'comillas' : s}">${q(s)}</button>`).join('');
  const mod = esMac ? '⌘' : 'Ctrl';
  const bar = document.createElement('div');
  bar.className = 'ed-bar';
  bar.setAttribute('role', 'toolbar');
  bar.setAttribute('aria-label', 'Herramientas del editor');
  bar.innerHTML =
    `<div class="ed-syms">${simBtns}` +
    `<button type="button" class="ed-sym" data-cmd="indent" tabindex="-1" aria-label="Indentar">⇥</button>` +
    `<button type="button" class="ed-sym" data-cmd="dedent" tabindex="-1" aria-label="Quitar indentación">⇤</button></div>` +
    `<div class="ed-tools">` +
    `<button type="button" class="ed-tool" data-cmd="menos" aria-label="Achicar texto">A−</button>` +
    `<button type="button" class="ed-tool" data-cmd="mas" aria-label="Agrandar texto">A+</button>` +
    `<button type="button" class="ed-tool" data-cmd="copiar" aria-label="Copiar código">⧉</button>` +
    `<button type="button" class="ed-tool ed-chip" data-cmd="atajos" aria-label="Atajos de teclado" title="${mod}+Enter: correr · Tab: sugerencia o indentar · Esc: salir del editor">⌨</button>` +
    `</div>`;
  parent.appendChild(bar);
  bar.addEventListener('click', (e) => {
    const b = e.target.closest('button'); if (!b) return;
    if (b.dataset.ins != null) return insertar(b.dataset.ins);
    const c = b.dataset.cmd;
    if (c === 'indent') { insertIndent(view); view.focus(); }
    else if (c === 'dedent') { indentLess(view); view.focus(); }
    else if (c === 'mas' || c === 'menos') {
      const px = Math.max(12, Math.min(22, fontPx() + (c === 'mas' ? 2 : -2)));
      localStorage.setItem('editor:fontPx', String(px)); window.dispatchEvent(new Event('editor:font'));
    } else if (c === 'copiar') {
      try { navigator.clipboard.writeText(view.state.doc.toString()); const t = b.textContent; b.textContent = '✓'; setTimeout(() => { b.textContent = t; }, 1200); } catch {}
    }
  });
}
