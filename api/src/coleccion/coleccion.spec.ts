import { mapaInc, mapaDec, arrTiene, arrAdd, arrDel, swapColeccion, leerCol, escribirCol } from './coleccion';

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

const blob = (atra: Record<string, number>, shiny: number[] = [], balls = 0) => ({
  'col:atrapados': JSON.stringify(atra),
  'col:shiny': JSON.stringify(shiny),
  'col:balls': String(balls),
});

describe('swapColeccion', () => {
  it('mueve por cantidad: A da 25 -> B', () => {
    const a = blob({ '25': 2 });
    const b = blob({ '7': 1 });
    const { estadoA, estadoB } = swapColeccion(a, [{ id: 25 }], 'A', b, [], 'B');
    expect(leerCol(estadoA).atra).toEqual({ '25': 1 });
    expect(leerCol(estadoB).atra).toEqual({ '7': 1, '25': 1 });
  });
  it('mueve shiny en ambos sentidos', () => {
    const a = blob({ '25': 1 }, [25]);
    const b = blob({ '7': 1 }, [7]);
    const { estadoA, estadoB } = swapColeccion(a, [{ id: 25, shiny: true }], 'A', b, [{ id: 7, shiny: true }], 'B');
    expect(leerCol(estadoA).shiny).toEqual([7]);
    expect(leerCol(estadoB).shiny).toEqual([25]);
  });
  it('falla si A no tiene stock', () => {
    expect(() => swapColeccion(blob({}), [{ id: 25 }], 'A', blob({}), [], 'B')).toThrow(/A no tiene/);
  });
  it('falla si pide shiny que no tiene', () => {
    expect(() => swapColeccion(blob({ '25': 1 }, []), [{ id: 25, shiny: true }], 'A', blob({}), [], 'B')).toThrow(/shiny/);
  });
});
