// rareza.js — 10 tiers de rareza. El tier de un Pokémon se asigna por su RANGO en la
// distribución global de pesos de aparición (aparicion.json), calibrado para que la TASA de
// aparición de cada tier sea la de diseño: los comunes dominan, los legendarios son rarísimos.
// Así el nombre del tier SÍ refleja qué tan seguido lo ves. El badge + la animación usan el tier.
// Puro: sin DOM, sin import.meta.
export const TIERS = [
  { nivel: 1,  nombre: 'Común',       color: '#7d8b79', ico: '',     rate: 0.28 },
  { nivel: 2,  nombre: 'Frecuente',   color: '#5fa84a', ico: '',     rate: 0.20 },
  { nivel: 3,  nombre: 'Inusual',     color: '#3fae8e', ico: '',     rate: 0.15 },
  { nivel: 4,  nombre: 'Poco común',  color: '#3aa6d8', ico: '✦',    rate: 0.11 },
  { nivel: 5,  nombre: 'Raro',        color: '#3b6fe0', ico: '✦',    rate: 0.085 },
  { nivel: 6,  nombre: 'Muy raro',    color: '#7a4fe0', ico: '✦✦',   rate: 0.065 },
  { nivel: 7,  nombre: 'Épico',       color: '#a23bd8', ico: '✦✦',   rate: 0.045 },
  { nivel: 8,  nombre: 'Excepcional', color: '#d83bb0', ico: '✦✦✦',  rate: 0.03 },
  { nivel: 9,  nombre: 'Mítico',      color: '#e07b2a', ico: '★',     rate: 0.028 },
  { nivel: 10, nombre: 'Legendario',  color: '#e8b923', ico: '★★',    rate: 0.007 },
];

// Construye el mapa id→tier recorriendo los Pokémon de MÁS a MENOS peso (común→raro) y
// acumulando su probabilidad de aparición; cuando el acumulado cruza el límite de un tier,
// pasa al siguiente. Memoizado por referencia del objeto `pesos`.
let _mapa = null, _ref = null;
function construir(pesos) {
  const ids = Object.keys(pesos).sort((a, b) => (pesos[b] || 1) - (pesos[a] || 1));
  const total = ids.reduce((s, id) => s + (pesos[id] || 1), 0) || 1;
  const mapa = {};
  let acum = 0, ti = 0, lim = TIERS[0].rate;
  for (const id of ids) {
    while (ti < TIERS.length - 1 && acum >= lim) { ti++; lim += TIERS[ti].rate; }
    mapa[id] = TIERS[ti];
    acum += (pesos[id] || 1) / total;
  }
  return mapa;
}

// tier de un Pokémon (por id) dado el mapa de pesos. Si no hay pesos, cae en Común.
export function tierDe(id, pesos) {
  if (!pesos) return TIERS[0];
  if (!_mapa || _ref !== pesos) { _ref = pesos; _mapa = construir(pesos); }
  return _mapa[String(id)] || TIERS[0];
}
