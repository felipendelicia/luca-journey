import test from 'node:test';
import assert from 'node:assert/strict';
import { probCaptura, pisoIV, sincronizaNat, fleeProb, baseCaptura, catchBall } from './safari-core.js';

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
