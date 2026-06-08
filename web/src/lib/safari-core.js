// safari-core.js — lógica PURA del safari (captura / escape / tasación). Sin DOM, sin JSON, sin estado.
// Testeable con `node --test src/lib/safari-core.test.mjs`. La orquestación (estado) vive en coleccion.js.

// un tiro flojo (Normal) ahora PENALIZA la captura; uno bueno la sube. La calidad del anillo importa.
export const MULT_CALIDAD = { Normal: 0.65, Bien: 1.0, Genial: 1.5, Excelente: 2.2 };

// captura base por tier de rareza (1..10): comunes ~0.5, legendarios bajo. Más difícil que antes (era ~0.95).
export const baseCaptura = (tier) => Math.max(0.06, Math.min(0.5, 0.55 - tier * 0.06));

// modificador de captura de la ball (puede depender del contexto del encuentro).
// ctx = { tiroN, calidad, tiposWild: string[], vistoYa: boolean }
export function catchBall(ballDef, ctx) {
  switch (ballDef.key) {
    case 'master': return Infinity;
    case 'veloz': return ctx.tiroN === 1 ? 4 : 1;
    case 'turno': return 1 + ctx.tiroN * 0.3;
    case 'red': return (ctx.tiposWild || []).some((t) => t === 'Bicho' || t === 'Agua') ? 3 : 1;
    case 'repeticion': return ctx.vistoYa ? 3 : 1;
    case 'dusk': return (ctx.noche || ctx.bioma === 'cueva') ? 3.5 : 1;
    default: return ballDef.catch ?? 1;   // poke 1, super 1.5, ultra 2, xeneize 2
  }
}

// probabilidad de captura [0..1]. Master = 1.
export function probCaptura(tier, ballDef, ctx) {
  if (ballDef.key === 'master') return 1;
  const mult = MULT_CALIDAD[ctx.calidad] ?? 1;
  const p = baseCaptura(tier) * catchBall(ballDef, ctx) * mult;
  return Math.max(0, Math.min(1, p));
}

// prob. de huida tras un fallo (raros huyen más), acotada a [0.2, 0.6]. Más alta que antes (huyen más seguido).
export const fleeProb = (tier) => Math.max(0.20, Math.min(0.6, 0.20 + tier * 0.04));

// piso de IVs por Excelente: SOLO el índice con menor IV → 31 (antes 2; ahora los IVs altos son más raros).
export function pisoIV(ivs, calidad) {
  if (calidad !== 'Excelente') return ivs.slice();
  const out = ivs.slice();
  const orden = out.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
  for (let k = 0; k < 1; k++) out[orden[k][1]] = 31;
  return out;
}

// Sincronía (pura): hab y nat del compañero → nat o null.
export const sincronizaNat = (compHab, compNat) => compHab === 'synchronize' ? compNat : null;

// ───────────────────────── Fase 2: racha / hora / bioma / tamaños ─────────────────────────
// chance de shiny según la racha de capturas seguidas. Base 0.1% (1/1000), cap ~0.67% (~1/150).
// (En los juegos reales es ~1/4096; acá un poco más generoso, pero las shinies siguen siendo un evento.)
export const shinyChance = (racha) => Math.min(0.0067, 0.001 * (1 + (racha || 0) * 0.1));
// IVs perfectos garantizados por racha alta. Umbrales más altos y tope 2 (antes 15/30/50 → 1/2/3): IVs altos raros.
export const pisoRacha = (racha) => racha >= 60 ? 2 : racha >= 30 ? 1 : 0;
// ¿es de noche? (reloj del dispositivo). Noche = antes de las 6 o desde las 19.
export const esNoche = (now = new Date()) => { const h = now.getHours(); return h < 6 || h >= 19; };
// bioma actual: rota Hierba→Agua→Cueva cada 10 min, determinista por el reloj.
export const biomaActual = (ms = Date.now()) => ['hierba', 'agua', 'cueva'][Math.floor(ms / 600000) % 3];
// tamaño del ejemplar (cosmético). Casi siempre Normal; colas raras XXS/XXL.
export function rolarTam(rng = Math.random) {
  const r = rng();
  return r < 0.03 ? 'XXS' : r < 0.12 ? 'S' : r > 0.97 ? 'XXL' : r > 0.88 ? 'L' : 'M';
}
