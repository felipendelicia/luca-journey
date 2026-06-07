// sprites.js — sprites SVG originales (string) para piedras evolutivas, Pokéballs y las 48 medallas
// de la Liga. Devuelven markup inline → sirven tanto en .astro (set:html) como en scripts cliente
// que arman DOM por innerHTML. Theme-aware: gradientes propios, legibles en oscuro y claro.
//
//   itemSvg(itemId, size)  · piedras tipadas (id 'piedra*'), 'discoenlace', comodín 'piedra'
//   ballSvg(tier, size)    · 0=Poké, 1=Super(Great), 2=Ultra
//   badgeSvg(region, i, won, size) · medalla del gimnasio i (0..7) de la región (48 únicas)

let _gid = 0;                                   // ids de gradiente únicos (evita choques entre SVGs)
const uid = () => 'g' + (++_gid);
const svg = (size, inner, vb = 32) =>
  `<svg viewBox="0 0 ${vb} ${vb}" width="${size}" height="${size}" class="spr" aria-hidden="true" ` +
  `style="display:inline-block;vertical-align:middle">${inner}</svg>`;
const linGrad = (id, a, b, vert = true) =>
  `<linearGradient id="${id}" x1="0" y1="0" x2="${vert ? 0 : 1}" y2="${vert ? 1 : 0}">` +
  `<stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></linearGradient>`;
const radGrad = (id, a, b) =>
  `<radialGradient id="${id}" cx="0.38" cy="0.32" r="0.85">` +
  `<stop offset="0" stop-color="${a}"/><stop offset="1" stop-color="${b}"/></radialGradient>`;

// ───────────────────────── geometría ─────────────────────────
const pt = (cx, cy, r, ang) => [cx + r * Math.cos(ang), cy + r * Math.sin(ang)];
const fix = (n) => Math.round(n * 100) / 100;
const poly = (pts) => 'M' + pts.map((p) => fix(p[0]) + ',' + fix(p[1])).join(' L') + 'Z';
const ngon = (cx, cy, r, n, rot = -Math.PI / 2) =>
  poly(Array.from({ length: n }, (_, i) => pt(cx, cy, r, rot + (i * 2 * Math.PI) / n)));
const star = (cx, cy, n, oR, iR, rot = -Math.PI / 2) =>
  poly(Array.from({ length: n * 2 }, (_, i) => pt(cx, cy, i % 2 ? iR : oR, rot + (i * Math.PI) / n)));

// formas fijas (diseñadas en caja 32, centradas ~16,16)
const SHAPES = {
  circle: () => '<circle cx="16" cy="16" r="13" __F__/>',
  octagon: () => `<path d="${ngon(16, 16, 13.5, 8, -Math.PI / 8)}" __F__/>`,
  hexagon: () => `<path d="${ngon(16, 16, 13.5, 6)}" __F__/>`,
  diamond: () => `<path d="${poly([[16, 2], [28, 16], [16, 30], [4, 16]])}" __F__/>`,
  square: () => '<rect x="4" y="4" width="24" height="24" rx="3" __F__/>',
  triangle: () => `<path d="${poly([[16, 3], [29, 27], [3, 27]])}" __F__/>`,
  star8: () => `<path d="${star(16, 16, 8, 14, 6)}" __F__/>`,
  star5: () => `<path d="${star(16, 16, 5, 14, 6)}" __F__/>`,
  heart: () => '<path d="M16 28C6 21 3 15 3 11a6 6 0 0 1 11-3 6 6 0 0 1 11 3c0 4-3 10-13 17Z" __F__/>',
  raindrop: () => '<path d="M16 3C10 12 7 16 7 20a9 9 0 0 0 18 0c0-4-3-8-9-17Z" __F__/>',
  flame: () => '<path d="M16 3c2 5-3 7-1 11 1-2 3-3 3-3 1 3 4 4 4 9a10 10 0 0 1-20 0c0-5 4-7 5-11 1 3 3 3 4 4 1-4-1-6 1-10Z" __F__/>',
  leaf: () => '<path d="M27 5C12 5 5 13 5 24c0 1 0 2 1 3 8-1 21-6 21-22Z" __F__/>' +
    '<path d="M9 24C13 16 19 12 24 10" fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1"/>',
  wing: () => '<path d="M4 22c8-1 14-6 24-18-2 11-9 18-18 18-2 0-4 0-6 0Z" __F__/>',
  gear: () => `<path d="${star(16, 16, 9, 14, 9.5)}" __F__/><circle cx="16" cy="16" r="4.5" fill="rgba(0,0,0,.35)"/>`,
  snowflake: () => '<g __SF__ stroke-width="2.4" stroke-linecap="round" fill="none">' +
    '<path d="M16 3V29M5.5 9.5 26.5 22.5M26.5 9.5 5.5 22.5"/>' +
    '<path d="M16 7l-3 3M16 7l3 3M16 25l-3-3M16 25l3-3" stroke-width="2"/></g>',
  crystal: () => `<path d="${poly([[16, 2], [25, 11], [21, 30], [11, 30], [7, 11]])}" __F__/>` +
    '<path d="M16 2 11 30M16 2 21 30M7 11h18" fill="none" stroke="rgba(255,255,255,.4)" stroke-width="1"/>',
  shield: () => '<path d="M16 3 27 7v9c0 7-5 11-11 14-6-3-11-7-11-14V7Z" __F__/>',
  mountain: () => `<path d="${poly([[16, 4], [29, 28], [3, 28]])}" __F__/>` +
    '<path d="M16 4 12 14l3 3 3-4 4 6" fill="none" stroke="rgba(255,255,255,.55)" stroke-width="1.4"/>',
  flower: () => '<g __F__>' +
    Array.from({ length: 6 }, (_, i) => { const a = (i * Math.PI) / 3 - Math.PI / 2; const [x, y] = pt(16, 16, 8, a); return `<circle cx="${fix(x)}" cy="${fix(y)}" r="6"/>`; }).join('') +
    '</g><circle cx="16" cy="16" r="5" fill="#ffe08a"/>',
  spiral: () => '<path d="M16 6a10 10 0 1 1-9 6 7 7 0 1 0 9 3 4 4 0 1 1-3 4" fill="none" __ST__ stroke-width="3" stroke-linecap="round"/>',
};

// emblemas blancos pequeños (centro ~16,16) para reforzar la identidad
const EMBLEM = {
  bolt: '<path d="M18 6 9 18h5l-2 8 10-13h-6Z" fill="#fff" stroke="rgba(0,0,0,.25)" stroke-width=".6"/>',
  drop: '<path d="M16 9c-3 4-4.5 6-4.5 8a4.5 4.5 0 0 0 9 0c0-2-1.5-4-4.5-8Z" fill="rgba(255,255,255,.85)"/>',
  flame: '<path d="M16 8c1 3-2 4-1 6 .6-1 1.6-1.6 1.6-1.6.5 1.6 2.4 2 2.4 4.6a4 4 0 0 1-8 0c0-2.4 2-3.4 2.5-5 .5 1.6 1 1.6 1.5 2 .5-2-1-3 0-6Z" fill="rgba(255,255,255,.9)"/>',
  leaf: '<path d="M23 9C14 9 10 14 10 21c5 0 13-3 13-12Z" fill="rgba(255,255,255,.85)"/>',
  crescent: '<path d="M21 16a6 6 0 1 1-5-6 7 7 0 0 0 5 6Z" fill="rgba(255,255,255,.9)"/>',
  sun: '<g fill="rgba(255,255,255,.92)"><circle cx="16" cy="16" r="4.2"/>' +
    Array.from({ length: 8 }, (_, i) => { const a = (i * Math.PI) / 4; const [x1, y1] = pt(16, 16, 6.5, a), [x2, y2] = pt(16, 16, 9, a); return `<line x1="${fix(x1)}" y1="${fix(y1)}" x2="${fix(x2)}" y2="${fix(y2)}" stroke="rgba(255,255,255,.92)" stroke-width="1.6" stroke-linecap="round"/>`; }).join('') + '</g>',
  sparkle: '<path d="M16 8l1.6 5.4L23 15l-5.4 1.6L16 22l-1.6-5.4L9 15l5.4-1.6Z" fill="rgba(255,255,255,.95)"/>',
  halfsun: '<g fill="none" stroke="rgba(255,255,255,.92)" stroke-width="1.6" stroke-linecap="round"><path d="M9 20a7 7 0 0 1 14 0" fill="rgba(255,255,255,.5)"/><path d="M16 7v3M7 13l2 2M25 13l-2 2"/></g>',
};

// ───────────────────────── piedras + disco ─────────────────────────
const STONES = {
  piedrafuego:  { c: ['#ff9a4d', '#d62828'], em: 'flame' },
  piedraagua:   { c: ['#7cc4f2', '#1f5fbf'], em: 'drop' },
  piedratrueno: { c: ['#ffe066', '#e08a00'], em: 'bolt' },
  piedrahoja:   { c: ['#9be564', '#2f9e44'], em: 'leaf' },
  piedraluna:   { c: ['#8ea2e6', '#2b3a8a'], em: 'crescent' },
  piedrasol:    { c: ['#ffce4d', '#ff6a00'], em: 'sun' },
  piedradia:    { c: ['#fff6c2', '#e8c349'], em: 'sparkle' },
  piedraalba:   { c: ['#8df0e0', '#1f9d8f'], em: 'halfsun' },
  piedranoche:  { c: ['#a78be6', '#34246a'], em: 'crescent' },
  piedra:       { c: ['#d3d6df', '#7a7f8c'], em: 'sparkle' },   // comodín legacy
};

// gema tallada (diamante facetado) con gradiente del tipo + emblema
function gemSvg(c, em, size) {
  const g = uid();
  const body = `<path d="${poly([[16, 2.5], [26, 12], [16, 30], [6, 12]])}" fill="url(#${g})" stroke="rgba(0,0,0,.45)" stroke-width="1" stroke-linejoin="round"/>`;
  const facets = '<path d="M16 2.5 11 12l5 18 5-18ZM6 12h20" fill="none" stroke="rgba(255,255,255,.4)" stroke-width=".9"/>' +
    '<path d="M16 2.5 11 12h10Z" fill="rgba(255,255,255,.28)"/>';
  return svg(size, `<defs>${linGrad(g, c[0], c[1])}</defs>${body}${facets}${EMBLEM[em] || ''}`);
}

// Disco de Enlace (Linking Cord): cable turquesa con dos conectores
function discoSvg(size) {
  const g = uid();
  return svg(size, `<defs>${linGrad(g, '#5fe0d8', '#1b8f97')}</defs>` +
    `<circle cx="16" cy="16" r="13" fill="url(#${g})" stroke="rgba(0,0,0,.4)" stroke-width="1"/>` +
    '<path d="M11 21c-3-2-3-7 1-8 3-1 4 2 7 1 3-1 3-5 0-6" fill="none" stroke="#e9fbf9" stroke-width="2.4" stroke-linecap="round"/>' +
    '<circle cx="10.5" cy="21" r="2.4" fill="#cfeeec" stroke="#0c5a60" stroke-width="1"/>' +
    '<circle cx="20" cy="9.5" r="2.4" fill="#cfeeec" stroke="#0c5a60" stroke-width="1"/>' +
    '<circle cx="13" cy="11" r="1.4" fill="rgba(255,255,255,.7)"/>');
}

// ── consumibles (fieles a la saga, familias congruentes) ──
const STK = 'stroke="rgba(0,0,0,.42)" stroke-width="1" stroke-linejoin="round"';
const gloss = (cx, cy, rx, ry) => `<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}" fill="rgba(255,255,255,.5)"/>`;
// Línea de Pociones: botella SPRAY (cuerpo + líquido + etiqueta blanca + cabezal/boquilla gris).
function sprayBottle(c, size) {
  const g = uid();
  return svg(size, `<defs>${linGrad(g, c[0], c[1])}</defs>` +
    `<path d="M11 9 L6.5 7.4 L6.5 10.3 L11 11.6 Z" fill="#e3e7ee" ${STK}/>` +       // boquilla
    `<rect x="10.8" y="7.4" width="9.4" height="5" rx="1.3" fill="#e3e7ee" ${STK}/>` + // cabezal
    `<rect x="9" y="12.2" width="14" height="15.6" rx="3.4" fill="url(#${g})" ${STK}/>` + // cuerpo+líquido
    `<rect x="9" y="17.6" width="14" height="4.3" fill="rgba(255,255,255,.88)"/>` +    // etiqueta
    gloss(12, 15, 1.7, 2.6));
}
// Curas de estado: VIAL pequeño (tapa + cuello + cuerpo + etiqueta), color por estado.
function vialBottle(c, size) {
  const g = uid();
  return svg(size, `<defs>${linGrad(g, c[0], c[1])}</defs>` +
    `<rect x="12" y="6.5" width="8" height="3.8" rx="1.2" fill="#b9bfca" ${STK}/>` +  // tapa
    `<rect x="13.4" y="10" width="5.2" height="2.4" fill="#c7ccd5" ${STK}/>` +         // cuello
    `<rect x="9.8" y="12" width="12.4" height="15.8" rx="5.2" fill="url(#${g})" ${STK}/>` + // cuerpo
    `<rect x="9.8" y="18" width="12.4" height="4.2" fill="rgba(255,255,255,.85)"/>` + // etiqueta
    gloss(13, 16, 1.6, 2.6));
}
// Vitaminas (EV): frasco de cápsulas, fiel a la saga (tarrito + tapa + etiqueta), color por stat.
// Tinte por stat vía `color`; si no se pasa, gris neutro. Cápsula bicolor (clara/oscura) adentro.
function vitaminaSvg(size, color) {
  const c = color || '#9aa0a6';
  const g = uid(), lo = `color-mix(in srgb, ${c} 72%, #000 28%)`;
  return svg(size, `<defs>${linGrad(g, `color-mix(in srgb, ${c} 88%, #fff 12%)`, lo)}</defs>` +
    `<rect x="11" y="5.5" width="10" height="3.4" rx="1.1" fill="#cfd4dd" ${STK}/>` +       // tapa
    `<rect x="8.4" y="8.4" width="15.2" height="19.4" rx="3.4" fill="url(#${g})" ${STK}/>` + // tarrito
    `<rect x="8.4" y="14.2" width="15.2" height="8.4" fill="rgba(255,255,255,.9)"/>` +       // etiqueta blanca
    `<rect x="10.6" y="16.4" width="10.8" height="1.5" rx=".7" fill="${lo}"/>` +              // renglones de la etiqueta
    `<rect x="10.6" y="19.2" width="7.4" height="1.4" rx=".7" fill="${lo}" opacity=".7"/>` +
    `<g transform="rotate(-30 16 11.4)">` +                                                   // cápsula bicolor
      `<rect x="12.4" y="9.4" width="7.2" height="4" rx="2" fill="${c}" stroke="rgba(0,0,0,.32)" stroke-width=".8"/>` +
      `<path d="M14 9.4a2 2 0 0 0-1.6 .8 2 2 0 0 0 0 2.4 2 2 0 0 0 1.6 .8h2V9.4Z" fill="#f4f6fa"/>` +
    `</g>` +
    gloss(11.5, 11.5, 1.4, 2.2));
}
// Revivir: cruz amarilla con borde teal (paleta canónica del Revive).
function reviveSvg(size) {
  const g = uid();
  return svg(size, `<defs>${linGrad(g, '#ffe45a', '#e0a000')}</defs>` +
    `<path d="M13.2 6 H18.8 V13.2 H26 V18.8 H18.8 V26 H13.2 V18.8 H6 V13.2 H13.2 Z" fill="url(#${g})" stroke="#1f7a86" stroke-width="1.4" stroke-linejoin="round"/>` +
    gloss(13, 12, 1.3, 2));
}
// Baya (EV-): fruta redonda lustrosa con hojita + tallo, color por stat. Misma familia (contorno + brillo).
// Cuerpo en radial para volumen; surco vertical sutil tipo baya de la saga.
function bayaSvg(size, color) {
  const c = color || '#9aa0a6';
  const g = uid();
  const hi = `color-mix(in srgb, ${c} 64%, #fff 36%)`, lo = `color-mix(in srgb, ${c} 78%, #000 22%)`;
  const stem = `color-mix(in srgb, ${c} 50%, #5a3a1a 50%)`;
  return svg(size, `<defs>${radGrad(g, hi, lo)}</defs>` +
    `<path d="M16 8.6 C10.5 8.4 9 6 9 4.2 C12 4.4 14.4 5.6 16 8 C13.8 6 11.4 5.4 10.4 5.6 C12 6.4 14.4 7.4 16 8.6 Z" fill="#5aa84a" stroke="rgba(0,0,0,.32)" stroke-width=".8" stroke-linejoin="round"/>` + // hojita
    `<path d="M16 8.6 L16.4 4.4" fill="none" stroke="${stem}" stroke-width="1.6" stroke-linecap="round"/>` + // tallo
    `<circle cx="16" cy="18.5" r="9.5" fill="url(#${g})" stroke="rgba(0,0,0,.42)" stroke-width="1"/>` +     // cuerpo
    `<path d="M16 9.6 V27" fill="none" stroke="rgba(0,0,0,.16)" stroke-width="1"/>` +                        // surco
    gloss(12.5, 15, 2, 3));
}
// Borrón EV: goma de borrar (cuerpo con franja + manga azul) — neutro, mismo contorno/brillo que la familia.
function borradorSvg(size) {
  const g = uid(), gs = uid();
  return svg(size, `<defs>${linGrad(g, '#ffd9e0', '#e88aa0')}${linGrad(gs, '#7cc4f2', '#2f7bd6')}</defs>` +
    `<g transform="rotate(-32 16 16)">` +
      `<rect x="7.5" y="11" width="17" height="11" rx="2.4" fill="url(#${g})" ${STK}/>` +     // cuerpo de goma
      `<rect x="7.5" y="11" width="17" height="4.4" rx="2.4" fill="url(#${gs})" ${STK}/>` +   // manga azul
      `<rect x="7.5" y="13.6" width="17" height="1.8" fill="rgba(0,0,0,.22)"/>` +              // borde manga/goma
      `<path d="M9.2 19.5 H22.8" fill="none" stroke="rgba(255,255,255,.45)" stroke-width="1" stroke-linecap="round"/>` + // brillo inferior
      gloss(12, 17.5, 2.2, 1.3) +
    `</g>` +
    `<path d="M9 24 q1.4 2 3 0 q1.4 2 3 0" fill="none" stroke="rgba(120,90,60,.5)" stroke-width="1" stroke-linecap="round"/>`); // virutas
}
const CONSUM = {
  pocion:      { kind: 'spray', c: ['#ff9e5a', '#e0561f'] },   // naranja
  superpocion: { kind: 'spray', c: ['#ff7a8a', '#d62246'] },   // rojo/rosa
  pocionmax:   { kind: 'spray', c: ['#ffd24a', '#e0a400'] },   // dorado
  antidoto:      { kind: 'vial', c: ['#c79be6', '#7b34c0'] },  // veneno (morado)
  antiquemar:    { kind: 'vial', c: ['#ffb07a', '#e0561f'] },  // quemadura (naranja)
  antiparalisis: { kind: 'vial', c: ['#ffe066', '#e0a400'] },  // parálisis (amarillo)
  despertar:     { kind: 'vial', c: ['#9fc4f2', '#2a6fb0'] },  // sueño (azul)
  antihielo:     { kind: 'vial', c: ['#a8e8f0', '#3fb0d8'] },  // congelado (celeste)
  curatotal:     { kind: 'vial', c: ['#ffd0e0', '#e0709a'] },  // cura total (rosa)
};

// color de cada vitamina por índice de stat (0=PS … 5=Vel) — paleta canon de stats.
const VIT_COLOR = ['#ff5959', '#f5ac78', '#fae078', '#9db7f5', '#a7db8d', '#fa92b2'];

// itemSvg(id, size, color?) — `color` solo lo usa 'vitamina' (tinte por stat). Para los demás se ignora.
export function itemSvg(id, size = 22, color = null) {
  if (id === 'discoenlace') return discoSvg(size);
  if (id === 'pokeball' || id === 'ball0') return ballSvg(0, size);
  if (id === 'superball' || id === 'ball1') return ballSvg(1, size);
  if (id === 'ultraball' || id === 'ball2') return ballSvg(2, size);
  if (id === 'ballveloz') return ballSvg('veloz', size);
  if (id === 'ballturno') return ballSvg('turno', size);
  if (id === 'ballred') return ballSvg('red', size);
  if (id === 'ballrepe') return ballSvg('repeticion', size);
  if (id === 'ballmaster') return ballSvg('master', size);
  if (id === 'ballxeneize') return ballSvg('xeneize', size);
  if (id === 'balldusk') return ballSvg('dusk', size);
  if (id === 'revivir') return reviveSvg(size);
  if (id === 'vitamina') return vitaminaSvg(size, color);
  if (id === 'baya') return bayaSvg(size, color);
  if (id === 'borrador') return borradorSvg(size);
  if (CONSUM[id]) return CONSUM[id].kind === 'spray' ? sprayBottle(CONSUM[id].c, size) : vialBottle(CONSUM[id].c, size);
  if (STONES[id]) return gemSvg(STONES[id].c, STONES[id].em, size);
  return gemSvg(STONES.piedra.c, STONES.piedra.em, size);   // comodín
}
// índice de stat → color de la vitamina de ese stat (para la tienda, que tinta por `ev`).
export const vitaminaColor = (statIdx) => VIT_COLOR[statIdx] || VIT_COLOR[0];
// índice de stat → color de la baya de ese stat (misma paleta canon que las vitaminas).
export const bayaColor = (statIdx) => VIT_COLOR[statIdx] || VIT_COLOR[0];

// ───────────────────────── pokeballs ─────────────────────────
// Familia de Pokéballs: misma silueta (domo superior + banda negra + botón central) y mismo
// acabado (gradiente vertical, brillo arriba-izq). Cambian color del domo + `arcs` (marcas del domo).
// `bot` opcional reemplaza el color de la mitad inferior (default blanco). `extra` dibuja por
// fuera del cuerpo (p.ej. esferas de la Master).
//   numéricas: 0=Poké(rojo) · 1=Super/Great(azul+arcos rojos) · 2=Ultra(amarillo+negro)
//   string:    veloz · turno · red · repeticion · master · xeneize
const BALLS = {
  0: { top: ['#ff5a4d', '#d11f1f'], arcs: '' },
  1: { top: ['#3a9ae0', '#1f63c4'], arcs: '<path d="M6 11c3-3 6-4 10-4M26 11c-3-3-6-4-10-4" fill="none" stroke="#d11f1f" stroke-width="2.4" stroke-linecap="round"/>' },
  2: { top: ['#f7d24a', '#e0a400'], arcs: '<path d="M16 4v9M8 7l4 5M24 7l-4 5" fill="none" stroke="#222" stroke-width="2.2" stroke-linecap="round"/>' },
  // Veloz (Quick Ball): domo azul con destellos amarillos radiando del botón.
  veloz: { top: ['#2f7bd6', '#1b4fa6'], arcs:
    '<path d="M16 4v9M9 6.5l4.5 6M23 6.5l-4.5 6M5 12l7 2.2M27 12l-7 2.2" fill="none" stroke="#f6d23a" stroke-width="2.1" stroke-linecap="round"/>' },
  // Turno (Timer Ball): domo blanco con marcas rojas radiales (esfera de reloj).
  turno: { top: ['#f4f6f8', '#cfd4da'], arcs:
    '<path d="M16 3.4v3.6M27.8 14H24.2M4.2 14H7.8M24.5 6.4l-2.5 2.5M7.5 6.4l2.5 2.5" fill="none" stroke="#d11f1f" stroke-width="2.1" stroke-linecap="round"/>' +
    '<path d="M16 14V8.5l3.4 3.4" fill="none" stroke="#d11f1f" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>' },
  // Red (Net Ball): domo celeste con trama de red.
  red: { top: ['#2bc6d6', '#1488b0'], arcs:
    '<path d="M9 6l5 8M16 4.5l0 9.5M23 6l-5 8M5 11l9 2.5M27 11l-9 2.5" fill="none" stroke="#0c5570" stroke-width="1.5" stroke-linecap="round" opacity="0.85"/>' },
  // Repetición (Repeat Ball): cuerpo Ultra (amarillo) con franja roja y flechas de "repetir".
  repeticion: { top: ['#f7d24a', '#e0a400'], arcs:
    '<path d="M3.6 9.5h24.8" fill="none" stroke="#d11f1f" stroke-width="2.6"/>' +
    '<path d="M11 6.4l-2 1.7 2 1.7M21 6.4l2 1.7-2 1.7" fill="none" stroke="#7a1010" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>' +
    '<path d="M9.5 8.1h13" fill="none" stroke="#7a1010" stroke-width="1.7" stroke-linecap="round"/>' },
  // Master: domo morado con dos esferas rosas a los lados y "M" blanca.
  master: { top: ['#9038c8', '#5e1b96'], extra:
      '<circle cx="9.5" cy="9.5" r="3" fill="#f06fb8"/><circle cx="22.5" cy="9.5" r="3" fill="#f06fb8"/>' +
      '<circle cx="9.5" cy="9.5" r="3" fill="none" stroke="#c43e87" stroke-width="0.9"/>' +
      '<circle cx="22.5" cy="9.5" r="3" fill="none" stroke="#c43e87" stroke-width="0.9"/>',
    arcs: '<path d="M12.5 13.5v-4l3.5 2.4 3.5-2.4v4" fill="none" stroke="#fff" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/>' },
  // Xeneize (Boca Juniors): domo azul profundo con banda dorada. Misma silueta de Pokéball.
  xeneize: { top: ['#103a86', '#0a2e6b'], arcs:
    '<rect x="3.4" y="9.2" width="25.2" height="3.4" fill="#f2c200"/>' +
    '<rect x="3.4" y="9.2" width="25.2" height="3.4" fill="none" stroke="#c79a00" stroke-width="0.6"/>' },
  // Dusk (Dusk Ball): domo verde oscuro casi negro con cresta verde y dos círculos rojo-naranja.
  dusk: { top: ['#2f5a44', '#0e1c18'], arcs:
    '<path d="M4 13.4c3-3 6.4-4.4 12-4.4s9 1.4 12 4.4" fill="none" stroke="#3d8f5a" stroke-width="2.2" stroke-linecap="round"/>' +
    '<circle cx="10" cy="9.6" r="2.3" fill="#ef5a2a"/><circle cx="22" cy="9.6" r="2.3" fill="#ef5a2a"/>' +
    '<circle cx="10" cy="9.6" r="2.3" fill="none" stroke="#a8331a" stroke-width="0.8"/>' +
    '<circle cx="22" cy="9.6" r="2.3" fill="none" stroke="#a8331a" stroke-width="0.8"/>' },
};
export function ballSvg(tier = 0, size = 22) {
  const b = BALLS[tier] || BALLS[0]; const g = uid(), gb = uid();
  return svg(size,
    `<defs>${linGrad(g, b.top[0], b.top[1])}${linGrad(gb, b.bot ? b.bot[0] : '#ffffff', b.bot ? b.bot[1] : '#d6d9de')}</defs>` +
    '<circle cx="16" cy="16" r="13" fill="#1c1c1f"/>' +
    `<path d="M3 16a13 13 0 0 1 26 0Z" fill="url(#${g})"/>` +
    `<path d="M3 16a13 13 0 0 0 26 0Z" fill="url(#${gb})"/>` +
    (b.arcs || '') +
    '<rect x="3" y="14.6" width="26" height="2.8" fill="#1c1c1f"/>' +
    '<circle cx="16" cy="16" r="4.6" fill="#1c1c1f"/>' +
    '<circle cx="16" cy="16" r="3" fill="#fff"/>' +
    '<circle cx="16" cy="16" r="1.3" fill="#cfd2d8"/>' +
    '<circle cx="11.5" cy="10.5" r="2.2" fill="rgba(255,255,255,.45)"/>' +
    (b.extra || ''));
}

// ───────────────────────── medallas (48) ─────────────────────────
// cfg por gimnasio: [shape, colorA, colorB, emblema?]. shape ∈ SHAPES. Reborde dorado tipo insignia.
const BADGES = {
  kanto: [
    ['octagon', '#a7adb5', '#5f6368'], ['raindrop', '#5cb3ec', '#1f6dbf'],
    ['star8', '#ffd23f', '#e08a00', 'bolt'], ['flower', '#ff7a59', '#ff3d6e'],
    ['heart', '#ff8ec4', '#e0246f'], ['circle', '#b06be0', '#7320b8'],
    ['flame', '#ff7a3c', '#c81e0f'], ['leaf', '#74c95f', '#2f8f3e'],
  ],
  johto: [
    ['wing', '#d2dbe6', '#8094ad'], ['hexagon', '#f4cf3a', '#c79400', 'sun'],
    ['circle', '#ecca70', '#b8923a'], ['diamond', '#bcccd9', '#7e95a8'],
    ['star5', '#7ab4e4', '#2a6fb0', 'bolt'], ['crystal', '#cf945f', '#8a5a2b'],
    ['snowflake', '#a8e6f2', '#3fb0d8'], ['triangle', '#e87ad6', '#a02f8f'],
  ],
  hoenn: [
    ['octagon', '#bda078', '#7a5f3f'], ['circle', '#e85a4d', '#b02a20', 'flame'],
    ['gear', '#f4cf3a', '#c89000'], ['flame', '#ff8a4c', '#d83a10'],
    ['diamond', '#9be0a0', '#3fae5a'], ['wing', '#d4e6f2', '#8fb8d0'],
    ['circle', '#d77be0', '#9b34c0', 'sparkle'], ['raindrop', '#62a8e6', '#2060b0'],
  ],
  sinnoh: [
    ['circle', '#52525c', '#222228'], ['leaf', '#5cc05f', '#256d2c'],
    ['square', '#cf7a4c', '#8a4a2b'], ['hexagon', '#88b85f', '#4a7a2f'],
    ['diamond', '#e6bf70', '#a8822f', 'sparkle'], ['octagon', '#727a8a', '#3a3f4a'],
    ['crystal', '#b2eef2', '#48b8d8'], ['star8', '#f4d44f', '#d89a10', 'sun'],
  ],
  unova: [
    ['triangle', '#9bd6e6', '#3f90b0'], ['shield', '#f4ce4f', '#c89a10'],
    ['hexagon', '#b4d44f', '#6f8f1f'], ['star8', '#ffd23f', '#e08a00', 'bolt'],
    ['circle', '#cf9f5f', '#8a5f2b'], ['wing', '#bccbd9', '#7e95a8'],
    ['snowflake', '#a8e6f2', '#3fb0d8'], ['star5', '#e87a7a', '#b02a2a'],
  ],
  kalos: [
    ['circle', '#e85a4d', '#b02a20'], ['triangle', '#cfae70', '#8a6f3a'],
    ['octagon', '#e8843c', '#b04a10'], ['leaf', '#74c95f', '#2f8f3e'],
    ['star8', '#f4cf3a', '#caa000', 'bolt'], ['star5', '#f7aee6', '#d060b0'],
    ['circle', '#b06be0', '#7b34c0', 'sparkle'], ['mountain', '#b2eef2', '#48b8d8'],
  ],
  alola: [
    ['gear', '#4fd0c0', '#1f8f88'], ['square', '#ffae4c', '#d87a10'],
    ['spiral', '#b06be0', '#7320b8'], ['hexagon', '#7a8aa0', '#3a4658'],
    ['diamond', '#ffd23f', '#e0a400'], ['circle', '#5cb3ec', '#1f6dbf', 'sun'],
    ['octagon', '#5cc08f', '#2f8f5f'], ['star8', '#ffd86b', '#e08a00', 'sparkle'],
  ],
  galar: [
    ['spiral', '#a07be8', '#6a32c0'], ['circle', '#6ea8f0', '#2a5fc0', 'crescent'],
    ['hexagon', '#7b6fe0', '#3a2fa8'], ['diamond', '#4fc0c8', '#1f8088'],
    ['square', '#5cc8e0', '#2080a8'], ['octagon', '#9a6fe0', '#5a2fa0'],
    ['triangle', '#f0b44c', '#c07a10'], ['star8', '#ffd86b', '#d8a020', 'sparkle'],
  ],
  paldea: [
    ['circle', '#f0934c', '#c05a10'], ['hexagon', '#e85a4d', '#a82820'],
    ['square', '#f0b84c', '#c08810'], ['triangle', '#f08060', '#c04830'],
    ['spiral', '#e06bb0', '#a02870'], ['octagon', '#4fc0a0', '#1f8068'],
    ['diamond', '#6ea8f0', '#2a5fc0'], ['star8', '#ffd86b', '#e0a000', 'sun'],
  ],
};

export function badgeSvg(region, i, won = true, size = 28) {
  const cfg = (BADGES[region] || BADGES.kanto)[i] || ['circle', '#9aa0a6', '#5f6368'];
  const [shape, ca, cb, em] = cfg;
  const g = uid();
  const colA = won ? ca : '#8a8f99', colB = won ? cb : '#54585f';
  const rim = won ? '#ffd86b' : '#9aa0a6';
  let inner = (SHAPES[shape] || SHAPES.circle)();
  inner = inner.replace(/__F__/g, `fill="url(#${g})" stroke="${rim}" stroke-width="1.6" stroke-linejoin="round"`)
    .replace(/__LF__/g, 'fill="none" stroke="rgba(255,255,255,.5)" stroke-width="1"')
    .replace(/__SF__/g, `stroke="url(#${g})"`)
    .replace(/__ST__/g, `stroke="url(#${g})"`);
  const emblem = won && em ? (EMBLEM[em] || '') : '';
  const op = won ? '' : ' opacity="0.5"';
  return svg(size, `<defs>${linGrad(g, colA, colB)}</defs><g${op}>${inner}${emblem}</g>`);
}
