// correr-ui.js — render compartido de resultados del runner (ejercicios y proyectos usan lo mismo):
// errores traducidos a español (causa + arreglo), pistas de tests, y salida del botón ▶ Ejecutar.
import { traducirError, pistaTest, pareceError } from './errores.js';

const esc = (s) => String(s == null ? '' : s).replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

// Bloque de error amigable: título + causa + cómo arreglarlo + traceback técnico colapsable.
// El mensaje de timeout (⏱️) se muestra tal cual.
export function bloqueError(raw) {
  if (/⏱️|tardó demasiado/.test(raw)) return '<div class="ejer-err">' + esc(raw) + '</div>';
  const e = traducirError(raw);
  if (!e) return '<div class="ejer-err">⚠️ El código no se pudo ejecutar:<br><code>' + esc(raw) + '</code></div>';
  return '<div class="ejer-err err-amigable">'
    + '<div class="err-tit">' + e.ico + ' ' + esc(e.titulo) + (e.linea ? ' <span class="err-linea">línea ' + e.linea + '</span>' : '') + '</div>'
    + '<div class="err-causa">' + esc(e.causa) + '</div>'
    + '<div class="err-fix">💡 ' + esc(e.fix) + '</div>'
    + '<details class="err-raw"><summary>Ver el error técnico</summary><code>' + esc(raw) + '</code></details>'
    + '</div>';
}

// Lista <ul> de resultados de tests, con pista amigable (pistaTest) + detalle técnico colapsable.
export function listaTests(tests) {
  let h = '<ul class="ejer-lista">';
  for (const t of tests) {
    h += '<li class="' + (t.ok ? 'ok' : 'no') + '"><span class="ic">' + (t.ok ? '✅' : '❌') + '</span><code>' + esc(t.name) + '</code>';
    if (t.msg) {
      const p = pistaTest(t.msg);
      h += '<div class="m">💡 ' + esc(p) + '</div>';
      if (p !== t.msg) h += '<details class="m-raw"><summary>detalle del test</summary><code>' + esc(t.msg) + '</code></details>';
    }
    if (t.out) h += '<div class="ej-out"><span class="lbl">🖨️ tus prints</span>' + esc(t.out) + '</div>';
    h += '</li>';
  }
  return h + '</ul>';
}

// HTML de la salida del botón ▶ Ejecutar (stdout / valor de retorno / error traducido).
export function salidaEjecutar(res) {
  let h = '<div class="ejer-run"><span class="lbl">▶ Ejecutar</span>';
  if (res.out && pareceError(res.out)) h += bloqueError(res.out);
  else if (res.out) h += '<pre class="ej-stdout">' + esc(res.out) + '</pre>';
  const tieneRet = res.ret !== null && res.ret !== undefined;
  if (tieneRet) h += '<div class="ej-ret">↩ devuelve <code>' + esc(res.ret) + '</code></div>';
  if (!res.out && !tieneRet) h += '<div class="ej-vacio">Sin salida. Agregá <code>print(...)</code> o poné una llamada como última línea para ver qué devuelve.</div>';
  return h + '</div>';
}
