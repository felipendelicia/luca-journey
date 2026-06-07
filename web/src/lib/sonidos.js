// sonidos.js — efectos 8-bit generados con Web Audio (sin archivos).
let ctx;
function ac() {
  if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
  if (ctx.state === 'suspended') ctx.resume();
  return ctx;
}
// ───────── volumen maestro (0..1) — lo controla el slider del botón de la navbar ─────────
export const volumen = () => {
  try {
    const v = localStorage.getItem('sonido:vol');
    if (v != null) return Math.max(0, Math.min(1, parseFloat(v) || 0));
    return localStorage.getItem('sonido:off') === '1' ? 0 : 0.8;   // migración del flag viejo
  } catch { return 0.8; }
};
const muteado = () => volumen() <= 0;
let _master = null;
// bus maestro: TODO el synth pasa por acá, así el slider escala todo de una.
function bus() {
  const c = ac();
  if (!_master) { _master = c.createGain(); _master.gain.value = volumen(); _master.connect(c.destination); }
  return _master;
}
export function setVolumen(v) {
  v = Math.max(0, Math.min(1, Number(v) || 0));
  try { localStorage.setItem('sonido:vol', String(v)); localStorage.setItem('sonido:off', v <= 0 ? '1' : '0'); } catch {}
  if (_master) _master.gain.value = v;
  if (v <= 0) detenerMusica();
  // avisar a la navbar (icono + slider) y a cualquier listener que el volumen cambió.
  try { window.dispatchEvent(new CustomEvent('sonido:cambio', { detail: { vol: v } })); } catch {}
}
// el slider de la navbar (otro script) avisa por evento → actualizamos el bus en vivo.
if (typeof window !== 'undefined') window.addEventListener('sonido:cambio', () => { if (_master) _master.gain.value = volumen(); if (volumen() <= 0) detenerMusica(); });

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
  g.connect(bus());
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
  const activar = muteado();        // si estaba en 0, lo activamos al último volumen
  if (activar) { let prev = parseFloat(localStorage.getItem('sonido:volPrev')); if (!(prev > 0)) prev = 0.8; setVolumen(prev); sonarClick(); }
  else { try { localStorage.setItem('sonido:volPrev', String(volumen())); } catch {} setVolumen(0); }   // guardamos el nivel y muteamos
  return activar;                   // true = ahora activo
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
  o.connect(g); g.connect(bus());
  o.start(t0); o.stop(t0 + dur);
  musNodos.push(o);
  o.onended = () => { musNodos = musNodos.filter((x) => x !== o); };
}
// ── batería 8-bit (kick/snare/hihat) — le da pegada de battle theme ──
let _noise;
function noiseBuf() { const c = ac(); if (!_noise) { _noise = c.createBuffer(1, c.sampleRate * 0.4, c.sampleRate); const d = _noise.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1; } return _noise; }
function track(node) { musNodos.push(node); node.onended = () => { musNodos = musNodos.filter((x) => x !== node); }; }
function kick(start, vol = 0.34) { const c = ac(); const o = c.createOscillator(), g = c.createGain(); const t0 = c.currentTime + start; o.type = 'sine'; o.frequency.setValueAtTime(128, t0); o.frequency.exponentialRampToValueAtTime(42, t0 + 0.11); g.gain.setValueAtTime(vol, t0); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.17); o.connect(g); g.connect(bus()); o.start(t0); o.stop(t0 + 0.19); track(o); }
function snare(start, vol = 0.2) { const c = ac(); const s = c.createBufferSource(); s.buffer = noiseBuf(); const f = c.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 1400; const g = c.createGain(); const t0 = c.currentTime + start; g.gain.setValueAtTime(vol, t0); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.13); s.connect(f); f.connect(g); g.connect(bus()); s.start(t0); s.stop(t0 + 0.15); track(s); }
function hihat(start, vol = 0.06) { const c = ac(); const s = c.createBufferSource(); s.buffer = noiseBuf(); const f = c.createBiquadFilter(); f.type = 'highpass'; f.frequency.value = 7000; const g = c.createGain(); const t0 = c.currentTime + start; g.gain.setValueAtTime(vol, t0); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.04); s.connect(f); f.connect(g); g.connect(bus()); s.start(t0); s.stop(t0 + 0.05); track(s); }
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

// Música de fondo de BATALLA: tema HEROICO 8-bit (progresión épica Am–F–C–G), con bajo galopante,
// hook melódico que resuelve y arpegios brillantes. Loop original que se reagenda solo.
const PASO = 0.13;          // corchea más rápida (~185bpm) → urgencia de battle-vs-trainer
const COMPASES = 4, PxC = 8; // 4 compases × 8 corcheas
const PROG_RAIZ = [110.0, 87.31, 130.81, 98.0];   // A2  F2  C3  G2
const PROG_OCT = [220.0, 174.61, 261.63, 196.0];  // A3  F3  C4  G3
const PROG_QNT = [164.81, 130.81, 196.0, 146.83]; // E3  C3  G3  D3
// galope de corcheas por compás: raíz raíz octava raíz quinta raíz octava quinta
const GALOPE = (b) => [PROG_RAIZ[b], PROG_RAIZ[b], PROG_OCT[b], PROG_RAIZ[b], PROG_QNT[b], PROG_RAIZ[b], PROG_OCT[b], PROG_QNT[b]];
// hook melódico por compás (0 = silencio): frase heroica que sube y resuelve
const MELODIA = [
  [659, 0, 587, 523, 0, 659, 523, 440],   // Am: E5 . D5 C5 . E5 C5 A4
  [523, 0, 440, 349, 0, 523, 440, 349],   // F:  C5 . A4 F4 . C5 A4 F4
  [523, 587, 659, 0, 784, 0, 659, 523],   // C:  C5 D5 E5 . G5 . E5 C5
  [587, 0, 494, 392, 494, 587, 0, 392],   // G:  D5 . B4 G4 B4 D5 . G4
];
// arpegios en semicorcheas por acorde — el "shimmer" clásico del battle theme GBA
const ARP = [
  [440, 523, 659, 523],   // Am: A C E
  [349, 440, 523, 440],   // F:  F A C
  [523, 659, 784, 659],   // C:  C E G
  [392, 494, 587, 494],   // G:  G B D
];
function loopBatalla() {
  if (muteado()) { musLoop = null; return; }
  for (let b = 0; b < COMPASES; b++) {
    const bajo = GALOPE(b);
    const arp = ARP[b];
    for (let s = 0; s < PxC; s++) {
      const t = (b * PxC + s) * PASO;
      // batería: kick en 1 y 3, snare (backbeat) en 2 y 4, hi-hat en cada corchea
      if (s % 4 === 0) kick(t);
      if (s % 4 === 2) snare(t);
      hihat(t, s % 2 ? 0.04 : 0.07);
      if (s === 7) kick(t, 0.22);                                       // pickup al cierre del compás
      nota(bajo[s], t, PASO * 0.92, 'triangle', 0.09);                  // bajo galopante
      const mf = MELODIA[b][s];
      if (mf) { nota(mf, t, PASO * 0.82, 'square', 0.085); nota(mf * 1.006, t, PASO * 0.82, 'square', 0.035); }   // lead doble (detune = más gordo)
      // arpegio en semicorcheas (octava arriba): acompañamiento brillante estilo GBA
      nota(arp[(s * 2) % 4] * 2, t, PASO * 0.42, 'square', 0.016);
      nota(arp[(s * 2 + 1) % 4] * 2, t + PASO * 0.5, PASO * 0.42, 'square', 0.016);
    }
  }
  const LARGO = COMPASES * PxC * PASO;     // 4*8*0.15 = 4.8s
  musLoop = setTimeout(loopBatalla, LARGO * 1000 - 40);
}
export function musicaBatalla() { if (muteado()) return; detenerMusica(); try { loopBatalla(); } catch {} }
