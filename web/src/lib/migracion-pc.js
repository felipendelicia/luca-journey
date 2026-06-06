// migracion-pc.js — one-time: col:atrapados {id:n} + col:shiny [ids] → col:pc/vistos/caramelos.
// Idempotente (flag col:pc:migrado). Conserva todo: cada repe = una instancia nivel 1.
const get = (k, def) => { try { const v = JSON.parse(localStorage.getItem(k)); return v ?? def; } catch { return def; } };
const set = (k, v) => localStorage.setItem(k, JSON.stringify(v));
const uid = () => Math.random().toString(36).slice(2, 10);

export function migrarPC() {
  if (localStorage.getItem('col:pc:migrado') === '1') return false;
  // cuenta nueva que ya arrancó en v2 (hay PC): solo marcar migrado
  if (Array.isArray(get('col:pc', null))) { localStorage.setItem('col:pc:migrado', '1'); return false; }
  const at = get('col:atrapados', {});
  const shi = new Set((get('col:shiny', []) || []).map(Number));
  const pc = [], vistos = new Set();
  for (const [id, n] of Object.entries(at)) {
    const k = Number(id); vistos.add(k);
    for (let i = 0; i < n; i++) pc.push({ iid: uid(), id: k, nivel: 1, exp: 0, shiny: false, movs: [], creado: Date.now() });
  }
  for (const id of shi) { vistos.add(id); const inst = pc.find((m) => m.id === id && !m.shiny); if (inst) inst.shiny = true; }
  set('col:pc', pc);
  set('col:vistos', [...vistos]);
  set('col:caramelos', get('col:caramelos', {}));
  localStorage.setItem('col:pc:migrado', '1');
  return true;
}
