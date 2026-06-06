// reporte-errores.js — captura errores JS no atrapados (y promesas rechazadas) en el navegador del
// alumno y los manda a la API (POST /errores, público) para tener visibilidad en producción.
// A prueba de spam: deduplica y corta a 15 por sesión. Si no hay API, no hace nada.
const BASE = (import.meta.env.PUBLIC_API_URL || '').replace(/\/+$/, '');
let enviados = 0;
const vistos = new Set();

function reportar(tipo, mensaje, stack) {
  if (!BASE || enviados >= 15) return;
  const clave = tipo + '|' + String(mensaje || '').slice(0, 100);
  if (vistos.has(clave)) return;
  vistos.add(clave);
  enviados += 1;
  let handle = '';
  try { handle = localStorage.getItem('liga:nombre') || ''; } catch {}
  const body = JSON.stringify({
    tipo,
    mensaje: String(mensaje || '').slice(0, 500),
    stack: String(stack || '').slice(0, 2000),
    url: location.href,
    ua: navigator.userAgent,
    handle,
  });
  try {
    // keepalive: sobrevive a la navegación/cierre, como sendBeacon, pero con JSON + CORS limpio
    fetch(BASE + '/errores', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body, keepalive: true, mode: 'cors' }).catch(() => {});
  } catch {}
}

export function iniciarReporteErrores() {
  if (!BASE) return;
  window.addEventListener('error', (e) => {
    // "Script error." = error de un script de otro origen (sin detalle): no sirve reportarlo
    if (!e || !e.message || /script error/i.test(e.message)) return;
    reportar('error', e.message + (e.filename ? ' (' + e.filename + ':' + e.lineno + ')' : ''), e.error && e.error.stack);
  });
  window.addEventListener('unhandledrejection', (e) => {
    const r = e && e.reason;
    reportar('promise', (r && r.message) || String(r), r && r.stack);
  });
}
