// errores.js — traduce errores de Python (Pyodide) a mensajes claros en español + causa y arreglo,
// y arma pistas a partir de los fallos de los tests. Pensado para principiantes absolutos.

const TIPOS = {
  SyntaxError:       { ico: '✏️', titulo: 'Error de sintaxis', causa: 'Python no entendió cómo está escrita una línea.', fix: 'Revisá comillas y paréntesis que abren y cierran, y los dos puntos `:` al final de `if`, `for`, `while`, `def`.' },
  IndentationError:  { ico: '📐', titulo: 'Error de indentación', causa: 'La sangría (los espacios al principio de la línea) no está bien.', fix: 'Lo que va “adentro” de un `if`/`for`/`def` lleva 4 espacios. No mezcles tabs con espacios.' },
  TabError:          { ico: '📐', titulo: 'Tabs y espacios mezclados', causa: 'Mezclaste tabulaciones con espacios en la sangría.', fix: 'Usá siempre 4 espacios (configurá tu editor para que el Tab inserte espacios).' },
  NameError:         { ico: '🔤', titulo: 'Nombre no definido', causa: 'Usaste una variable o función que Python no conoce.', fix: '¿La escribiste distinto (mayúsculas/typo)? ¿La definiste ANTES de usarla?' },
  TypeError:         { ico: '🧩', titulo: 'Error de tipo', causa: 'Hiciste una operación entre tipos que no se llevan (ej. sumar texto con número) o pasaste mal los argumentos.', fix: 'Convertí los tipos (`int(...)`, `str(...)`) o revisá cuántos/qué argumentos pasás.' },
  ValueError:        { ico: '🔢', titulo: 'Valor inválido', causa: 'El valor no sirve para esa operación (ej. `int("hola")`).', fix: 'Revisá que el valor tenga el formato esperado antes de convertirlo o usarlo.' },
  IndexError:        { ico: '📏', titulo: 'Índice fuera de rango', causa: 'Pediste una posición que no existe en la lista o el texto.', fix: 'Acordate: la primera posición es `0` y la última es `len(x) - 1`.' },
  KeyError:          { ico: '🗝️', titulo: 'Clave inexistente', causa: 'Buscaste una clave que no está en el diccionario.', fix: 'Verificá el nombre de la clave, o usá `mi_dict.get(clave)` para no romper.' },
  ZeroDivisionError: { ico: '➗', titulo: 'División por cero', causa: 'Dividiste por 0.', fix: 'Asegurate de que el divisor no sea 0 antes de dividir.' },
  AttributeError:    { ico: '🔗', titulo: 'Método o atributo inexistente', causa: 'Usaste un método o atributo que ese objeto no tiene.', fix: 'Revisá el nombre del método y el tipo del objeto (¿es lista, texto, diccionario?).' },
  ModuleNotFoundError: { ico: '📦', titulo: 'Módulo no encontrado', causa: 'Importaste un módulo que no está disponible.', fix: 'Revisá el nombre del `import`.' },
  ImportError:       { ico: '📦', titulo: 'Error al importar', causa: 'No se pudo importar lo que pediste.', fix: 'Revisá el nombre del módulo o de lo que importás de él.' },
  RecursionError:    { ico: '🌀', titulo: 'Demasiada recursión', causa: 'Una función se llama a sí misma sin frenar nunca.', fix: 'Agregá un caso base que corte la recursión (un `return` sin volver a llamarse).' },
  FileNotFoundError: { ico: '📄', titulo: 'Archivo no encontrado', causa: 'Intentaste abrir un archivo que no existe en esa ruta.', fix: 'Revisá el nombre y la ruta del archivo (¿está bien escrito? ¿existe?).' },
  AssertionError:    { ico: '❗', titulo: 'Afirmación fallida', causa: 'Un `assert` comprobó algo que resultó falso.', fix: 'El valor no era el que esperaba esa comprobación.' },
};
const cap = (s, n = 60) => { s = String(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; };

// refina la causa/fix según el detalle del error (mensajes típicos de CPython).
function refinar(tipo, detalle, base) {
  const d = (detalle || '').toLowerCase();
  const ent = (re) => (detalle.match(re) || [])[1];

  if (tipo === 'NameError') {
    const n = ent(/name '([^']+)'/);
    if (n) return { ...base, causa: `Usaste «${n}» pero Python no sabe qué es.`, fix: `¿«${n}» está bien escrito (mayúsculas/typo)? ¿Lo definiste (con \`=\` o \`def\`) ANTES de esta línea? ¿Falta un \`import\`?` };
  }
  if (tipo === 'SyntaxError') {
    if (d.includes("expected ':'")) return { ...base, fix: 'Falta el `:` al final de la línea (después del `if`, `for`, `while`, `def`, etc.).' };
    if (d.includes('print')) return { ...base, causa: 'En Python 3, `print` es una función.', fix: 'Va con paréntesis: `print("hola")` (no `print "hola"`).' };
    if (d.includes('unterminated string') || d.includes('eol while scanning')) return { ...base, fix: 'Quedó una comilla sin cerrar. Cada `"` o `\'` que abre tiene que cerrar.' };
    if (d.includes('unexpected eof') || d.includes('was never closed')) return { ...base, fix: 'Quedó un paréntesis `(`, corchete `[` o llave `{` sin cerrar.' };
    if (d.includes('cannot assign')) return { ...base, fix: 'Para comparar se usa `==` (doble); un solo `=` asigna, y no se puede asignar a eso.' };
    if (d.includes('invalid syntax')) return { ...base, fix: 'Revisá la línea: ¿falta un `:`, una coma, un paréntesis, o usaste `=` donde va `==`?' };
  }
  if (tipo === 'IndentationError') {
    if (d.includes('unexpected indent')) return { ...base, fix: 'Hay espacios de más al principio de esa línea. Alineala con las de su mismo bloque.' };
    if (d.includes('expected an indented block')) return { ...base, fix: 'Después de un `:` (de `if`/`for`/`def`…) la línea siguiente va con 4 espacios de sangría.' };
  }
  if (tipo === 'TypeError') {
    if (d.includes('not callable')) return { ...base, causa: 'Usaste `()` sobre algo que no es una función.', fix: '¿Le pusiste el mismo nombre a una variable y a una función? Revisá los nombres.' };
    if (d.includes('not iterable')) return { ...base, causa: 'Intentaste recorrer (`for`) o desempaquetar algo que no es una colección.', fix: 'Eso no es una lista/tupla/texto. Revisá qué le pasás al `for`.' };
    if (d.includes('not subscriptable')) return { ...base, causa: 'Usaste `[...]` sobre algo que no es lista/dict/texto.', fix: 'Quizás esa variable es un número o `None` y no se puede indexar.' };
    if (d.includes('concatenate') || (d.includes('unsupported operand') && (d.includes('str') || d.includes('int') || d.includes('float')))) {
      return { ...base, causa: 'Mezclaste texto y número en una misma operación.', fix: 'Convertí: `str(numero)` para unir con texto, o `int(texto)` para sumar como número.' };
    }
    if (d.includes('argument')) return { ...base, causa: 'Llamaste a una función con más/menos argumentos de los que espera.', fix: 'Fijate cuántos parámetros tiene la función y pasale exactamente esos.' };
  }
  if (tipo === 'ValueError') {
    const n = ent(/int\(\) with base 10: '([^']*)'/);
    if (n != null) return { ...base, causa: `Intentaste convertir a número algo que no lo es ("${n}").`, fix: '`int(...)` solo convierte textos que sean números (ej. `"42"`). Revisá el valor.' };
  }
  if (tipo === 'KeyError') {
    const k = ent(/'([^']+)'/) || (detalle || '').trim();
    if (k) return { ...base, causa: `No existe la clave «${k}» en el diccionario.`, fix: `Revisá el nombre de la clave, o usá \`mi_dict.get("${k}")\` para no romper.` };
  }
  if (tipo === 'AttributeError') {
    const attr = ent(/attribute '([^']+)'/);
    const obj = ent(/'([A-Za-z_.]+)' object/);
    if (obj === 'NoneType') return { ...base, causa: 'La variable vale `None`.', fix: 'Quizás una función no devolvió nada (le falta `return`). Revisá de dónde sale ese valor.' };
    if (attr) return { ...base, causa: `Ese ${obj ? '`' + obj + '`' : 'objeto'} no tiene «${attr}».`, fix: `Revisá cómo se escribe «${attr}» y el tipo del objeto (¿lista, texto, dict?).` };
  }
  if (tipo === 'ModuleNotFoundError' || tipo === 'ImportError') {
    const m = ent(/named '([^']+)'/) || ent(/'([^']+)'/);
    if (m) return { ...base, causa: `No se encontró el módulo «${m}».`, fix: `Revisá que «${m}» esté bien escrito.` };
  }
  if (tipo === 'FileNotFoundError') {
    const f = ent(/'([^']+)'/);
    if (f) return { ...base, causa: `No se encontró el archivo «${f}».`, fix: 'Revisá el nombre y la ruta (¿existe? ¿está bien escrito?).' };
  }
  return base;
}

// Traduce un traceback o mensaje de error de Python. Devuelve {ico,titulo,causa,fix,linea,tipo,detalle} o null.
export function traducirError(raw) {
  if (!raw) return null;
  const txt = String(raw);
  const matches = [...txt.matchAll(/([A-Za-z_]*(?:Error|Exception|Warning))(?:\s*:\s*([^\n]*))?/g)];
  if (!matches.length) return null;
  const last = matches[matches.length - 1];
  const tipo = last[1];
  const detalle = (last[2] || '').trim();
  const base = TIPOS[tipo] || { ico: '⚠️', titulo: tipo, causa: 'Ocurrió un error al ejecutar.', fix: 'Leé el detalle y revisá la línea indicada.' };
  const linea = (txt.match(/line (\d+)/) ? Number(txt.match(/line (\d+)/)[1]) : null);
  return { ...refinar(tipo, detalle, base), tipo, detalle, linea };
}

// ¿el texto parece un error/traceback de Python? (para decidir si traducir la salida de ▶ Ejecutar)
export const pareceError = (txt) => /Traceback \(most recent call last\)|[A-Za-z_]*(?:Error|Exception)\s*:/.test(String(txt || ''));

// Pista a partir del mensaje de un test fallido (pytest). No revela la solución.
export function pistaTest(msg) {
  if (!msg) return '';
  // pytest a veces antepone "AssertionError:" a la comparación reescrita → lo sacamos para leer los valores.
  const t = msg.trim().replace(/^AssertionError:\s*/, '');
  // pytest.raises esperaba un error que tu código NO lanzó ('DID NOT RAISE <class 'ValueError'>')
  let nr = t.match(/DID NOT RAISE\s+<class '([^']+)'>/) || t.match(/DID NOT RAISE\s+(\w+)/);
  if (nr) return `Se esperaba que tu código lanzara un error (${nr[1].split('.').pop()}), pero no lanzó ninguno.`;
  // si el test reventó por una excepción (no un assert), traducir el error
  if (!/^assert\b/.test(t) && pareceError(t)) {
    const e = traducirError(t);
    if (e) return `${e.titulo}: ${e.causa}`;
  }
  let m = t.match(/^assert\s+(.+?)\s*==\s*(.+)$/s);
  if (m) return `Se esperaba ${cap(m[2])} pero tu código devolvió ${cap(m[1])}.`;
  m = t.match(/^assert\s+(.+?)\s*!=\s*(.+)$/s);
  if (m) return `Tu resultado no debería ser igual a ${cap(m[2])}.`;
  m = t.match(/^assert\s+(.+?)\s*(<=|>=|<|>)\s*(.+)$/s);
  if (m) return `Se esperaba que ${cap(m[1])} fuera ${m[2]} ${cap(m[3])}.`;
  m = t.match(/^assert\s+(.+?)\s+in\s+(.+)$/s);
  if (m) return `Se esperaba encontrar ${cap(m[1])} dentro de ${cap(m[2])}.`;
  // X is True / is False / is None  (pytest reescribe a 'assert <valor> is True')
  m = t.match(/^assert\s+(.+?)\s+is\s+(not\s+)?(True|False|None)$/s);
  if (m) {
    if (m[3] === 'None') return m[2]
      ? `Se esperaba un valor, pero tu código devolvió None (no devolvió nada).`
      : `Se esperaba None (es decir, nada) pero tu código devolvió ${cap(m[1])}.`;
    const esp = m[2] ? (m[3] === 'True' ? 'False' : 'True') : m[3];
    return `Se esperaba ${esp} pero tu código devolvió ${cap(m[1])}.`;
  }
  if (/^assert\b/.test(t)) return `No se cumplió una condición esperada (${cap(t.replace(/^assert\s+/, ''), 80)}).`;
  return t;
}
