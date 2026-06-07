/* pyrun.js — wrapper main-thread para py-worker.js.
   Crea el worker lazy y lo recrea si fue terminado por timeout.

   export function run(helperSrc, packages, fn, args, timeoutMs = 10000): Promise<string>
*/

let worker = null;
let pendingMap = new Map(); // id → { resolve, reject, timer }
let nextId = 1;

function getWorker() {
  if (!worker) {
    const base = (typeof window !== 'undefined' && window.__BASE) ? window.__BASE : '/';
    const url = base.replace(/\/$/, '') + '/py-worker.js';
    worker = new Worker(url);
    worker.onmessage = (evt) => {
      const { id, ok, result, error, chunk, err } = evt.data;
      const pending = pendingMap.get(id);
      if (!pending) return;
      if (chunk !== undefined) { if (pending.onChunk) pending.onChunk(chunk, err); return; }  // streaming: no resuelve aún
      clearTimeout(pending.timer);
      pendingMap.delete(id);
      if (ok) {
        pending.resolve(result);
      } else {
        pending.reject(new Error(error));
      }
    };
    worker.onerror = (evt) => {
      // Errores no capturados en el worker: rechazamos todos los pendientes.
      const err = new Error(evt.message || 'Error en el worker de Python.');
      for (const [, pending] of pendingMap) {
        clearTimeout(pending.timer);
        pending.reject(err);
      }
      pendingMap.clear();
      worker = null;
    };
  }
  return worker;
}

/**
 * Corre una función Python en el worker.
 * @param {string} helperSrc  - Código Python que define las funciones (se ejecuta una vez por hash).
 * @param {string[]} packages - Paquetes Pyodide adicionales a cargar.
 * @param {string} fn         - Nombre de la función Python a llamar.
 * @param {string[]} args     - Argumentos string para la función.
 * @param {number} timeoutMs  - Timeout en ms (default 10 s).
 * @returns {Promise<string>} - El JSON string devuelto por la función Python.
 */
// Timeout: termina el worker (única forma de cortar un bucle infinito) y rechaza los pendientes.
function makeTimer(timeoutMs) {
  return setTimeout(() => {
    if (worker) { worker.terminate(); worker = null; }
    for (const [, pending] of pendingMap) {
      pending.reject(new Error('⏱️ Tu código tardó demasiado (¿bucle infinito? ej. un while sin fin).'));
    }
    pendingMap.clear();
  }, timeoutMs);
}

export function run(helperSrc, packages, fn, args, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    const w = getWorker();
    const timer = makeTimer(timeoutMs);
    pendingMap.set(id, { resolve, reject, timer });
    w.postMessage({ id, helperSrc, packages, fn, args });
  });
}

/**
 * Corre `code` con stdout/stderr en vivo (modo streaming). onChunk(texto, esError) recibe cada
 * fragmento impreso. Resuelve con el resultado final (ej. imagen matplotlib base64 o '').
 */
export function runStream(helperSrc, packages, code, onChunk, timeoutMs = 10000) {
  return new Promise((resolve, reject) => {
    const id = nextId++;
    const w = getWorker();
    const timer = makeTimer(timeoutMs);
    pendingMap.set(id, { resolve, reject, timer, onChunk });
    w.postMessage({ id, helperSrc, packages, code, stream: true });
  });
}

/**
 * Chequeo de SINTAXIS para el linter inline: compila `code` (sin ejecutar) y devuelve el detalle del
 * SyntaxError (`{lineno, offset, end_lineno, end_offset, msg, type}`) o `null` si compila o si Pyodide
 * todavía no está caliente. Timeout corto que NO termina el worker (no es un bucle infinito).
 * @returns {Promise<object|null>}
 */
export function checkSintaxis(code) {
  return new Promise((resolve) => {
    const id = nextId++;
    let w;
    try { w = getWorker(); } catch { return resolve(null); }
    const timer = setTimeout(() => { pendingMap.delete(id); resolve(null); }, 5000);
    pendingMap.set(id, {
      resolve: (r) => { try { resolve(r ? JSON.parse(r) : null); } catch { resolve(null); } },
      reject: () => resolve(null),
      timer,
    });
    w.postMessage({ id, syntax: true, code });
  });
}
