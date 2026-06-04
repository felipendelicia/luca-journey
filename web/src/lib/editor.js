// editor.js — fábrica del editor de código (CodeMirror 6) usado en libro, playground
// y ejercicios. Autocompletado Python rico, indentación de 4 espacios, cierre de
// brackets, y atajo Ctrl/Cmd+Enter para correr.
import { basicSetup } from 'codemirror';
import { EditorView, keymap } from '@codemirror/view';
import { indentWithTab } from '@codemirror/commands';
import { python } from '@codemirror/lang-python';
import { oneDark } from '@codemirror/theme-one-dark';
import { indentUnit } from '@codemirror/language';
import { snippetCompletion as snip } from '@codemirror/autocomplete';

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

// Crea el editor. opts: { doc, parent, onRun, onChange, extra }
export function editorPython({ doc = '', parent, onRun, onChange, extra = [] } = {}) {
  const py = python();
  const ext = [
    basicSetup,
    py,
    py.language.data.of({ autocomplete: fuentePython }),
    oneDark,
    indentUnit.of('    '),
    keymap.of([indentWithTab]),
  ];
  if (onRun) ext.push(keymap.of([{ key: 'Mod-Enter', preventDefault: true, run: () => { onRun(); return true; } }]));
  if (onChange) ext.push(EditorView.updateListener.of((v) => { if (v.docChanged) onChange(v.state.doc.toString()); }));
  ext.push(...extra);
  return new EditorView({ doc, parent, extensions: ext });
}
