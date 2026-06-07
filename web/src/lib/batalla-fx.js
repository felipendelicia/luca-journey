// batalla-fx.js — animaciones de ataque estilo GBA. Cada movimiento anima según su id (override) o,
// si no hay override, según su TIPO (base). Todo es DOM + CSS (keyframes en global.css), sin libs.
// API: efectoAtaque(arena, mov, haciaRival)  → haciaRival = true si el que recibe es el rival.

const rnd = (a, b) => a + Math.random() * (b - a);
const TCOLOR = { Normal: '#c8c8d0', Fuego: '#ff7a2c', Agua: '#3aa0e6', Planta: '#5cc23c', 'Eléctrico': '#f2d022', Hielo: '#7fe0e0', Lucha: '#e0506a', Veneno: '#b35fd6', Tierra: '#d39b4f', Volador: '#a8c0ee', 'Psíquico': '#fb6a8e', Bicho: '#a4c41e', Roca: '#bcaa70', Fantasma: '#7763c0', 'Dragón': '#5a78e0', Siniestro: '#5a5566', Acero: '#9fb6c4', Hada: '#f29ae6' };

// capa de efectos sobre la arena (se autodestruye)
function capa(arena) {
  const l = document.createElement('div'); l.className = 'fx-layer';
  arena.appendChild(l); setTimeout(() => l.remove(), 1500);
  return l;
}
// posición (px) del centro de cada combatiente dentro de la arena
function puntos(arena, haciaRival) {
  const w = arena.clientWidth, h = arena.clientHeight;
  const def = haciaRival ? { x: w * 0.76, y: h * 0.30 } : { x: w * 0.26, y: h * 0.70 };
  const atk = haciaRival ? { x: w * 0.26, y: h * 0.70 } : { x: w * 0.76, y: h * 0.30 };
  return { def, atk, w, h };
}
// una partícula con animación parametrizada por custom props
function part(layer, x, y, css, vars, anim, dur, delay = 0, ease = 'ease-out') {
  const p = document.createElement('div'); p.className = 'fxp';
  p.style.cssText = 'left:' + x + 'px;top:' + y + 'px;' + css;
  for (const k in vars) p.style.setProperty('--' + k, vars[k]);
  p.style.animation = 'fx-' + anim + ' ' + dur + 's ' + ease + ' ' + delay + 's forwards';
  layer.appendChild(p);
}
// estallido radial de n partículas desde (cx,cy)
function estallido(layer, cx, cy, n, make) {
  for (let i = 0; i < n; i++) { const o = make(i, n); part(layer, cx, cy, o.css, o.vars, o.anim || 'fly', o.dur || 0.55, o.delay || 0, o.ease); }
}
// flash radial
function flash(layer, cx, cy, color, size = 150, dur = 0.4) {
  part(layer, cx, cy, 'width:' + size + 'px;height:' + size + 'px;border-radius:50%;background:radial-gradient(circle,' + color + ' 0%,transparent 65%)', { s: 1.7 }, 'flash', dur);
}
// anillo expansivo
function anillo(layer, cx, cy, color, dur = 0.5) {
  part(layer, cx, cy, 'width:60px;height:60px;border-radius:50%;border:4px solid ' + color, { s: 2.4 }, 'ring', dur);
}
// rayo de energía de atacante→defensor (bar rotado)
function rayo(layer, a, d, color, grosor = 14, dur = 0.5) {
  const dx = d.x - a.x, dy = d.y - a.y; const len = Math.hypot(dx, dy); const ang = Math.atan2(dy, dx) * 180 / Math.PI;
  const b = document.createElement('div'); b.className = 'fxp';
  b.style.cssText = 'left:' + a.x + 'px;top:' + (a.y - grosor / 2) + 'px;width:' + len + 'px;height:' + grosor + 'px;transform-origin:0 50%;border-radius:' + grosor + 'px;'
    + 'background:linear-gradient(90deg,transparent,' + color + ' 18%,#fff 50%,' + color + ' 82%,transparent);box-shadow:0 0 14px ' + color;
  b.style.setProperty('--rot', ang + 'deg');
  b.style.animation = 'fx-beam ' + dur + 's ease-out forwards';
  layer.appendChild(b);
}
// destello de pantalla completa (rayos eléctricos, híper rayo)
function pantallazo(layer, color, dur = 0.32) {
  const f = document.createElement('div'); f.className = 'fxp fx-screen';
  f.style.cssText = 'left:0;top:0;width:100%;height:100%;background:' + color;
  f.style.animation = 'fx-shock ' + dur + 's steps(3) forwards';
  layer.appendChild(f);
}
// rayo SVG zigzag cayendo sobre el defensor
function bolt(layer, d) {
  const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
  svg.setAttribute('width', '120'); svg.setAttribute('height', '170'); svg.classList.add('fxp', 'fx-bolt');
  svg.style.cssText = 'left:' + (d.x - 60) + 'px;top:' + (d.y - 150) + 'px';
  svg.innerHTML = "<polyline points='60,0 42,52 72,58 36,118 66,124 30,170' fill='none' stroke='#fff14a' stroke-width='7' stroke-linejoin='round' style='filter:drop-shadow(0 0 6px #ffe23a)'/>";
  svg.style.animation = 'fx-shock .4s steps(3) forwards';
  layer.appendChild(svg);
}

// ───────── efectos por TIPO (base, cubren TODOS los movimientos) ─────────
const TYPE_FX = {
  Normal: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(255,255,255,.85)', 130); estallido(l, d.x, d.y, 10, () => { const a = rnd(0, 6.28), r = rnd(34, 70); return { css: 'width:8px;height:8px;border-radius:50%;background:#fff', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px' }, dur: 0.45 }; }); },
  Fuego: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(255,140,40,.9)', 150); estallido(l, d.x, d.y, 18, () => ({ css: 'width:14px;height:14px;border-radius:50% 50% 50% 0;background:radial-gradient(circle at 40% 35%,#ffe07a,#ff8a2c 55%,#e63a16)', vars: { x: rnd(-30, 30) + 'px', y: rnd(-90, -30) + 'px', s: rnd(0.8, 1.3) }, anim: 'rise', dur: rnd(0.5, 0.75), delay: rnd(0, 0.14) })); },
  Agua: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(80,170,240,.8)', 130); anillo(l, d.x, d.y, '#6fc0ff', 0.5); estallido(l, d.x, d.y, 20, () => { const a = rnd(-3.14, 0), r = rnd(45, 95); return { css: 'width:11px;height:11px;border-radius:50%;background:radial-gradient(circle at 38% 30%,#bfe9ff,#3aa0e6 60%,#1f6fc0);box-shadow:0 0 6px #6fc0ff', vars: { x: Math.cos(a) * r + 'px', y: (Math.sin(a) * r + rnd(20, 55)) + 'px' }, dur: 0.6, delay: rnd(0, 0.1) }; }); },
  'Eléctrico': ({ l, d }) => { pantallazo(l, '#fff6b0'); bolt(l, d); estallido(l, d.x, d.y, 12, () => { const a = rnd(0, 6.28), r = rnd(30, 70); return { css: 'width:5px;height:5px;background:#fff3a0;box-shadow:0 0 8px 2px #ffe23a', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', s: 0 }, dur: 0.4, delay: rnd(0, 0.08) }; }); },
  Planta: ({ l, d }) => { estallido(l, d.x, d.y, 16, () => { const a = rnd(0, 6.28), r = rnd(40, 90); return { css: 'width:16px;height:10px;border-radius:0 100% 0 100%;background:linear-gradient(135deg,#bff06a,#3f9a2e)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: rnd(180, 540) + 'deg' }, anim: 'spin', dur: rnd(0.6, 0.85), delay: rnd(0, 0.12) }; }); },
  Hielo: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(150,230,230,.85)', 140); estallido(l, d.x, d.y, 14, () => { const a = rnd(0, 6.28), r = rnd(35, 80); return { css: 'width:9px;height:18px;background:linear-gradient(#eafcff,#7fe0e0);clip-path:polygon(50% 0,100% 50%,50% 100%,0 50%)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: rnd(-60, 60) + 'deg', s: rnd(0.7, 1.2) }, dur: 0.55, delay: rnd(0, 0.1) }; }); },
  Roca: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(190,170,110,.7)', 120); estallido(l, d.x, d.y, 13, () => { const a = rnd(0, 6.28), r = rnd(35, 80); return { css: 'width:' + rnd(10, 18) + 'px;height:' + rnd(10, 16) + 'px;border-radius:3px;background:linear-gradient(135deg,#cbb886,#7a6438)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: rnd(-180, 180) + 'deg' }, anim: 'spin', dur: 0.55, delay: rnd(0, 0.08) }; }); },
  Tierra: ({ l, d, arena }) => { arena.classList.add('bt-sacude'); setTimeout(() => arena.classList.remove('bt-sacude'), 320); estallido(l, d.x, d.y + 20, 16, () => ({ css: 'width:' + rnd(8, 16) + 'px;height:' + rnd(8, 14) + 'px;border-radius:3px;background:linear-gradient(135deg,#d8a85c,#8a5a28)', vars: { x: rnd(-50, 50) + 'px', y: rnd(-70, -20) + 'px', r: rnd(-180, 180) + 'deg' }, anim: 'spin', dur: 0.6, delay: rnd(0, 0.1) })); },
  Veneno: ({ l, d }) => { estallido(l, d.x, d.y, 14, () => ({ css: 'width:' + rnd(8, 16) + 'px;height:' + rnd(8, 16) + 'px;border-radius:50%;background:radial-gradient(circle at 35% 30%,#e7b6ff,#a23fd0 70%);opacity:.85', vars: { x: rnd(-35, 35) + 'px', y: rnd(-80, -20) + 'px', s: rnd(0.8, 1.4) }, anim: 'rise', dur: rnd(0.6, 0.9), delay: rnd(0, 0.15) })); },
  'Psíquico': ({ l, d }) => { anillo(l, d.x, d.y, '#fb6a8e', 0.55); anillo(l, d.x, d.y, '#ffa6c0', 0.7); flash(l, d.x, d.y, 'rgba(251,106,142,.6)', 150); },
  Volador: ({ l, d }) => { estallido(l, d.x, d.y, 12, (i) => { const a = -2.4 + i * 0.18, r = rnd(50, 95); return { css: 'width:20px;height:7px;border-radius:50%;background:linear-gradient(90deg,transparent,#eef4ff,#a8c0ee)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: (a * 57) + 'deg' }, dur: 0.5, delay: rnd(0, 0.12) }; }); },
  Lucha: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(255,255,255,.9)', 120); estallido(l, d.x, d.y, 8, (i) => ({ css: 'width:26px;height:5px;border-radius:3px;background:#ffd84a', vars: { x: '0px', y: '0px', r: (i * 45) + 'deg', s: 1.6 }, dur: 0.35 })); },
  Fantasma: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(120,90,200,.8)', 150); estallido(l, d.x, d.y, 12, () => ({ css: 'width:16px;height:16px;border-radius:50%;background:radial-gradient(circle,#9b7fe0,#3a2a66 75%);opacity:.8', vars: { x: rnd(-45, 45) + 'px', y: rnd(-55, 25) + 'px', s: rnd(0.6, 1.3) }, anim: 'rise', dur: rnd(0.6, 0.85), delay: rnd(0, 0.14) })); },
  Bicho: ({ l, d }) => { estallido(l, d.x, d.y, 14, () => { const a = rnd(0, 6.28), r = rnd(35, 80); return { css: 'width:8px;height:8px;border-radius:50%;background:#b6d63a', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px' }, dur: 0.5, delay: rnd(0, 0.1) }; }); },
  'Dragón': ({ l, d, atk }) => { rayo(l, atk, d, '#7a8ef0', 18, 0.5); anillo(l, d.x, d.y, '#9aa6ff', 0.55); },
  Hada: ({ l, d }) => { estallido(l, d.x, d.y, 16, () => { const a = rnd(0, 6.28), r = rnd(30, 80); return { css: 'width:12px;height:12px;background:#ffb6ee;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: rnd(0, 360) + 'deg', s: rnd(0.5, 1.1) }, anim: 'spin', dur: 0.6, delay: rnd(0, 0.14) }; }); },
  Acero: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(220,235,245,.9)', 120); estallido(l, d.x, d.y, 10, (i) => ({ css: 'width:22px;height:4px;border-radius:3px;background:linear-gradient(90deg,transparent,#fff,transparent)', vars: { x: '0px', y: '0px', r: (i * 36) + 'deg', s: 1.5 }, dur: 0.3 })); },
  Siniestro: ({ l, d }) => { flash(l, d.x, d.y, 'rgba(40,30,60,.8)', 160, 0.5); estallido(l, d.x, d.y, 12, () => ({ css: 'width:14px;height:14px;border-radius:50%;background:radial-gradient(circle,#5a4a7a,#1a1424 75%)', vars: { x: rnd(-40, 40) + 'px', y: rnd(-40, 40) + 'px', s: rnd(0.5, 1.2) }, dur: 0.55, delay: rnd(0, 0.12) })); },
};

// ───────── overrides por MOVIMIENTO (los icónicos) ─────────
const llamas = (ctx, n) => { rayo(ctx.l, ctx.atk, ctx.def, '#ff8a2c', 16, 0.45); flash(ctx.l, ctx.def.x, ctx.def.y, 'rgba(255,140,40,.9)', 150); TYPE_FX.Fuego(ctx); };
const chorro = (ctx, grosor) => { rayo(ctx.l, ctx.atk, ctx.def, '#3aa0e6', grosor, 0.5); flash(ctx.l, ctx.def.x, ctx.def.y, 'rgba(80,170,240,.8)', 130); TYPE_FX.Agua(ctx); };
const trueno = (ctx) => { pantallazo(ctx.l, '#fff6b0', 0.36); bolt(ctx.l, ctx.def); bolt(ctx.l, { x: ctx.def.x - 22, y: ctx.def.y }); TYPE_FX['Eléctrico'](ctx); };
const haz = (ctx, color) => { rayo(ctx.l, ctx.atk, ctx.def, color, 18, 0.55); flash(ctx.l, ctx.def.x, ctx.def.y, color, 150); };

const MOVE_FX = {
  52: (c) => llamas(c),                          // Ascuas
  53: (c) => llamas(c),                          // Lanzallamas
  126: (c) => { llamas(c); estallido(c.l, c.def.x, c.def.y, 6, (i) => ({ css: 'width:30px;height:8px;background:#ff7a2c;border-radius:4px', vars: { x: '0px', y: '0px', r: (i * 72) + 'deg', s: 1.8 }, dur: 0.4 })); },   // Llamarada (estrella)
  55: (c) => chorro(c, 12),                       // Pistola Agua
  56: (c) => chorro(c, 22),                       // Hidrobomba
  57: (c) => { chorro(c, 26); anillo(c.l, c.def.x, c.def.y, '#6fc0ff', 0.6); },   // Surf
  84: trueno, 85: trueno, 87: trueno,             // Impactrueno / Rayo / Trueno
  75: (c) => { estallido(c.l, c.def.x, c.def.y, 8, (i) => ({ css: 'width:30px;height:6px;border-radius:3px;background:linear-gradient(90deg,transparent,#bff06a,#3f9a2e)', vars: { x: '0px', y: '0px', r: (i % 2 ? 35 : -35) + 'deg', s: 1.6 }, dur: 0.4, delay: i * 0.04 })); TYPE_FX.Planta(c); },   // Hoja Afilada (cuchilladas)
  22: (c) => { rayo(c.l, c.atk, c.def, '#5cc23c', 10, 0.4); TYPE_FX.Planta(c); },   // Látigo Cepa
  76: (c) => haz(c, '#9ee34f'),                   // Rayo Solar
  89: (c) => TYPE_FX.Tierra(c),                   // Terremoto (sacude + rocas)
  91: (c) => TYPE_FX.Tierra(c),                   // Excavar
  63: (c) => { pantallazo(c.l, 'rgba(255,255,255,.5)', 0.4); haz(c, '#ffd84a'); flash(c.l, c.def.x, c.def.y, 'rgba(255,216,74,.9)', 200, 0.5); },   // Hiperrayo
  129: (c) => estallido(c.l, c.def.x, c.def.y, 14, () => { const a = rnd(0, 6.28), r = rnd(30, 80); return { css: 'width:14px;height:14px;background:#fff7a0;clip-path:polygon(50% 0,61% 35%,98% 35%,68% 57%,79% 91%,50% 70%,21% 91%,32% 57%,2% 35%,39% 35%)', vars: { x: Math.cos(a) * r + 'px', y: Math.sin(a) * r + 'px', r: rnd(0, 360) + 'deg' }, anim: 'spin', dur: 0.5, delay: rnd(0, 0.1) }; }),   // Rapidez (estrellas)
  58: (c) => haz(c, '#9ff0f0'),                   // Rayo Hielo
  59: (c) => { TYPE_FX.Hielo(c); estallido(c.l, c.def.x - 40, c.def.y - 30, 16, () => ({ css: 'width:8px;height:8px;border-radius:50%;background:#eafcff', vars: { x: rnd(50, 110) + 'px', y: rnd(20, 70) + 'px' }, dur: 0.6, delay: rnd(0, 0.2) })); },   // Ventisca
  247: (c) => { const b = document.createElement('div'); b.className = 'fxp'; b.style.cssText = 'left:' + c.atk.x + 'px;top:' + c.atk.y + 'px;width:26px;height:26px;border-radius:50%;background:radial-gradient(circle,#9b7fe0,#2a1a4a 80%);box-shadow:0 0 14px #6a4ac0'; b.style.setProperty('--x', (c.def.x - c.atk.x) + 'px'); b.style.setProperty('--y', (c.def.y - c.atk.y) + 'px'); b.style.animation = 'fx-fly .4s ease-in forwards'; c.l.appendChild(b); setTimeout(() => TYPE_FX.Fantasma(c), 360); },   // Bola Sombra (orbe viaja)
  44: (c) => { flash(c.l, c.def.x, c.def.y, 'rgba(255,255,255,.9)', 120); estallido(c.l, c.def.x, c.def.y, 2, (i) => ({ css: 'width:34px;height:22px;border:5px solid #fff;border-radius:50%;border-color:#fff transparent transparent transparent', vars: { x: '0px', y: (i ? 14 : -14) + 'px', s: 0.5 }, dur: 0.3 })); },   // Mordisco (mandíbulas)
  64: (c) => { rayo(c.l, c.atk, c.def, '#fff', 8, 0.3); TYPE_FX.Volador(c); },   // Picotazo
  17: (c) => TYPE_FX.Volador(c),                  // Ataque Ala
  88: (c) => TYPE_FX.Roca(c),                     // Lanzarrocas
  5: (c) => { flash(c.l, c.def.x, c.def.y, 'rgba(255,255,255,.95)', 130); TYPE_FX.Lucha(c); },   // Megapuño
  33: (c) => { flash(c.l, c.def.x, c.def.y, 'rgba(255,255,255,.85)', 110); TYPE_FX.Normal(c); },   // Placaje
  98: (c) => { estallido(c.l, c.def.x, c.def.y, 6, (i) => ({ css: 'width:40px;height:5px;background:linear-gradient(90deg,transparent,#fff)', vars: { x: '0px', y: '0px', r: (i * 30 - 75) + 'deg', s: 1.5 }, dur: 0.25 })); TYPE_FX.Normal(c); },   // Ataque Rápido (rayas)
};

// punto de entrada: dispara el efecto del movimiento (override por id, o base por tipo).
export function efectoAtaque(arena, mov, haciaRival) {
  if (!arena) return;
  const l = capa(arena);
  const { def, atk } = puntos(arena, haciaRival);
  const ctx = { l, d: def, def, atk, arena, mov };
  const fn = MOVE_FX[mov && mov.id] || TYPE_FX[mov && mov.tipo] || TYPE_FX.Normal;
  try { fn(ctx); } catch (e) {}
}
