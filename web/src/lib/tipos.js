// tipos.js — tabla de efectividad de tipos (estándar Pokémon, en español).
// efectividad(tipoAtaque, tiposDefensor[]) = multiplicador de daño (0, 0.25, 0.5, 1, 2, 4).
import tiposData from '../data/tipos.json' with { type: 'json' };

export const tiposDe = (id) => tiposData[String(id)] || ['Normal'];

// Para cada tipo atacante: a qué se le pega x2, x0.5 y x0. (lo no listado = x1)
const TABLA = {
  Normal: { x2: [], x05: ['Roca', 'Acero'], x0: ['Fantasma'] },
  Fuego: { x2: ['Planta', 'Hielo', 'Bicho', 'Acero'], x05: ['Fuego', 'Agua', 'Roca', 'Dragón'], x0: [] },
  Agua: { x2: ['Fuego', 'Tierra', 'Roca'], x05: ['Agua', 'Planta', 'Dragón'], x0: [] },
  Planta: { x2: ['Agua', 'Tierra', 'Roca'], x05: ['Fuego', 'Planta', 'Veneno', 'Volador', 'Bicho', 'Dragón', 'Acero'], x0: [] },
  Eléctrico: { x2: ['Agua', 'Volador'], x05: ['Eléctrico', 'Planta', 'Dragón'], x0: ['Tierra'] },
  Hielo: { x2: ['Planta', 'Tierra', 'Volador', 'Dragón'], x05: ['Fuego', 'Agua', 'Hielo', 'Acero'], x0: [] },
  Lucha: { x2: ['Normal', 'Hielo', 'Roca', 'Siniestro', 'Acero'], x05: ['Veneno', 'Volador', 'Psíquico', 'Bicho', 'Hada'], x0: ['Fantasma'] },
  Veneno: { x2: ['Planta', 'Hada'], x05: ['Veneno', 'Tierra', 'Roca', 'Fantasma'], x0: ['Acero'] },
  Tierra: { x2: ['Fuego', 'Eléctrico', 'Veneno', 'Roca', 'Acero'], x05: ['Planta', 'Bicho'], x0: ['Volador'] },
  Volador: { x2: ['Planta', 'Lucha', 'Bicho'], x05: ['Eléctrico', 'Roca', 'Acero'], x0: [] },
  Psíquico: { x2: ['Lucha', 'Veneno'], x05: ['Psíquico', 'Acero'], x0: ['Siniestro'] },
  Bicho: { x2: ['Planta', 'Psíquico', 'Siniestro'], x05: ['Fuego', 'Lucha', 'Veneno', 'Volador', 'Fantasma', 'Acero', 'Hada'], x0: [] },
  Roca: { x2: ['Fuego', 'Hielo', 'Volador', 'Bicho'], x05: ['Lucha', 'Tierra', 'Acero'], x0: [] },
  Fantasma: { x2: ['Psíquico', 'Fantasma'], x05: ['Siniestro'], x0: ['Normal'] },
  Dragón: { x2: ['Dragón'], x05: ['Acero'], x0: ['Hada'] },
  Siniestro: { x2: ['Psíquico', 'Fantasma'], x05: ['Lucha', 'Siniestro', 'Hada'], x0: [] },
  Acero: { x2: ['Hielo', 'Roca', 'Hada'], x05: ['Fuego', 'Agua', 'Eléctrico', 'Acero'], x0: [] },
  Hada: { x2: ['Lucha', 'Dragón', 'Siniestro'], x05: ['Fuego', 'Veneno', 'Acero'], x0: [] },
};

function unoContra(atk, def) {
  const t = TABLA[atk]; if (!t) return 1;
  if (t.x0.includes(def)) return 0;
  if (t.x2.includes(def)) return 2;
  if (t.x05.includes(def)) return 0.5;
  return 1;
}

export function efectividad(tipoAtaque, tiposDefensor) {
  return (tiposDefensor || []).reduce((m, d) => m * unoContra(tipoAtaque, d), 1);
}

// etiqueta legible del multiplicador
export function etiquetaEfec(mult) {
  if (mult === 0) return 'No afecta…';
  if (mult >= 2) return '¡Súper eficaz!';
  if (mult <= 0.5) return 'Poco eficaz…';
  return '';
}
