import test from 'node:test';
import assert from 'node:assert/strict';
import { probCaptura, pisoIV, sincronizaNat, fleeProb, baseCaptura, catchBall } from './safari-core.js';
import { shinyChance, pisoRacha, esNoche, biomaActual, rolarTam } from './safari-core.js';

const poke = { key: 'pokeball', catch: 1 };
const ultra = { key: 'ultraball', catch: 2 };
const master = { key: 'master' };
const veloz = { key: 'veloz' };
const turno = { key: 'turno' };
const red = { key: 'red' };
const repe = { key: 'repeticion' };
const ctx = (o = {}) => ({ tiroN: 1, calidad: 'Normal', tiposWild: [], vistoYa: false, ...o });

test('baseCaptura: comunes alto, legendarios bajo, piso 0.12', () => {
  assert.ok(baseCaptura(1) > baseCaptura(10));
  assert.ok(baseCaptura(10) >= 0.12);
});
test('probCaptura: Ultra > Poké', () => {
  assert.ok(probCaptura(5, ultra, ctx()) > probCaptura(5, poke, ctx()));
});
test('probCaptura: mejor calidad sube', () => {
  assert.ok(probCaptura(5, poke, ctx({ calidad: 'Excelente' })) > probCaptura(5, poke, ctx({ calidad: 'Normal' })));
});
test('probCaptura: Master = 1', () => {
  assert.equal(probCaptura(10, master, ctx()), 1);
});
test('probCaptura: clamp 0..1', () => {
  const p = probCaptura(1, ultra, ctx({ calidad: 'Excelente' }));
  assert.ok(p <= 1 && p >= 0);
});
test('Veloz: ×4 primer tiro, ×1 luego', () => {
  assert.equal(catchBall(veloz, ctx({ tiroN: 1 })), 4);
  assert.equal(catchBall(veloz, ctx({ tiroN: 2 })), 1);
});
test('Turno: escala con tiroN', () => {
  assert.ok(catchBall(turno, ctx({ tiroN: 3 })) > catchBall(turno, ctx({ tiroN: 1 })));
});
test('Red: ×3 vs Bicho/Agua, ×1 si no', () => {
  assert.equal(catchBall(red, ctx({ tiposWild: ['Agua'] })), 3);
  assert.equal(catchBall(red, ctx({ tiposWild: ['Fuego'] })), 1);
});
test('Repetición: ×3 si visto', () => {
  assert.equal(catchBall(repe, ctx({ vistoYa: true })), 3);
  assert.equal(catchBall(repe, ctx({ vistoYa: false })), 1);
});
test('pisoIV: Excelente sube los 2 más bajos a 31', () => {
  assert.deepEqual(pisoIV([5, 20, 2, 30, 31, 10], 'Excelente'), [31, 20, 31, 30, 31, 10]);
});
test('pisoIV: otras calidades no tocan', () => {
  assert.deepEqual(pisoIV([5, 20, 2, 30, 31, 10], 'Genial'), [5, 20, 2, 30, 31, 10]);
});
test('sincronizaNat: synchronize → nat del compañero; otra → null', () => {
  assert.equal(sincronizaNat('synchronize', 7), 7);
  assert.equal(sincronizaNat('overgrow', 7), null);
});
test('fleeProb: crece con la rareza, en [0.1, 0.5]', () => {
  assert.ok(fleeProb(10) > fleeProb(1));
  assert.ok(fleeProb(1) >= 0.1 && fleeProb(10) <= 0.5);
});
test('shinyChance: racha 0 = 0.01, crece, cap 0.08', () => {
  assert.equal(shinyChance(0), 0.01);
  assert.ok(shinyChance(25) > shinyChance(10));
  assert.equal(shinyChance(1000), 0.08);
});
test('pisoRacha: umbrales 15/30/50', () => {
  assert.equal(pisoRacha(14), 0);
  assert.equal(pisoRacha(15), 1);
  assert.equal(pisoRacha(30), 2);
  assert.equal(pisoRacha(50), 3);
});
test('esNoche: 23h noche, 12h día, 5h noche', () => {
  assert.equal(esNoche(new Date(2026, 0, 1, 23, 0)), true);
  assert.equal(esNoche(new Date(2026, 0, 1, 12, 0)), false);
  assert.equal(esNoche(new Date(2026, 0, 1, 5, 0)), true);
});
test('biomaActual: determinista, rota cada 10 min', () => {
  assert.equal(biomaActual(0), 'hierba');
  assert.equal(biomaActual(599999), 'hierba');
  assert.equal(biomaActual(600000), 'agua');
  assert.equal(biomaActual(1200000), 'cueva');
  assert.equal(biomaActual(1800000), 'hierba');
});
test('catchBall dusk: noche o cueva → 3.5; día+superficie → 1', () => {
  const dusk = { key: 'dusk' };
  assert.equal(catchBall(dusk, ctx({ noche: true, bioma: 'hierba' })), 3.5);
  assert.equal(catchBall(dusk, ctx({ noche: false, bioma: 'cueva' })), 3.5);
  assert.equal(catchBall(dusk, ctx({ noche: false, bioma: 'hierba' })), 1);
});
test('rolarTam: extremos y rango', () => {
  assert.equal(rolarTam(() => 0.01), 'XXS');
  assert.equal(rolarTam(() => 0.5), 'M');
  assert.equal(rolarTam(() => 0.99), 'XXL');
});
