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
  if (nuevo) sonarClick(); else detenerMusica();   // si se mutea, cortar la música en curso
  return nuevo;
}

// ───────── música (osciladores rastreados para poder cortarla) ─────────
let musNodos = [];
let musLoop = null;
// agenda una nota de música con attack/decay; la registra para poder detenerla.
function nota(freq, start, dur, tipo = 'square', vol = 0.12) {
  const c = ac();
  const o = c.createOscillator(); const g = c.createGain();
  o.type = tipo; o.frequency.value = freq;
  const t0 = c.currentTime + start;
  g.gain.setValueAtTime(0.0001, t0);
  g.gain.exponentialRampToValueAtTime(vol, t0 + 0.02);
  g.gain.exponentialRampToValueAtTime(0.0008, t0 + dur);
  o.connect(g); g.connect(c.destination);
  o.start(t0); o.stop(t0 + dur);
  musNodos.push(o);
  o.onended = () => { musNodos = musNodos.filter((x) => x !== o); };
}
export function detenerMusica() {
  if (musLoop) { clearTimeout(musLoop); musLoop = null; }
  for (const o of musNodos) { try { o.stop(); } catch {} }
  musNodos = [];
}

// Tema ÉPICO de evolución (~5s): bajo pulsante + melodía ascendente que crece hasta el clímax
// (~4.5s, coincide con el reveal). One-shot.
export function musicaEvolucion() {
  if (muteado()) return;
  detenerMusica();
  try {
    const bass = [110, 110, 123, 131, 131, 147, 165, 175, 196, 220];   // tensión que sube
    bass.forEach((f, i) => nota(f, i * 0.5, 0.46, 'triangle', 0.11));
    const mel = [
      [330, 0.0, 0.42], [392, 0.5, 0.42], [440, 1.0, 0.42], [392, 1.5, 0.42],
      [440, 2.0, 0.42], [523, 2.5, 0.42], [587, 3.0, 0.42], [659, 3.5, 0.46], [698, 4.0, 0.42],
      [784, 4.5, 0.9],   // CLÍMAX (reveal)
    ];
    mel.forEach(([f, t, d]) => nota(f, t, d, 'square', 0.13));
    [[1047, 4.5, 0.6], [1319, 4.8, 0.7], [1568, 5.05, 0.5]].forEach(([f, t, d]) => nota(f, t, d, 'square', 0.09));  // brillo del clímax
  } catch {}
}

// Música de fondo de BATALLA: loop chiptune (bajo + melodía) que se reagenda solo. (F4)
const BATALLA_BASE = [
  // [freq, beat, dur] melodía; el bajo se deriva. Compás ~ 8s, vibe heroico 8-bit.
  [440, 0, 0.5], [523, 0.5, 0.5], [659, 1.0, 0.5], [587, 1.5, 0.5],
  [523, 2.0, 0.5], [440, 2.5, 0.5], [494, 3.0, 0.5], [523, 3.5, 0.5],
  [587, 4.0, 0.5], [659, 4.5, 0.5], [698, 5.0, 0.5], [784, 5.5, 0.5],
  [659, 6.0, 0.5], [587, 6.5, 0.5], [523, 7.0, 0.5], [494, 7.5, 0.5],
];
const BATALLA_BAJO = [220, 165, 196, 247];   // un grave por cada 2 beats
function loopBatalla() {
  if (muteado()) { musLoop = null; return; }
  const LARGO = 8;
  BATALLA_BASE.forEach(([f, t, d]) => nota(f, t, d, 'square', 0.06));
  for (let i = 0; i < LARGO; i++) nota(BATALLA_BAJO[(i / 2 | 0) % BATALLA_BAJO.length], i, 0.9, 'triangle', 0.05);
  musLoop = setTimeout(loopBatalla, LARGO * 1000 - 60);
}
export function musicaBatalla() { if (muteado()) return; detenerMusica(); try { loopBatalla(); } catch {} }
