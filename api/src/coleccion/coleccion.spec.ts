import { mapaInc, mapaDec, arrTiene, arrAdd, arrDel, swapColeccion, leerCol, escribirCol, swapInstancias } from './coleccion';

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

const pcBlob = (pc: any[]) => ({ 'col:pc': JSON.stringify(pc) });
describe('swapInstancias (intercambio por instancia)', () => {
  it('mueve la INSTANCIA exacta conservando nivel/shiny/mote y reasigna iid', () => {
    const a = pcBlob([{ iid: 'a1', id: 6, nivel: 50, shiny: true, movs: [7], mote: 'Drako' }]);
    const b = pcBlob([{ iid: 'b1', id: 25, nivel: 12, shiny: false, movs: [] }]);
    const { estadoA, estadoB } = swapInstancias(a, ['a1'], 'A', b, ['b1'], 'B');
    const pcA = JSON.parse(estadoA['col:pc']); const pcB = JSON.parse(estadoB['col:pc']);
    // A ahora tiene el Pikachu de B; B tiene el Charizard Nv50 shiny con su mote y movs
    expect(pcA).toHaveLength(1); expect(pcA[0].id).toBe(25);
    expect(pcB).toHaveLength(1);
    expect(pcB[0]).toMatchObject({ id: 6, nivel: 50, shiny: true, mote: 'Drako', movs: [7] });
    expect(pcB[0].iid).not.toBe('a1');   // iid nuevo al recibir
    // derivados recomputados
    expect(JSON.parse(estadoB['col:atrapados'])).toEqual({ '6': 1 });
    expect(JSON.parse(estadoB['col:shiny'])).toEqual([6]);
    expect(JSON.parse(estadoA['col:vistos'])).toContain(25);
  });
  it('falla si el oferente ya no tiene esa instancia', () => {
    expect(() => swapInstancias(pcBlob([]), ['x'], 'A', pcBlob([]), [], 'B')).toThrow(/A ya no tiene/);
  });
});
