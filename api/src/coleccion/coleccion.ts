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
  // tolerante a JSON corrupto en la nube: no tirar 500 en un intercambio por data inválida.
  const p = (v: any, def: any) => { try { return JSON.parse((v as string) || JSON.stringify(def)); } catch { return def; } };
  return { atra: p(estado['col:atrapados'], {}) as MapaAtrapados, shiny: p(estado['col:shiny'], []) as number[] };
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

// ───────────────────────── intercambio por INSTANCIA (v2) ─────────────────────────
export type Instancia = { iid: string; id: number; nivel?: number; exp?: number; shiny?: boolean; movs?: number[]; mote?: string; creado?: number };
export type ItemInst = { iid: string; id?: number; nivel?: number; shiny?: boolean; mote?: string };
const nuevoIid = () => 'i' + Date.now().toString(36) + Math.random().toString(36).slice(2, 8);

function leerPC(estado: Estado): Instancia[] { try { return JSON.parse((estado['col:pc'] as string) || '[]'); } catch { return []; } }
// reescribe col:pc + recomputa los derivados (atrapados/shiny/vistos-acumulado) desde el PC.
function escribirPC(estado: Estado, pc: Instancia[]): Estado {
  const atra: MapaAtrapados = {}; const shiny = new Set<number>(); const vistos = new Set<number>();
  for (const m of pc) { const id = Number(m.id); atra[id] = (atra[id] || 0) + 1; vistos.add(id); if (m.shiny) shiny.add(id); }
  let vistosPrev: number[] = []; try { vistosPrev = JSON.parse((estado['col:vistos'] as string) || '[]'); } catch {}
  for (const v of vistosPrev) vistos.add(Number(v));   // no perder especies ya vistas
  return {
    ...estado,
    'col:pc': JSON.stringify(pc),
    'col:atrapados': JSON.stringify(atra),
    'col:shiny': JSON.stringify([...shiny]),
    'col:vistos': JSON.stringify([...vistos]),
  };
}

// A entrega las instancias `iidsA` a B; B entrega `iidsB` a A. Mueve el OBJETO instancia exacto
// (conserva nivel/exp/shiny/movs/mote), reasigna iid al recibir. Valida propiedad. Pura.
export function swapInstancias(
  estadoA: Estado, iidsA: string[], labelA: string,
  estadoB: Estado, iidsB: string[], labelB: string,
): { estadoA: Estado; estadoB: Estado } {
  const pcA = leerPC(estadoA); const pcB = leerPC(estadoB);
  const tomar = (pc: Instancia[], iids: string[], label: string): Instancia[] => {
    const out: Instancia[] = [];
    for (const iid of iids) {
      const i = pc.findIndex((m) => String(m.iid) === String(iid));
      if (i < 0) throw new Error(`${label} ya no tiene esa instancia (${iid})`);
      out.push(pc.splice(i, 1)[0]);
    }
    return out;
  };
  const daA = tomar(pcA, iidsA, labelA);   // lo que A entrega
  const daB = tomar(pcB, iidsB, labelB);   // lo que B entrega
  const recibir = (m: Instancia): Instancia => ({ ...m, iid: nuevoIid(), creado: Date.now() });
  for (const m of daA) pcB.push(recibir(m));
  for (const m of daB) pcA.push(recibir(m));
  return { estadoA: escribirPC(estadoA, pcA), estadoB: escribirPC(estadoB, pcB) };
}
