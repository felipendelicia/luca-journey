// runner-py.js — runner unificado para ejercicios y proyectos: corre runner.py (pytest) en el
// Web Worker (pyrun.js) con warm-up y timeout. Un bucle infinito termina el worker (no congela).
import { run } from './pyrun.js';

// Paquetes Pyodide para pytest (+ micropip si el tema usa flask).
export function paquetesPytest(dataPackages) {
  const pkgs = dataPackages || [];
  const flask = pkgs.includes('flask');
  return { packages: ['pytest', ...(flask ? ['micropip'] : []), ...pkgs.filter((p) => p !== 'flask')], flask };
}

/**
 * Crea un runner ligado a un helper (runner.py) y sus paquetes.
 * @returns {{ asegurar: ()=>Promise, correr: (...args)=>Promise<string>, ejecutar: (code)=>Promise<string> }}
 */
export function crearRunnerPytest(runnerSrc, dataPackages, timeoutMs = 10000) {
  const { packages, flask } = paquetesPytest(dataPackages);
  const helper = flask ? "import micropip\nawait micropip.install('flask')\n\n" + runnerSrc : runnerSrc;
  let listo = null;
  // Asegura el worker cargado (Pyodide + pytest + helper) con timeout amplio para la 1ra carga (~20s).
  // Se resetea si el worker muere por timeout.
  function asegurar() {
    if (!listo) listo = run(helper, packages, 'ejecutar', [''], 60000).catch((e) => { listo = null; throw e; });
    return listo;
  }
  return {
    asegurar,
    async correr(slug, ej, test, extra, solo) {
      await asegurar();
      return run(helper, packages, 'correr', [slug, ej, test, extra, solo], timeoutMs);
    },
    async ejecutar(code) {
      await asegurar();
      return run(helper, packages, 'ejecutar', [code], timeoutMs);
    },
  };
}
