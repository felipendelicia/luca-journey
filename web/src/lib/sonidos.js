// sonidos.js — efectos 8-bit generados con Web Audio (sin archivos).
let ctx;
function ac() {
  if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}
const muteado = () => localStorage.getItem('sonido:off') === '1';

function tono(freq, start, dur, tipo = 'square', vol = 0.14) {
  const c = ac();
  const o = c.createOscillator();
  const g = c.createGain();
  o.type = tipo;
  o.frequency.value = freq;
  const t0 = c.currentTime + start;
  g.gain.setValueAtTime(vol, t0);
  g.gain.exponentialRampToValueAtTime(0.0008, t0 + dur);
  o.connect(g);
  g.connect(c.destination);
  o.start(t0);
  o.stop(t0 + dur);
}
function tocar(notas, tipo = 'square') {
  if (muteado()) return;
  try { notas.forEach(([f, t, d]) => tono(f, t, d, tipo)); } catch {}
}

export const sonarCaptura = () => tocar([[523, 0, 0.1], [659, 0.1, 0.1], [784, 0.2, 0.16]]);          // do-mi-sol
export const sonarShiny = () => tocar([[988, 0, 0.08], [1319, 0.09, 0.08], [1568, 0.18, 0.08], [2093, 0.27, 0.25]]);
// fanfarria épica/legendaria: arpegio ascendente + nota final sostenida (tiers altos)
export const sonarEpico = () => tocar([[392, 0, 0.13], [523, 0.13, 0.13], [659, 0.26, 0.13], [784, 0.39, 0.13], [1047, 0.52, 0.45]]);
export const sonarExito = () => tocar([[659, 0, 0.09], [784, 0.09, 0.09], [1047, 0.18, 0.22]]);
export const sonarError = () => tocar([[196, 0, 0.22], [165, 0.12, 0.26]], 'sawtooth');
export const sonarClick = () => tocar([[880, 0, 0.05]]);

export const sonidoActivo = () => !muteado();
export function toggleSonido() {
  const nuevo = muteado();          // si estaba muteado, lo activamos
  localStorage.setItem('sonido:off', nuevo ? '0' : '1');
  if (nuevo) sonarClick();
  return nuevo;
}
