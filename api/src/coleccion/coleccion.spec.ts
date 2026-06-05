import { mapaInc, mapaDec, arrTiene, arrAdd, arrDel } from './coleccion';

describe('helpers coleccion', () => {
  it('mapaInc suma 1', () => {
    expect(mapaInc({ '25': 2 }, '25')).toEqual({ '25': 3 });
    expect(mapaInc({}, '7')).toEqual({ '7': 1 });
  });
  it('mapaDec resta y borra al llegar a 0', () => {
    expect(mapaDec({ '25': 2 }, '25')).toEqual({ '25': 1 });
    expect(mapaDec({ '25': 1 }, '25')).toEqual({});
  });
  it('arr add/del/tiene sin duplicar', () => {
    expect(arrTiene([25, 7], '25')).toBe(true);
    expect(arrAdd([25], '7')).toEqual([25, 7]);
    expect(arrAdd([25], '25')).toEqual([25]);
    expect(arrDel([25, 7], '25')).toEqual([7]);
  });
});
