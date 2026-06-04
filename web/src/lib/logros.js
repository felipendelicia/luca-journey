// logros.js — logros desbloqueables, calculados desde el progreso (localStorage).
import { estado } from './coleccion.js';

export const LOGROS = [
  { id: 'primer-ej', ico: '🌱', nombre: 'Primer paso', desc: 'Resolvé tu primer ejercicio', check: (c) => c.ejHechos >= 1 },
  { id: 'aprendiz', ico: '📖', nombre: 'Aprendiz', desc: 'Resolvé 10 ejercicios', check: (c) => c.ejHechos >= 10 },
  { id: 'estudioso', ico: '🎓', nombre: 'Estudioso', desc: 'Resolvé 50 ejercicios', check: (c) => c.ejHechos >= 50 },
  { id: 'empollon', ico: '🧠', nombre: 'Empollón', desc: 'Resolvé 100 ejercicios', check: (c) => c.ejHechos >= 100 },
  { id: 'erudito', ico: '🏅', nombre: 'Erudito', desc: 'Resolvé TODOS los ejercicios', check: (c) => c.totalEj > 0 && c.ejHechos >= c.totalEj },
  { id: 'kanto', ico: '🔴', nombre: 'Campeón de Kanto', desc: 'Completá la región Kanto', check: (c) => c.reg.kanto },
  { id: 'johto', ico: '⚪', nombre: 'Campeón de Johto', desc: 'Completá la región Johto', check: (c) => c.reg.johto },
  { id: 'hoenn', ico: '🟢', nombre: 'Campeón de Hoenn', desc: 'Completá la región Hoenn', check: (c) => c.reg.hoenn },
  { id: 'maestro', ico: '👑', nombre: 'Maestro Pokémon', desc: 'Completá todas las regiones', check: (c) => c.regiones.length > 0 && c.regiones.every((r) => c.reg[r]) },
  { id: 'primer-poke', ico: '🔴', nombre: '¡Te elijo a ti!', desc: 'Atrapá tu primer Pokémon', check: (c) => c.unicos >= 1 },
  { id: 'coleccionista', ico: '📕', nombre: 'Coleccionista', desc: 'Atrapá 50 Pokémon distintos', check: (c) => c.unicos >= 50 },
  { id: 'kantodex', ico: '🗺️', nombre: 'Pokédex de Kanto', desc: 'Atrapá los 151 de Kanto', check: (c) => c.kanto >= 151 },
  { id: 'todos', ico: '🌟', nombre: '¡Hay que atraparlos a todos!', desc: 'Atrapá los 386', check: (c) => c.unicos >= 386 },
  { id: 'shiny', ico: '✨', nombre: '¡Brilla!', desc: 'Atrapá un Pokémon shiny', check: (c) => c.shinies >= 1 },
  { id: 'cazashiny', ico: '💎', nombre: 'Cazador de shinies', desc: 'Atrapá 5 shinies', check: (c) => c.shinies >= 5 },
  { id: 'repetido', ico: '👯', nombre: 'De a montones', desc: 'Tené 5 del mismo Pokémon', check: (c) => c.maxRepe >= 5 },
];

export function contexto(temas) {
  const st = estado();
  const done = (slug, id) => localStorage.getItem(`ej:${slug}:${id}:ok`) === '1';
  let ejHechos = 0;
  for (const t of temas) for (const ex of t.ejercicios) if (done(t.slug, ex.id)) ejHechos++;

  const porReg = {};
  for (const t of temas) (porReg[t.region] ||= []).push(t);
  const reg = {};
  for (const [r, ts] of Object.entries(porReg)) {
    reg[r] = ts.every((t) => t.ejercicios.length && t.ejercicios.every((ex) => done(t.slug, ex.id)));
  }
  const ids = Object.keys(st.atrapados).map(Number);
  const valores = Object.values(st.atrapados);
  return {
    ejHechos,
    totalEj: temas.reduce((a, t) => a + t.ejercicios.length, 0),
    unicos: st.unicos,
    shinies: st.shiny.size,
    kanto: ids.filter((id) => id <= 151).length,
    maxRepe: valores.length ? Math.max(...valores) : 0,
    reg,
    regiones: Object.keys(porReg),
  };
}

export function evaluar(temas) {
  const c = contexto(temas);
  return LOGROS.map((l) => ({ ...l, cumplido: l.check(c) }));
}
