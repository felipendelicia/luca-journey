export type MapaAtrapados = Record<string, number>;

export function mapaInc(m: MapaAtrapados, k: string): MapaAtrapados {
  return { ...m, [k]: (m[k] || 0) + 1 };
}
export function mapaDec(m: MapaAtrapados, k: string): MapaAtrapados {
  const n = (m[k] || 0) - 1;
  const out = { ...m };
  if (n <= 0) delete out[k];
  else out[k] = n;
  return out;
}
export function arrTiene(a: number[], k: string): boolean {
  return a.includes(Number(k));
}
export function arrAdd(a: number[], k: string): number[] {
  return arrTiene(a, k) ? a : [...a, Number(k)];
}
export function arrDel(a: number[], k: string): number[] {
  return a.filter((x) => x !== Number(k));
}

export type Estado = Record<string, any>;
export type Item = { id: number | string; shiny?: boolean };

export function leerCol(estado: Estado) {
  const atra = JSON.parse((estado['col:atrapados'] as string) || '{}');
  const shiny = JSON.parse((estado['col:shiny'] as string) || '[]');
  return { atra: atra as MapaAtrapados, shiny: shiny as number[] };
}
export function escribirCol(estado: Estado, atra: MapaAtrapados, shiny: number[]): Estado {
  return { ...estado, 'col:atrapados': JSON.stringify(atra), 'col:shiny': JSON.stringify(shiny) };
}

// A entrega loteA a B; B entrega loteB a A. Valida multiplicidad + shiny sobre copias,
// luego aplica. Lanza con el label del lado que no cumple. Pura: no toca DB.
export function swapColeccion(
  estadoA: Estado, loteA: Item[], labelA: string,
  estadoB: Estado, loteB: Item[], labelB: string,
): { estadoA: Estado; estadoB: Estado } {
  let { atra: aAt, shiny: aSh } = leerCol(estadoA);
  let { atra: bAt, shiny: bSh } = leerCol(estadoB);

  const validar = (at: MapaAtrapados, sh: number[], lote: Item[], label: string) => {
    let tmp = { ...at };
    for (const it of lote) {
      const id = String(it.id);
      if ((tmp[id] || 0) < 1) throw new Error(`${label} no tiene suficiente ${id}`);
      if (it.shiny && !arrTiene(sh, id)) throw new Error(`${label} no tiene shiny ${id}`);
      tmp = mapaDec(tmp, id);
    }
  };
  validar(aAt, aSh, loteA, labelA);
  validar(bAt, bSh, loteB, labelB);

  for (const it of loteA) {
    const id = String(it.id);
    aAt = mapaDec(aAt, id); bAt = mapaInc(bAt, id);
    if (it.shiny) { aSh = arrDel(aSh, id); bSh = arrAdd(bSh, id); }
  }
  for (const it of loteB) {
    const id = String(it.id);
    bAt = mapaDec(bAt, id); aAt = mapaInc(aAt, id);
    if (it.shiny) { bSh = arrDel(bSh, id); aSh = arrAdd(aSh, id); }
  }
  return { estadoA: escribirCol(estadoA, aAt, aSh), estadoB: escribirCol(estadoB, bAt, bSh) };
}
