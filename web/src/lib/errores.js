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

};
const cap = (s, n = 60) => { s = String(s); return s.length > n ? s.slice(0, n - 1) + '…' : s; };

// refina el `fix` según el detalle del error (mensajes típicos de CPython).
function refinar(tipo, detalle, base) {
  const d = (detalle || '').toLowerCase();
  if (tipo === 'NameError') {
    const n = (detalle.match(/name '([^']+)'/) || [])[1];
    if (n) return { ...base, causa: `Usaste «${n}» pero Python no sabe qué es.`, fix: `¿«${n}» está bien escrito? ¿Lo definiste (con \`=\` o \`def\`) antes de esta línea?` };
  }
  if (tipo === 'SyntaxError') {
    if (d.includes('expected \':\'')) return { ...base, fix: 'Falta el `:` al final de la línea (después del `if`, `for`, `while`, `def`, etc.).' };
    if (d.includes('unterminated string')) return { ...base, fix: 'Quedó una comilla sin cerrar. Cada `"` o `\'` que abre tiene que cerrar.' };
    if (d.includes('unexpected eof') || d.includes('was never closed')) return { ...base, fix: 'Quedó un paréntesis/corchete/llave sin cerrar.' };
    if (d.includes('invalid syntax') && d.includes('=')) return { ...base, fix: 'Para comparar se usa `==` (doble). Un solo `=` es asignar.' };
  }
  if (tipo === 'IndentationError' && d.includes('expected an indented block')) {
    return { ...base, fix: 'Después de un `:` (de `if`/`for`/`def`…) la línea siguiente tiene que ir con 4 espacios de sangría.' };
  }
  if (tipo === 'TypeError') {
    if (d.includes('positional argument')) return { ...base, causa: 'Llamaste a una función con más/menos argumentos de los que espera.', fix: 'Fijate cuántos parámetros tiene la función y pasale exactamente esos.' };
    if (d.includes('not subscriptable')) return { ...base, causa: 'Usaste `[...]` sobre algo que no es lista/dict/texto.', fix: 'Revisá la variable: quizás es un número o None y no se puede indexar.' };
  }
  return base;
}

// Traduce un traceback o mensaje de error de Python. Devuelve {ico,titulo,causa,fix,linea,tipo,detalle} o null.
export function traducirError(raw) {
  if (!raw) return null;
  const txt = String(raw);
  const matches = [...txt.matchAll(/([A-Za-z_]*(?:Error|Exception|Warning))\s*:\s*([^\n]*)/g)];
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
  const t = msg.trim();
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
  if (/^assert\b/.test(t)) return `No se cumplió una condición esperada (${cap(t.replace(/^assert\s+/, ''), 80)}).`;
  return t;
}
