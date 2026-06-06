// tipos.js — tipos de cada especie (lee tipos.json) + re-exporta la tabla de efectividad.
// La lógica de efectividad/etiqueta vive UNA sola vez en combate-core.ts (fuente de verdad
// compartida con el motor del server). Acá queda solo `tiposDe` (que depende de la data).
import tiposData from '../data/tipos.json' with { type: 'json' };
export { efectividad, etiquetaEfec } from './combate-core.ts';

export const tiposDe = (id) => tiposData[String(id)] || ['Normal'];
