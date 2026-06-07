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

// Extrae la imagen de matplotlib (si hay figura) como PNG base64.
const PLOT_B64 = "import io,base64,matplotlib.pyplot as _p\n_b=''\nif _p.get_fignums():\n    _f=io.BytesIO(); _p.gcf().savefig(_f,format='png',bbox_inches='tight',dpi=110); _p.close('all'); _b=base64.b64encode(_f.getvalue()).decode()\n_b";

self.onmessage = async (evt) => {
  const { id, helperSrc, packages, fn, args, code, stream, syntax } = evt.data;

  // Chequeo de SINTAXIS (linter inline): compila sin ejecutar. NO fuerza la carga de Pyodide:
  // si todavía no está caliente, devuelve null (no marca nada hasta que el warm-up termine).
  if (syntax) {
    if (!pyodide) { self.postMessage({ id, ok: true, result: null }); return; }
    try {
      pyodide.globals.set('_src_chk', code || '');
      const r = pyodide.runPython(
        "import json as _j\n" +
        "def _chk(s):\n" +
        "    try:\n" +
        "        compile(s, '<editor>', 'exec'); return None\n" +
        "    except SyntaxError as e:\n" +
        "        return _j.dumps({'lineno': e.lineno, 'offset': e.offset, 'end_lineno': getattr(e,'end_lineno',None), 'end_offset': getattr(e,'end_offset',None), 'msg': e.msg or '', 'type': type(e).__name__})\n" +
        "    except Exception:\n" +
        "        return None\n" +
        "_chk(_src_chk)"
      );
      self.postMessage({ id, ok: true, result: r || null });
    } catch (e) {
      self.postMessage({ id, ok: true, result: null });
    }
    return;
  }

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

    // Modo streaming (▶ del libro): corre `code` con stdout/stderr en vivo (postMessage por chunk),
    // sin input interactivo (eso queda en main thread). Devuelve la imagen matplotlib si la hay.
    if (stream) {
      pyodide.setStdout({ batched: (s) => self.postMessage({ id, chunk: s + '\n' }) });
      pyodide.setStderr({ batched: (s) => self.postMessage({ id, chunk: s + '\n', err: true }) });
      pyodide.setStdin({ stdin: () => '' });
      const usaPlot = /\bmatplotlib\b|\bplt\./.test(code);
      try {
        if (usaPlot) await pyodide.runPythonAsync("import matplotlib; matplotlib.use('AGG')");
        await pyodide.runPythonAsync(code);
        const img = usaPlot ? await pyodide.runPythonAsync(PLOT_B64) : '';
        self.postMessage({ id, ok: true, result: img });
      } finally {
        pyodide.setStdout({}); pyodide.setStderr({});
      }
      return;
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
