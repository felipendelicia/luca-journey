import { contieneGroseria } from './groserias';

describe('contieneGroseria', () => {
  it('bloquea términos claramente ofensivos (con acentos/espacios/repes)', () => {
    for (const s of ['hijodeputa', 'Hijo De Putaa', 'fuck you', 'maricon', 'putamadre', 'NAZI88', 'cónchatumadre']) {
      expect(contieneGroseria(s)).toBe(true);
    }
  });
  it('NO bloquea palabras/nombres inocentes (sin falsos positivos)', () => {
    for (const s of ['computadora', 'disputa', 'computo', 'vergara', 'pijama', 'rapero', 'paraguas',
      'ortografia', 'cacao', 'penelope', 'controlo', 'felipo', 'lucario', 'ash_kanto', 'tortilla', 'sexto']) {
      expect(contieneGroseria(s)).toBe(false);
    }
  });
});
