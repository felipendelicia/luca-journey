// batalla-fx.js — motor de animaciones de ataque en CANVAS: partículas con física (velocidad,
// gravedad, fricción), glow aditivo, trails, haces y coreografía por movimiento. Cada ataque anima
// según su MOVIMIENTO (override) o, si no, según su TIPO/categoría. API estable para el combate:
//   efectoAtaque(arena, mov, haciaRival)   → haciaRival = true si el que recibe es el rival.

const rnd = (a, b) => a + Math.random() * (b - a);
const TCOLOR = { Normal: '#c8c8d0', Fuego: '#ff7a2c', Agua: '#3aa0e6', Planta: '#5cc23c', 'Eléctrico': '#f2d022', Hielo: '#7fe0e0', Lucha: '#e0506a', Veneno: '#b35fd6', Tierra: '#d39b4f', Volador: '#a8c0ee', 'Psíquico': '#fb6a8e', Bicho: '#a4c41e', Roca: '#bcaa70', Fantasma: '#7763c0', 'Dragón': '#5a78e0', Siniestro: '#5a5566', Acero: '#9fb6c4', Hada: '#f29ae6' };

// ───────────────────────── motor de partículas (canvas) ─────────────────────────
class FX {
  constructor(arena) {
    this.arena = arena;
    const c = document.createElement('canvas');
    c.className = 'fx-canvas';
    c.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:4';
    arena.appendChild(c);
    this.c = c; this.ctx = c.getContext('2d');
    this.P = []; this.O = []; this.E = []; this.run = false;   // E = emisores sostenidos (varios frames)
    this.tick = this.tick.bind(this);
    this.resize();
  }
  resize() {
    const r = this.arena.getBoundingClientRect();
    this.w = r.width || 1; this.h = r.height || 1;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    this.c.width = Math.round(this.w * dpr); this.c.height = Math.round(this.h * dpr);
    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
  add(p) { this.P.push(p); this.start(); }
  addO(o) { o.t = 0; this.O.push(o); this.start(); }
  emit(n, fn) { this.E.push({ n, fn }); this.start(); }   // emisor sostenido: fn(this) por n frames
  start() { if (!this.run) { this.run = true; requestAnimationFrame(this.tick); } }
  tick() {
    const ctx = this.ctx; ctx.clearRect(0, 0, this.w, this.h);
    // emisores sostenidos (llamas que ondulan, chorros, etc.)
    for (const e of this.E) { if (e.n > 0) { e.n--; try { e.fn(this); } catch (er) {} } }
    this.E = this.E.filter((e) => e.n > 0);
    // partículas
    for (const p of this.P) {
      if (p.turb) { p.vx += rnd(-p.turb, p.turb); p.vy += rnd(-p.turb, p.turb); }   // turbulencia → movimiento orgánico
      p.vx *= p.drag; p.vy *= p.drag; p.vy += p.g; p.x += p.vx; p.y += p.vy; p.rot += p.spin; p.life--;
      const k = p.life / p.max, a = p.fade ? k : 1;
      if (a <= 0) continue;
      ctx.globalAlpha = Math.max(0, Math.min(1, a));
      ctx.globalCompositeOperation = p.add ? 'lighter' : 'source-over';
      const r = p.r + (p.r2 - p.r) * (1 - k);
      ctx.fillStyle = p.col;
      if (p.shape === 'spark') { ctx.strokeStyle = p.col; ctx.lineWidth = Math.max(1, r * 0.6); ctx.beginPath(); ctx.moveTo(p.x, p.y); ctx.lineTo(p.x - p.vx * 2.6, p.y - p.vy * 2.6); ctx.stroke(); }
      else if (p.shape === 'rect' || p.shape === 'leaf') { ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.rot); ctx.beginPath(); if (p.shape === 'leaf') { ctx.ellipse(0, 0, r * 1.3, r * 0.6, 0, 0, 6.2832); ctx.fill(); } else ctx.fillRect(-r, -r * 0.5, r * 2, r); ctx.restore(); }
      else if (p.shape === 'star') { estrella(ctx, p.x, p.y, r, p.rot); }
      else if (p.shape === 'triUp' || p.shape === 'triDn') { const dy = p.shape === 'triUp' ? -1 : 1; ctx.beginPath(); ctx.moveTo(p.x, p.y + dy * r); ctx.lineTo(p.x - r, p.y - dy * r * 0.7); ctx.lineTo(p.x + r, p.y - dy * r * 0.7); ctx.closePath(); ctx.fill(); }
      else { ctx.beginPath(); ctx.arc(p.x, p.y, r, 0, 6.2832); ctx.fill(); }
    }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    // overlays (haces, flashes, anillos, rayos, pantallazos)
    for (const o of this.O) { o.t++; o.draw(ctx, o.t / o.life); }
    this.P = this.P.filter((p) => p.life > 0);
    this.O = this.O.filter((o) => o.t < o.life);
    if (this.P.length || this.O.length || this.E.length) requestAnimationFrame(this.tick); else this.run = false;
  }
}
function estrella(ctx, x, y, r, rot) {
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot || 0); ctx.beginPath();
  for (let i = 0; i < 10; i++) { const ra = i % 2 ? r * 0.45 : r; const a = Math.PI / 5 * i - Math.PI / 2; ctx[i ? 'lineTo' : 'moveTo'](Math.cos(a) * ra, Math.sin(a) * ra); }
  ctx.closePath(); ctx.fill(); ctx.restore();
}
function getFX(arena) {
  if (!arena.__fx || !arena.contains(arena.__fx.c)) arena.__fx = new FX(arena);
  else arena.__fx.resize();
  return arena.__fx;
}

// ───────────────────────── emisores (helpers) ─────────────────────────
// estallido radial / cono
function burst(fx, x, y, n, o) {
  for (let i = 0; i < n; i++) {
    const a = o.dir != null ? o.dir + rnd(-(o.spread || 0.5), o.spread || 0.5) : rnd(0, 6.2832);
    const sp = rnd(o.spMin != null ? o.spMin : 1.5, o.spMax != null ? o.spMax : 4.5);
    const r = (o.r != null ? o.r : 4) * rnd(0.7, 1.3);
    fx.add({ x: x + (o.jx ? rnd(-o.jx, o.jx) : 0), y: y + (o.jy ? rnd(-o.jy, o.jy) : 0), vx: Math.cos(a) * sp, vy: Math.sin(a) * sp + (o.vyBias || 0), g: o.g || 0, drag: o.drag != null ? o.drag : 0.94, life: Math.round((o.life || 30) * rnd(0.8, 1.1)), max: o.life || 30, r, r2: o.r2 != null ? o.r2 : r, col: typeof o.col === 'function' ? o.col() : o.col, add: !!o.add, shape: o.shape || 'circle', rot: rnd(0, 6.28), spin: o.spin != null ? o.spin : 0, fade: o.fade !== false });
  }
}
// haz de energía atacante→defensor (overlay animado)
function beam(fx, a, b, col, wid, life = 26) {
  fx.addO({ life, draw(ctx, k) { const grow = Math.min(1, k * 1.7), al = k < 0.6 ? 1 : 1 - (k - 0.6) / 0.4; const ex = a.x + (b.x - a.x) * grow, ey = a.y + (b.y - a.y) * grow; const g = ctx.createLinearGradient(a.x, a.y, ex, ey); g.addColorStop(0, 'transparent'); g.addColorStop(0.5, col); g.addColorStop(0.5, '#fff'); g.addColorStop(1, col); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = al; ctx.strokeStyle = g; ctx.lineCap = 'round'; ctx.lineWidth = wid * (1 + Math.sin(k * 9) * 0.12); ctx.shadowBlur = wid; ctx.shadowColor = col; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(ex, ey); ctx.stroke(); ctx.shadowBlur = 0; ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; } });
}
// flash radial
function flash(fx, x, y, col, r = 70, life = 18) {
  fx.addO({ life, draw(ctx, k) { const rr = r * (0.3 + k * 1.5), al = 1 - k; const g = ctx.createRadialGradient(x, y, 0, x, y, rr); g.addColorStop(0, col); g.addColorStop(1, 'transparent'); ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = al; ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, rr, 0, 6.2832); ctx.fill(); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; } });
}
// anillo expansivo (onda de choque)
function ring(fx, x, y, col, r = 70, life = 20, wid = 5) {
  fx.addO({ life, draw(ctx, k) { const rr = r * (0.15 + k * 1.1), al = 1 - k; ctx.globalAlpha = al; ctx.strokeStyle = col; ctx.lineWidth = wid * (1 - k * 0.6); ctx.beginPath(); ctx.arc(x, y, rr, 0, 6.2832); ctx.stroke(); ctx.globalAlpha = 1; } });
}
// pantallazo (flicker de color a pantalla completa)
function screen(fx, col, life = 14) {
  fx.addO({ life, draw(ctx, k) { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = (1 - k) * (0.5 + 0.5 * Math.abs(Math.sin(k * 12))); ctx.fillStyle = col; ctx.fillRect(0, 0, fx.w, fx.h); ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; } });
}
// rayo eléctrico zigzag cayendo sobre el defensor (se redibuja con jitter)
function bolt(fx, x, y, life = 16) {
  fx.addO({ life, draw(ctx, k) { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = k < 0.8 ? 1 : 1 - (k - 0.8) / 0.2; ctx.strokeStyle = '#fff14a'; ctx.lineWidth = 5; ctx.shadowBlur = 12; ctx.shadowColor = '#ffe23a'; ctx.lineJoin = 'round'; ctx.beginPath(); let py = y - 150; ctx.moveTo(x, py); while (py < y) { py += rnd(20, 34); ctx.lineTo(x + rnd(-22, 22), Math.min(y, py)); } ctx.stroke(); ctx.shadowBlur = 0; ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; } });
}
// humo (puffs grises que suben y se expanden)
function humo(fx, x, y, n = 8) {
  for (let i = 0; i < n; i++) fx.add({ x: x + rnd(-18, 18), y: y + rnd(-10, 10), vx: rnd(-0.6, 0.6), vy: rnd(-1.6, -0.4), g: -0.01, drag: 0.96, turb: 0.18, life: rnd(34, 56), max: 50, r: rnd(8, 14), r2: rnd(22, 34), col: 'rgba(80,75,80,.5)', add: false, shape: 'circle', rot: 0, spin: 0, fade: true });
}
// onda de choque blanca (impacto universal)
function choque(fx, x, y) { ring(fx, x, y, 'rgba(255,255,255,.9)', 64, 18, 5); flash(fx, x, y, 'rgba(255,255,255,.7)', 46, 12); }
// carga previa en el atacante (partículas que convergen + flash) antes de un haz
function cargar(fx, a, col) { for (let i = 0; i < 10; i++) { const ang = rnd(0, 6.28), d = rnd(28, 46); fx.add({ x: a.x + Math.cos(ang) * d, y: a.y + Math.sin(ang) * d, vx: -Math.cos(ang) * d * 0.18, vy: -Math.sin(ang) * d * 0.18, g: 0, drag: 0.9, life: 14, max: 14, r: 4, r2: 1, col, add: true, shape: 'circle', rot: 0, spin: 0, fade: true }); } flash(fx, a.x, a.y, col, 36, 12); }

// ───────────────────────── efectos por TIPO (base) ─────────────────────────
const dosCol = (a, b) => () => (Math.random() < 0.5 ? a : b);
const fuegoCol = () => { const r = Math.random(); return r < 0.22 ? '#fff2b0' : r < 0.58 ? '#ffd24a' : r < 0.85 ? '#ff8a2c' : '#e6431a'; };
const aguaCol = () => { const r = Math.random(); return r < 0.35 ? '#eafaff' : r < 0.7 ? '#7fd0ff' : '#2f8fd8'; };
const TYPE_FX = {
  Normal: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.9)', 60); burst(c.fx, c.d.x, c.d.y, 14, { col: '#fff', add: true, r: 4, r2: 1, spMin: 2, spMax: 6, life: 24 }); },
  // llama irregular: emite por 14 frames, partículas que suben con turbulencia, tamaños/colores variados
  Fuego: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,150,50,.9)', 72); c.fx.emit(14, (fx) => { for (let i = 0; i < 3; i++) { const a = rnd(-2.5, -0.6); fx.add({ x: c.d.x + rnd(-18, 18), y: c.d.y + rnd(-4, 12), vx: Math.cos(a) * rnd(0.7, 2.2), vy: Math.sin(a) * rnd(1.4, 3.4), g: -0.03, drag: 0.93, turb: 0.55, life: Math.round(rnd(18, 34)), max: 30, r: rnd(4, 11), r2: 0.5, col: fuegoCol(), add: true, shape: 'circle', rot: 0, spin: 0, fade: true }); } }); humo(c.fx, c.d.x, c.d.y - 12, 7); },
  // agua irregular: chorro de gotas con gravedad + spray, tamaños/arcos dispares
  Agua: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(80,180,255,.8)', 55); ring(c.fx, c.d.x, c.d.y + 8, '#7fd0ff', 62, 22, 4); c.fx.emit(9, (fx) => { for (let i = 0; i < 4; i++) { const a = rnd(-2.8, -0.3); fx.add({ x: c.d.x + rnd(-10, 10), y: c.d.y, vx: Math.cos(a) * rnd(1.8, 6), vy: Math.sin(a) * rnd(2, 6), g: 0.3, drag: 0.98, turb: 0.22, life: Math.round(rnd(26, 46)), max: 40, r: rnd(2.5, 6.5), r2: 1, col: aguaCol(), add: true, shape: Math.random() < 0.45 ? 'spark' : 'circle', rot: 0, spin: 0, fade: true }); } }); },
  'Eléctrico': (c) => { screen(c.fx, 'rgba(255,246,160,.55)'); bolt(c.fx, c.d.x, c.d.y); burst(c.fx, c.d.x, c.d.y, 18, { col: '#fff7a0', add: true, r: 4, r2: 0, spMin: 3, spMax: 8, life: 18, shape: 'spark' }); },
  Planta: (c) => { burst(c.fx, c.d.x, c.d.y, 18, { col: dosCol('#bff06a', '#3f9a2e'), r: 8, r2: 5, spMin: 1.5, spMax: 5, g: 0.06, drag: 0.95, life: 40, shape: 'leaf', spin: 0.3 }); },
  Hielo: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(160,240,240,.85)', 64); burst(c.fx, c.d.x, c.d.y, 16, { col: dosCol('#eafcff', '#7fe0e0'), add: true, r: 7, r2: 3, spMin: 2, spMax: 6, life: 30, shape: 'rect', spin: 0.2 }); },
  Roca: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(190,170,110,.6)', 50); burst(c.fx, c.d.x, c.d.y, 14, { col: dosCol('#cbb886', '#7a6438'), r: 8, r2: 6, spMin: 2, spMax: 6, g: 0.3, drag: 0.98, life: 36, shape: 'rect', spin: 0.4 }); humo(c.fx, c.d.x, c.d.y, 5); },
  Tierra: (c) => { sacudir(c.arena); burst(c.fx, c.d.x, c.d.y + 18, 18, { col: dosCol('#d8a85c', '#8a5a28'), r: 8, r2: 5, dir: -1.57, spread: 1, spMin: 3, spMax: 7, g: 0.34, drag: 0.98, life: 40, shape: 'rect', spin: 0.4 }); humo(c.fx, c.d.x, c.d.y + 16, 8); },
  Veneno: (c) => { burst(c.fx, c.d.x, c.d.y, 16, { col: dosCol('#e7b6ff', '#a23fd0'), add: true, r: 8, r2: 4, vyBias: -1.6, g: -0.02, drag: 0.95, life: 44, jx: 10 }); },
  'Psíquico': (c) => { ring(c.fx, c.d.x, c.d.y, '#fb6a8e', 70, 24, 6); ring(c.fx, c.d.x, c.d.y, '#ffa6c0', 90, 30, 4); flash(c.fx, c.d.x, c.d.y, 'rgba(251,106,142,.6)', 60); burst(c.fx, c.d.x, c.d.y, 12, { col: '#ffb6cf', add: true, r: 4, r2: 1, spMin: 1, spMax: 3, life: 30 }); },
  Volador: (c) => { burst(c.fx, c.d.x, c.d.y, 14, { col: '#eef4ff', add: true, r: 5, r2: 1, dir: -2.2, spread: 0.5, spMin: 4, spMax: 8, life: 24, shape: 'spark' }); },
  Lucha: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.95)', 60); ring(c.fx, c.d.x, c.d.y, '#ffd84a', 56, 16, 6); burst(c.fx, c.d.x, c.d.y, 10, { col: '#ffe06a', add: true, r: 5, r2: 1, spMin: 3, spMax: 7, life: 20, shape: 'spark' }); },
  Fantasma: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(120,90,200,.8)', 70); burst(c.fx, c.d.x, c.d.y, 14, { col: dosCol('#9b7fe0', '#3a2a66'), add: true, r: 9, r2: 4, vyBias: -0.8, drag: 0.95, life: 40, jx: 10 }); },
  Bicho: (c) => { burst(c.fx, c.d.x, c.d.y, 14, { col: dosCol('#b6d63a', '#7a9a1e'), r: 5, r2: 2, spMin: 2, spMax: 6, life: 28 }); },
  'Dragón': (c) => { beam(c.fx, c.atk, c.d, '#7a8ef0', 18); ring(c.fx, c.d.x, c.d.y, '#9aa6ff', 70, 22, 5); burst(c.fx, c.d.x, c.d.y, 12, { col: '#aab6ff', add: true, r: 5, r2: 2, spMin: 2, spMax: 5, life: 26 }); },
  Hada: (c) => { burst(c.fx, c.d.x, c.d.y, 16, { col: dosCol('#ffd6f4', '#f29ae6'), add: true, r: 7, r2: 2, spMin: 1.5, spMax: 5, life: 34, shape: 'star', spin: 0.25 }); },
  Acero: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(230,240,250,.95)', 56); burst(c.fx, c.d.x, c.d.y, 12, { col: '#fff', add: true, r: 4, r2: 1, spMin: 3, spMax: 8, life: 18, shape: 'spark' }); },
  Siniestro: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(60,40,90,.85)', 80); burst(c.fx, c.d.x, c.d.y, 14, { col: dosCol('#5a4a7a', '#1a1424'), r: 9, r2: 4, spMin: 1.5, spMax: 5, life: 34, jx: 8 }); },
};
function sacudir(arena) { arena.classList.add('bt-sacude'); setTimeout(() => arena.classList.remove('bt-sacude'), 320); }

// ───────────────────────── overrides por MOVIMIENTO (icónicos) ─────────────────────────
const llamas = (c) => { cargar(c.fx, c.atk, '#ff8a2c'); beam(c.fx, c.atk, c.d, '#ff7a2c', 16); TYPE_FX.Fuego(c); };
const chorro = (c, w) => { cargar(c.fx, c.atk, '#3aa0e6'); beam(c.fx, c.atk, c.d, '#3aa0e6', w); TYPE_FX.Agua(c); };
const truenoFx = (c) => { screen(c.fx, 'rgba(255,246,160,.6)'); bolt(c.fx, c.d.x, c.d.y); bolt(c.fx, c.d.x - 24, c.d.y, 14); TYPE_FX['Eléctrico'](c); };
const hazCol = (c, col) => { cargar(c.fx, c.atk, col); beam(c.fx, c.atk, c.d, col, 18); flash(c.fx, c.d.x, c.d.y, col, 64); };
const MOVE_FX = {
  52: llamas, 53: llamas,
  126: (c) => { llamas(c); burst(c.fx, c.d.x, c.d.y, 7, { col: '#ff7a2c', add: true, r: 10, r2: 4, spMin: 4, spMax: 8, life: 26, shape: 'star' }); },   // Llamarada
  55: (c) => chorro(c, 12), 56: (c) => chorro(c, 22), 57: (c) => { chorro(c, 26); ring(c.fx, c.d.x, c.d.y, '#7fd0ff', 90, 26, 5); },
  84: truenoFx, 85: truenoFx, 87: truenoFx,
  75: (c) => { for (let i = 0; i < 3; i++) burst(c.fx, c.d.x, c.d.y, 6, { col: '#bff06a', add: true, r: 8, r2: 3, dir: i % 2 ? -0.6 : -2.5, spread: 0.3, spMin: 5, spMax: 9, life: 18, shape: 'rect' }); TYPE_FX.Planta(c); },   // Hoja Afilada
  22: (c) => { beam(c.fx, c.atk, c.d, '#5cc23c', 10); TYPE_FX.Planta(c); },
  76: (c) => hazCol(c, '#9ee34f'),
  89: (c) => TYPE_FX.Tierra(c), 91: (c) => TYPE_FX.Tierra(c),
  63: (c) => { screen(c.fx, 'rgba(255,255,255,.6)'); hazCol(c, '#ffd84a'); flash(c.fx, c.d.x, c.d.y, '#ffd84a', 100, 22); },   // Hiperrayo
  129: (c) => burst(c.fx, c.d.x, c.d.y, 14, { col: '#fff7a0', add: true, r: 8, r2: 3, spMin: 2, spMax: 6, life: 30, shape: 'star', spin: 0.3 }),   // Rapidez
  58: (c) => hazCol(c, '#9ff0f0'),
  59: (c) => { TYPE_FX.Hielo(c); burst(c.fx, c.d.x - 60, c.d.y - 40, 18, { col: '#eafcff', add: true, r: 5, r2: 2, dir: 0.5, spread: 0.4, spMin: 5, spMax: 9, life: 30, shape: 'rect' }); },   // Ventisca
  247: (c) => { proyectil(c, '#7a4ad0'); setTimeout(() => { try { TYPE_FX.Fantasma(c); } catch (e) {} }, 320); },   // Bola Sombra
  44: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.9)', 60); for (const s of [-1, 1]) c.fx.addO({ life: 16, draw(ctx, k) { ctx.globalAlpha = 1 - k; ctx.strokeStyle = '#fff'; ctx.lineWidth = 6; ctx.beginPath(); ctx.arc(c.d.x, c.d.y, 22, s > 0 ? 0.2 : 3.34, s > 0 ? 1.1 : 4.24); ctx.stroke(); ctx.globalAlpha = 1; } }); },   // Mordisco
  64: (c) => { beam(c.fx, c.atk, c.d, '#fff', 7, 14); TYPE_FX.Volador(c); }, 17: (c) => TYPE_FX.Volador(c),
  88: (c) => TYPE_FX.Roca(c),
  5: (c) => { TYPE_FX.Lucha(c); }, 33: (c) => TYPE_FX.Normal(c),
  98: (c) => burst(c.fx, c.d.x, c.d.y, 8, { col: '#fff', add: true, r: 4, r2: 1, dir: 3.14, spread: 0.6, spMin: 6, spMax: 10, life: 14, shape: 'spark' }),   // Ataque Rápido
};
function proyectil(c, col) { const a = c.atk, b = c.d, life = 20; c.fx.addO({ life, draw(ctx, k) { const x = a.x + (b.x - a.x) * k, y = a.y + (b.y - a.y) * k; ctx.globalCompositeOperation = 'lighter'; ctx.shadowBlur = 16; ctx.shadowColor = col; ctx.fillStyle = col; ctx.beginPath(); ctx.arc(x, y, 13, 0, 6.28); ctx.fill(); ctx.fillStyle = '#fff'; ctx.beginPath(); ctx.arc(x, y, 6, 0, 6.28); ctx.fill(); ctx.shadowBlur = 0; ctx.globalCompositeOperation = 'source-over'; } }); }

// ───────────────────────── estado + ailment + plantillas ─────────────────────────
const esEstadoMov = (m) => !m || m.categoria === 'Estado' || !m.poder;
const AIL_COL = { veneno: '#b35fd6', quemadura: '#ff7a2c', paralisis: '#f2d022', sueno: '#8aa6df', congelado: '#7fe0e0', confusion: '#c060b0' };
function flechas(fx, x, y, sube) {
  const col = sube ? '#5cd24a' : '#ff5a5a';
  for (let i = 0; i < 5; i++) fx.add({ x: x + rnd(-22, 22), y: y + 8, vx: 0, vy: sube ? -2.2 : 2.2, g: 0, drag: 1, life: 40, max: 40, r: 9, r2: 9, col, add: false, shape: sube ? 'triUp' : 'triDn', rot: 0, spin: 0, fade: true });
}
function ailmentFx(fx, d, ail) { burst(fx, d.x, d.y, 7, { col: AIL_COL[ail] || '#fff', add: true, r: 6, r2: 2, vyBias: -1.4, drag: 0.95, life: 40, jx: 14 }); }
function efectoEstado(c) {
  const d = c.mov.desc || '';
  if (/\b(sube|aumenta|increment|refuerza|eleva|crece)/i.test(d)) flechas(c.fx, c.atk.x, c.atk.y, true);
  else if (/\b(baja|reduce|disminu|debilita)/i.test(d)) flechas(c.fx, c.d.x, c.d.y, false);
  else flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.6)', 50);
  if (c.mov.ailment) ailmentFx(c.fx, c.d, c.mov.ailment);
}
const C = (c) => TCOLOR[c.mov.tipo] || '#fff';
const T = {
  golpe: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.85)', 56); burst(c.fx, c.d.x, c.d.y, 12, { col: C(c), add: true, r: 6, r2: 2, spMin: 2, spMax: 6, life: 24 }); },
  multi: (c) => { for (let k = 0; k < 4; k++) setTimeout(() => { try { flash(c.fx, c.d.x + rnd(-18, 18), c.d.y + rnd(-16, 16), 'rgba(255,255,255,.9)', 36, 12); } catch (e) {} }, k * 95); },
  cuchillada: (c) => { for (let i = 0; i < 3; i++) c.fx.addO({ life: 14, t0: i, draw(ctx, k) { ctx.globalCompositeOperation = 'lighter'; ctx.globalAlpha = 1 - k; ctx.strokeStyle = C(c); ctx.lineWidth = 6 * (1 - k * 0.5); ctx.shadowBlur = 8; ctx.shadowColor = C(c); const dir = i % 2 ? 1 : -1; ctx.beginPath(); ctx.moveTo(c.d.x - 48, c.d.y - 28 * dir); ctx.lineTo(c.d.x + 48, c.d.y + 28 * dir); ctx.stroke(); ctx.shadowBlur = 0; ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over'; } }); },
  puno: (c) => { flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.95)', 64); ring(c.fx, c.d.x, c.d.y, '#ffd84a', 54, 16, 6); burst(c.fx, c.d.x, c.d.y, 9, { col: '#ffe06a', add: true, r: 5, r2: 1, spMin: 3, spMax: 7, life: 20, shape: 'spark' }); },
  mordida: MOVE_FX[44], picotazo: (c) => { beam(c.fx, c.atk, c.d, '#fff', 7, 12); flash(c.fx, c.d.x, c.d.y, 'rgba(255,255,255,.7)', 40); },
  haz: (c) => { cargar(c.fx, c.atk, C(c)); beam(c.fx, c.atk, c.d, C(c), 16); (TYPE_FX[c.mov.tipo] || TYPE_FX.Normal)(c); },
  proyectil: (c) => { proyectil(c, C(c)); setTimeout(() => { try { flash(c.fx, c.d.x, c.d.y, C(c), 60); (TYPE_FX[c.mov.tipo] || TYPE_FX.Normal)(c); } catch (e) {} }, 320); },
  absorber: (c) => { for (let i = 0; i < 14; i++) { const x = c.d.x + rnd(-30, 30), y = c.d.y + rnd(-30, 30); c.fx.add({ x, y, vx: (c.atk.x - x) * 0.06, vy: (c.atk.y - y) * 0.06, g: 0, drag: 1, life: 26, max: 26, r: 5, r2: 2, col: '#9ee34f', add: true, shape: 'circle', rot: 0, spin: 0, fade: true }); } },
  cura: (c) => { for (let i = 0; i < 12; i++) c.fx.add({ x: c.atk.x + rnd(-26, 26), y: c.atk.y + rnd(0, 26), vx: 0, vy: rnd(-1.6, -0.8), g: 0, drag: 1, life: 44, max: 44, r: 5, r2: 2, col: '#bfffce', add: true, shape: 'circle', rot: 0, spin: 0, fade: true }); },
  danza: (c) => { flechas(c.fx, c.atk.x, c.atk.y, true); burst(c.fx, c.atk.x, c.atk.y, 8, { col: '#ffe06a', add: true, r: 6, r2: 2, spMin: 1, spMax: 3, life: 36, shape: 'star', spin: 0.3 }); },
  polvo: (c) => { for (let i = 0; i < 16; i++) c.fx.add({ x: c.d.x + rnd(-40, 40), y: c.d.y - 50, vx: rnd(-0.4, 0.4), vy: rnd(0.8, 1.6), g: 0, drag: 1, life: 50, max: 50, r: 5, r2: 5, col: C(c), add: false, shape: 'circle', rot: 0, spin: 0, fade: true }); if (c.mov.ailment) ailmentFx(c.fx, c.d, c.mov.ailment); },
  onda: (c) => { ring(c.fx, c.atk.x, c.atk.y, C(c), 80, 26, 4); ring(c.fx, c.atk.x, c.atk.y, C(c), 110, 32, 3); },
  clima: (c) => { const agua = c.mov.tipo === 'Agua'; screen(c.fx, 'rgba(' + (agua ? '90,150,230' : '200,170,110') + ',.3)', 30); for (let i = 0; i < 26; i++) c.fx.add({ x: rnd(0, c.fx.w), y: -10, vx: rnd(-1.5, 0), vy: rnd(3, 6), g: 0, drag: 1, life: 50, max: 50, r: agua ? 2 : 3, r2: agua ? 2 : 3, col: C(c), add: false, shape: agua ? 'rect' : 'circle', rot: 1.4, spin: 0, fade: true }); },
};
const GRUPOS = {
  golpe: [38, 36, 29, 1, 310, 389, 185, 205, 21, 37, 228, 372, 117, 583, 332, 34, 371, 282, 283, 364, 401, 343, 363, 387, 23, 200, 175],
  mordida: [242], cuchillada: [10, 163, 400, 210, 232, 403], multi: [154, 31, 458, 24], puno: [370, 68, 276, 249, 179],
  picotazo: [450, 398, 40], haz: [93, 60, 352, 189, 145, 61, 362, 225, 406, 585, 248, 506, 246], proyectil: [412],
  absorber: [71, 72, 202], cura: [156, 105, 355, 235], danza: [14, 97, 347], polvo: [78], clima: [240, 201], onda: [48, 253],
};
for (const k in GRUPOS) for (const id of GRUPOS[k]) MOVE_FX[id] = T[k];
for (const id of [435, 209]) MOVE_FX[id] = TYPE_FX['Eléctrico'];
for (const id of [157]) MOVE_FX[id] = TYPE_FX.Roca;
for (const id of [523, 414]) MOVE_FX[id] = TYPE_FX.Tierra;
for (const id of [16]) MOVE_FX[id] = TYPE_FX.Volador;

// punto de entrada
export function efectoAtaque(arena, mov, haciaRival) {
  if (!arena || !mov) return;
  let fx; try { fx = getFX(arena); } catch (e) { return; }
  const w = fx.w, h = fx.h;
  const def = haciaRival ? { x: w * 0.76, y: h * 0.32 } : { x: w * 0.26, y: h * 0.70 };
  const atk = haciaRival ? { x: w * 0.26, y: h * 0.70 } : { x: w * 0.76, y: h * 0.32 };
  const c = { fx, d: def, def, atk, arena, mov };
  try {
    if (MOVE_FX[mov.id]) { MOVE_FX[mov.id](c); if (!esEstadoMov(mov)) choque(fx, def.x, def.y); return; }
    if (esEstadoMov(mov)) { efectoEstado(c); return; }
    if (mov.categoria === 'Especial') { cargar(fx, atk, C(c)); beam(fx, atk, def, C(c), 14); }
    (TYPE_FX[mov.tipo] || TYPE_FX.Normal)(c);
    if (mov.ailment) ailmentFx(fx, def, mov.ailment);
    choque(fx, def.x, def.y);
  } catch (e) {}
}
