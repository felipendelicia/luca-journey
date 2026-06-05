/* py-worker.js — Pyodide runner en Web Worker con soporte de timeout desde el main thread.
   Protocolo de entrada:  { id, helperSrc, packages, fn, args }
   Protocolo de salida:   { id, ok: true,  result }
                       o  { id, ok: false, error }
*/
importScripts('https://cdn.jsdelivr.net/pyodide/v0.26.4/full/pyodide.js');

let pyodide = null;
// Set de hashes de helperSrc ya ejecutados para no re-ejecutar en cada llamada.
const executedHelpers = new Set();
// Paquetes ya cargados.
const loadedPackages = new Set();

function simpleHash(str) {
  // Hash rápido (djb2) para identificar helpers ya ejecutados.
  let h = 5381;
  for (let i = 0; i < str.length; i++) {
    h = ((h << 5) + h) + str.charCodeAt(i);
    h |= 0;
  }
  return h.toString(36);
}

async function ensurePyodide() {
  if (!pyodide) {
    pyodide = await loadPyodide();
  }
  return pyodide;
}

async function ensurePackages(packages) {
  const needed = (packages || []).filter((p) => !loadedPackages.has(p));
  if (needed.length) {
    await pyodide.loadPackage(needed);
    needed.forEach((p) => loadedPackages.add(p));
  }
}

self.onmessage = async (evt) => {
  const { id, helperSrc, packages, fn, args } = evt.data;
  try {
    await ensurePyodide();
    await ensurePackages(packages);

    // Ejecutar helperSrc sólo si no lo vimos antes.
    if (helperSrc) {
      const key = simpleHash(helperSrc);
      if (!executedHelpers.has(key)) {
        await pyodide.runPythonAsync(helperSrc);
        executedHelpers.add(key);
      }
    }

    // Setear argumentos como globals _a0, _a1, ...
    const argNames = (args || []).map((_, i) => '_a' + i);
    (args || []).forEach((val, i) => {
      pyodide.globals.set('_a' + i, val);
    });

    // Construir llamada: fn(_a0, _a1, ...)
    const call = fn + '(' + argNames.join(', ') + ')';
    const result = await pyodide.runPythonAsync(call);

    self.postMessage({ id, ok: true, result });
  } catch (e) {
    self.postMessage({ id, ok: false, error: String(e) });
  }
};
