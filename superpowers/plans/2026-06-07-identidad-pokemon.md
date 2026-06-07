# Identidad por Pokémon — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Cada instancia capturada se vuelve única — IVs, naturaleza, género, habilidad (set curado con efecto en combate) y EVs entrenables.

**Architecture:** Toda la lógica pura vive en `web/src/lib/combate-core.ts` (fuente única; `api/scripts/sync-batalla-data.mjs` copia el core + los JSON a `api/src/batalla/`). Identidad fija = derivada del hash del `iid` (cero migración); EVs mutables viven en la instancia de `col:pc` (sync nube existente). Habilidades "core-contained" (modificadores de daño/inmunidad/estado/precisión) van dentro de las funciones puras; las de orquestación (Intimidación al entrar, Estática/Cuerpo Llama al contacto) se exponen como helpers puros que llaman los dos orquestadores (`batalla.astro` práctica, `motor.ts` PvP).

**Tech Stack:** TypeScript (combate-core), JS módulos (coleccion/batalla/items), Astro (pokedex/safari/tienda/ayuda), Jest (tests en `api/`), Node scripts (gen-data desde PokeAPI), Pyodide no se toca.

**Convención del repo:** specs/plans en `superpowers/` (raíz, NO `docs/` — el build limpia `docs/`). Sin atribución Claude en commits. UI/diseño visual → skill `/frontend-design`.

**Flujo de tests del core:** el spec vive en `api/src/batalla/combate-core.spec.ts` y corre contra la **copia sincronizada**. Por eso cada tarea que toca el core hace: editar `web/src/lib/combate-core.ts` → `cd api && node scripts/sync-batalla-data.mjs` → editar/correr el spec en `api/`.

---

### Task 1: Data — habilidades.json + yields.json (gen scripts + sync + inyección)

**Files:**
- Create: `web/scripts/gen-habilidades.mjs`
- Create: `web/scripts/gen-yields.mjs`
- Create: `web/src/data/habilidades.json` (salida del script)
- Create: `web/src/data/yields.json` (salida del script)
- Modify: `api/scripts/sync-batalla-data.mjs` (agregar los 2 JSON a `FILES`)
- Modify: `web/src/lib/batalla.js` (importar + inyectar `habilidades` en `DATOS`)
- Modify: `api/src/batalla/motor.ts` (importar + inyectar `habilidades` en `DATOS`)

**Shapes:**
- `habilidades.json`: `{ especies: { "<id>": [{ "key": "espesura", "hidden": false }, ...] }, genero: { "<id>": <gender_rate -1..8> }, meta: { "<key>": { "nombre": "Espesura", "desc": "...", "efecto": true|false } } }`
- `yields.json`: `{ "<id>": [h,a,d,sa,sd,sp] }` (effort yield, enteros 0..3).

- [ ] **Step 1: Escribir `web/scripts/gen-habilidades.mjs`**

```js
// gen-habilidades.mjs — baja habilidades (slots por especie + meta ES) y gender_rate de PokeAPI.
// Salida: web/src/data/habilidades.json. Correr: node scripts/gen-habilidades.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'habilidades.json');
const MAX = 721;                          // dex actual (gen 1-6), igual que pokemon.json
const API = 'https://pokeapi.co/api/v2';

// set CURADO: key interno → {nombre, desc, efecto:true}. El resto se marca efecto:false.
const CURADAS = {
  intimidate:      { nombre: 'Intimidación', desc: 'Al entrar en combate baja el Ataque del rival.' },
  levitate:        { nombre: 'Levitación',   desc: 'Inmune a los movimientos de tipo Tierra.' },
  sturdy:          { nombre: 'Robustez',     desc: 'Soporta con 1 PS un golpe letal si tenía los PS al máximo.' },
  static:          { nombre: 'Estática',     desc: 'Puede paralizar al atacante al recibir un golpe de contacto.' },
  'flame-body':    { nombre: 'Cuerpo Llama', desc: 'Puede quemar al atacante al recibir un golpe de contacto.' },
  overgrow:        { nombre: 'Espesura',     desc: 'Potencia los movimientos de tipo Planta con pocos PS.' },
  blaze:           { nombre: 'Mar Llamas',   desc: 'Potencia los movimientos de tipo Fuego con pocos PS.' },
  torrent:         { nombre: 'Torrente',     desc: 'Potencia los movimientos de tipo Agua con pocos PS.' },
  guts:            { nombre: 'Agallas',      desc: 'Sube el Ataque si sufre un estado alterado.' },
  'water-absorb':  { nombre: 'Absorbe Agua', desc: 'Inmune a los movimientos de tipo Agua.' },
  'flash-fire':    { nombre: 'Absorbe Fuego', desc: 'Inmune a los movimientos de tipo Fuego.' },
  immunity:        { nombre: 'Inmunidad',    desc: 'No puede ser envenenado.' },
  insomnia:        { nombre: 'Insomnio',     desc: 'No puede quedarse dormido.' },
  'magma-armor':   { nombre: 'Armadura Magma', desc: 'No puede ser congelado.' },
  'compound-eyes': { nombre: 'Ojo Compuesto', desc: 'Aumenta la precisión de sus movimientos.' },
};

const get = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); };
const esES = (arr, key) => (arr.find((x) => x.language.name === 'es') || {})[key] || '';

const especies = {}, genero = {}, meta = {};
const abilityKeys = new Set();
for (let id = 1; id <= MAX; id++) {
  const p = await get(`${API}/pokemon/${id}`);
  especies[id] = p.abilities.map((a) => ({ key: a.ability.name, hidden: a.is_hidden }));
  p.abilities.forEach((a) => abilityKeys.add(a.ability.name));
  const sp = await get(`${API}/pokemon-species/${id}`);
  genero[id] = sp.gender_rate;            // -1 sin género, 0 siempre ♂, 8 siempre ♀, n = n/8 ♀
  if (id % 50 === 0) console.log('…', id);
}
for (const key of abilityKeys) {
  if (CURADAS[key]) { meta[key] = { ...CURADAS[key], efecto: true }; continue; }
  const a = await get(`${API}/ability/${key}`);
  meta[key] = {
    nombre: esES(a.names, 'name') || key,
    desc: (esES(a.flavor_text_entries, 'flavor_text') || '').replace(/\s+/g, ' ').trim(),
    efecto: false,
  };
}
fs.writeFileSync(OUT, JSON.stringify({ especies, genero, meta }));
console.log('✓ habilidades.json', Object.keys(especies).length, 'especies,', Object.keys(meta).length, 'habilidades');
```

- [ ] **Step 2: Escribir `web/scripts/gen-yields.mjs`**

```js
// gen-yields.mjs — baja el effort yield (EVs que da derrotar la especie) de PokeAPI.
// Salida: web/src/data/yields.json {id:[h,a,d,sa,sd,sp]}. Correr: node scripts/gen-yields.mjs
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const OUT = path.resolve(HERE, '..', 'src', 'data', 'yields.json');
const MAX = 721;
const ORD = ['hp', 'attack', 'defense', 'special-attack', 'special-defense', 'speed'];
const get = async (u) => { const r = await fetch(u); if (!r.ok) throw new Error(u + ' ' + r.status); return r.json(); };

const out = {};
for (let id = 1; id <= MAX; id++) {
  const p = await get(`https://pokeapi.co/api/v2/pokemon/${id}`);
  const m = {}; p.stats.forEach((s) => { m[s.stat.name] = s.effort; });
  out[id] = ORD.map((k) => m[k] || 0);
  if (id % 50 === 0) console.log('…', id);
}
fs.writeFileSync(OUT, JSON.stringify(out));
console.log('✓ yields.json', Object.keys(out).length, 'especies');
```

- [ ] **Step 3: Correr los gen scripts**

Run (desde `web/`): `node scripts/gen-habilidades.mjs && node scripts/gen-yields.mjs`
Expected: crea `web/src/data/habilidades.json` y `web/src/data/yields.json`. (Tardan: ~721×2 fetches. Si PokeAPI falla por rate-limit, reintentar.)

- [ ] **Step 4: Agregar los JSON al sync**

En `api/scripts/sync-batalla-data.mjs`, cambiar la línea de `FILES`:
```js
const FILES = ['tipos.json', 'movimientos.json', 'learnsets.json', 'pokemon.json', 'evoluciones.json', 'estadisticas.json', 'habilidades.json', 'yields.json'];
```

- [ ] **Step 5: Inyectar `habilidades` en el DATOS del front (`web/src/lib/batalla.js`)**

Agregar import (junto a los otros, ~línea 7):
```js
import habilidades from '../data/habilidades.json' with { type: 'json' };
```
Y dentro del objeto `DATOS` (~línea 18-20) agregar la propiedad `habilidades`:
```js
const DATOS = {
  nombres: Object.fromEntries(pokemon.map((p) => [p.id, p.nombre])),
  tipos, learnsets, movimientos, estadisticas, habilidades,
};
```
(Mantener las claves existentes; solo sumar `habilidades`.)

- [ ] **Step 6: Inyectar `habilidades` en el DATOS del server (`api/src/batalla/motor.ts`)**

Agregar import (junto a `import estadisticas from './data/estadisticas.json';`, ~línea 10):
```ts
import habilidades from './data/habilidades.json';
```
Y en el objeto `DATOS` (~línea 28-30) agregar:
```ts
  estadisticas: estadisticas as any,
  habilidades: habilidades as any,
```

- [ ] **Step 7: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/scripts/gen-habilidades.mjs web/scripts/gen-yields.mjs web/src/data/habilidades.json web/src/data/yields.json api/scripts/sync-batalla-data.mjs web/src/lib/batalla.js api/src/batalla/motor.ts
git commit -m "data: habilidades + yields (PokeAPI) e inyección en ambos motores"
```

---

### Task 2: combate-core — naturalezas + derivación de identidad

**Files:**
- Modify: `web/src/lib/combate-core.ts` (interfaces + NATURALEZAS + semilla/prng + identidad + rolarIdentidad)
- Test: `api/src/batalla/combate-core.spec.ts`

- [ ] **Step 1: Extender interfaces en `combate-core.ts`**

Reemplazar la interfaz `Inst` (línea 10) por:
```ts
export interface Inst { iid: string; id: number; nivel: number; shiny?: boolean; mote?: string; movs?: number[];
  ivs?: number[]; nat?: number; hab?: string; gen?: 'm' | 'f' | null; evs?: number[]; }
```
En `Combatiente` (líneas 11-15) agregar al final del objeto, antes del cierre `}` (OPCIONALES — así `combatiente()` sigue compilando hasta que Task 3 los setea):
```ts
  hab?: string | null; gen?: 'm' | 'f' | null;
```
En `DatosCombate` (líneas 17-23) agregar:
```ts
  habilidades?: { especies: Record<string, { key: string; hidden: boolean }[]>; genero: Record<string, number>; meta: Record<string, { nombre: string; desc: string; efecto: boolean }> };
```

- [ ] **Step 2: Escribir el test de naturalezas + derivación (FALLA primero)**

En `api/src/batalla/combate-core.spec.ts`, agregar (importar lo nuevo arriba):
```ts
import { NATURALEZAS, semilla, identidad, rolarIdentidad } from './combate-core';

describe('identidad', () => {
  const HAB = { especies: { '1': [{ key: 'overgrow', hidden: false }, { key: 'chlorophyll', hidden: true }] }, genero: { '1': 1 }, meta: {} };
  const D: any = { nombres: {}, tipos: {}, learnsets: {}, movimientos: {}, estadisticas: {}, habilidades: HAB };

  test('NATURALEZAS tiene 25 entradas, 5 neutras', () => {
    expect(NATURALEZAS).toHaveLength(25);
    expect(NATURALEZAS.filter((n) => n.sube === n.baja)).toHaveLength(5);
  });

  test('semilla es estable y determinista', () => {
    expect(semilla('abc123')).toBe(semilla('abc123'));
    expect(semilla('abc123')).not.toBe(semilla('abc124'));
  });

  test('identidad deriva valores estables del iid (sin campos explícitos)', () => {
    const a = identidad({ iid: 'seed0001', id: 1, nivel: 5 }, D);
    const b = identidad({ iid: 'seed0001', id: 1, nivel: 5 }, D);
    expect(a).toEqual(b);
    expect(a.ivs).toHaveLength(6);
    a.ivs.forEach((v) => { expect(v).toBeGreaterThanOrEqual(0); expect(v).toBeLessThanOrEqual(31); });
    expect(a.nat).toBeGreaterThanOrEqual(0); expect(a.nat).toBeLessThan(25);
    expect(['overgrow', 'chlorophyll']).toContain(a.hab);
    expect(['m', 'f']).toContain(a.gen);
  });

  test('identidad respeta campos explícitos', () => {
    const inst = { iid: 'x', id: 1, nivel: 5, ivs: [31, 31, 31, 31, 31, 31], nat: 3, hab: 'overgrow', gen: 'm' as const };
    expect(identidad(inst, D)).toEqual({ ivs: [31, 31, 31, 31, 31, 31], nat: 3, hab: 'overgrow', gen: 'm' });
  });

  test('rolarIdentidad produce identidad válida', () => {
    const r = rolarIdentidad(1, HAB, () => 0.99);   // rng alto → no hidden (0.99>0.05), ♂ (0.99>1/8)
    expect(r.hab).toBe('overgrow'); expect(r.gen).toBe('m'); expect(r.ivs).toHaveLength(6);
  });

  test('género genderless cuando gender_rate = -1', () => {
    const D2: any = { habilidades: { especies: { '100': [] }, genero: { '100': -1 }, meta: {} } };
    expect(identidad({ iid: 'z', id: 100, nivel: 5 }, D2).gen).toBeNull();
  });
});
```

- [ ] **Step 3: Correr el test (debe fallar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t identidad`
Expected: FAIL (`NATURALEZAS`/`semilla`/`identidad`/`rolarIdentidad` no existen).

- [ ] **Step 4: Implementar en `web/src/lib/combate-core.ts`**

Agregar después de la sección de tipos (después de la línea 61, antes de "combatientes"):
```ts
// ───────────────────────── identidad: naturalezas / IVs / género / habilidad ─────────────────────────
// stat index: 1=Atk 2=Def 3=SpA 4=SpD 5=Vel (HP=0 nunca lo afecta la naturaleza).
export interface Naturaleza { nombre: string; sube: number | null; baja: number | null; }
export const NATURALEZAS: Naturaleza[] = [
  { nombre: 'Fuerte',  sube: null, baja: null },      // 0 neutra
  { nombre: 'Huraña',  sube: 1, baja: 2 }, { nombre: 'Audaz',   sube: 1, baja: 5 },
  { nombre: 'Firme',   sube: 1, baja: 3 }, { nombre: 'Pícara',  sube: 1, baja: 4 },
  { nombre: 'Osada',   sube: 2, baja: 1 }, { nombre: 'Dócil',   sube: null, baja: null }, // 6 neutra
  { nombre: 'Plácida', sube: 2, baja: 5 }, { nombre: 'Agitada', sube: 2, baja: 3 },
  { nombre: 'Floja',   sube: 2, baja: 4 }, { nombre: 'Miedosa', sube: 5, baja: 1 },
  { nombre: 'Activa',  sube: 5, baja: 2 }, { nombre: 'Seria',   sube: null, baja: null }, // 12 neutra
  { nombre: 'Alegre',  sube: 5, baja: 3 }, { nombre: 'Ingenua', sube: 5, baja: 4 },
  { nombre: 'Modesta', sube: 3, baja: 1 }, { nombre: 'Afable',  sube: 3, baja: 2 },
  { nombre: 'Mansa',   sube: 3, baja: 5 }, { nombre: 'Cándida', sube: null, baja: null }, // 18 neutra
  { nombre: 'Alocada', sube: 3, baja: 4 }, { nombre: 'Serena',  sube: 4, baja: 1 },
  { nombre: 'Amable',  sube: 4, baja: 2 }, { nombre: 'Grosera', sube: 4, baja: 5 },
  { nombre: 'Cauta',   sube: 4, baja: 3 }, { nombre: 'Rara',    sube: null, baja: null }, // 24 neutra
];

// hash estable string→uint32 (FNV-1a)
export function semilla(iid: string): number {
  let h = 0x811c9dc5;
  for (let i = 0; i < iid.length; i++) { h ^= iid.charCodeAt(i); h = Math.imul(h, 0x01000193); }
  return h >>> 0;
}
// PRNG determinista (mulberry32)
function prng(seed: number): Rng {
  let a = seed >>> 0;
  return () => { a = (a + 0x6D2B79F5) | 0; let t = Math.imul(a ^ (a >>> 15), 1 | a); t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t; return ((t ^ (t >>> 14)) >>> 0) / 4294967296; };
}

type Ident = { ivs: number[]; nat: number; hab: string | null; gen: 'm' | 'f' | null };

// rolea una identidad nueva (captura). rng por defecto = Math.random.
export function rolarIdentidad(id: number, habData: DatosCombate['habilidades'], rng: Rng = Math.random): Ident {
  const ivs = [0, 0, 0, 0, 0, 0].map(() => Math.floor(rng() * 32));
  const nat = Math.floor(rng() * 25);
  const pool = (habData?.especies || {})[String(id)] || [];
  const normals = pool.filter((a) => !a.hidden), hiddens = pool.filter((a) => a.hidden);
  const hidR = rng();
  const hab = (hidR < 0.05 && hiddens.length) ? hiddens[0].key
    : (normals.length ? normals[Math.floor(rng() * normals.length)].key : (pool[0]?.key || null));
  const rate = (habData?.genero || {})[String(id)];
  const gen: 'm' | 'f' | null = (rate == null || rate < 0) ? null : (rng() < rate / 8 ? 'f' : 'm');
  return { ivs, nat, hab, gen };
}

// identidad de una instancia: campos explícitos si están; si no, derivada del iid (estable, sin migración).
export function identidad(inst: Inst, d: DatosCombate): Ident {
  if (inst.ivs && inst.nat != null) return { ivs: inst.ivs, nat: inst.nat, hab: inst.hab ?? null, gen: inst.gen ?? null };
  return rolarIdentidad(inst.id, d.habilidades, prng(semilla(inst.iid)));
}
```

- [ ] **Step 5: Correr el test (debe pasar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t identidad`
Expected: PASS (6/6).

- [ ] **Step 6: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: naturalezas + derivación determinista de identidad (IVs/nat/hab/género)"
```

---

### Task 3: combate-core — fórmula de stats con IV/EV/naturaleza + stats efectivas en combatiente

**Files:**
- Modify: `web/src/lib/combate-core.ts` (`statEf`, `hpEf`, `combatiente`, `calcularDano`)
- Test: `api/src/batalla/combate-core.spec.ts`

- [ ] **Step 1: Escribir el test (FALLA primero)**

Agregar a `combate-core.spec.ts`:
```ts
import { statEf as statEf3, hpEf as hpEf3 } from './combate-core';
describe('stats con IV/EV/naturaleza', () => {
  test('statEf suma IV y ⌊EV/4⌋ y aplica multiplicador de naturaleza', () => {
    // base 100, nivel 100, iv 31, ev 0, nat 1.1: floor((floor((200+31)*100/100)+5)*1.1)=floor((231+5)*1.1)=floor(259.6)=259
    expect(statEf3(100, 100, 31, 0, 1.1)).toBe(259);
    // ev 252 → floor(252/4)=63: floor((floor((200+31+63))+5)*1)=294+5=299
    expect(statEf3(100, 100, 31, 252, 1)).toBe(299);
    // compat: sin IV/EV/nat = fórmula vieja
    expect(statEf3(100, 100)).toBe(205);
  });
  test('hpEf suma IV y ⌊EV/4⌋', () => {
    // base 100, nivel 100, iv 31, ev 0: floor((200+31)*100/100)+100+10 = 231+110 = 341
    expect(hpEf3(100, 100, 31, 0)).toBe(341);
    expect(hpEf3(100, 100)).toBe(310);   // compat vieja
  });
});
```

- [ ] **Step 2: Correr el test (debe fallar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t "stats con"`
Expected: FAIL (firmas viejas ignoran iv/ev/nat → `statEf3(100,100,31,0,1.1)` da 205).

- [ ] **Step 3: Reemplazar `statEf`/`hpEf` (líneas 68-70)**

```ts
// stats efectivas estilo Gen 3 con IV (0-31), EV (0-252) y multiplicador de naturaleza (1.1/0.9/1).
export const statEf = (base: number, nivel: number, iv = 0, ev = 0, natMult = 1): number =>
  Math.floor((Math.floor((2 * (base || 60) + iv + Math.floor(ev / 4)) * nivel / 100) + 5) * natMult);
export const hpEf = (baseHp: number, nivel: number, iv = 0, ev = 0): number =>
  Math.floor((2 * (baseHp || 60) + iv + Math.floor(ev / 4)) * nivel / 100) + nivel + 10;
```

- [ ] **Step 4: Reescribir `combatiente` (líneas 99-109) para precomputar stats efectivas**

```ts
export function combatiente(inst: Inst, d: DatosCombate): Combatiente {
  const st = (d.estadisticas || {})[String(inst.id)];   // [hp, atk, def, spa, spd, spe] base
  const idn = identidad(inst, d);
  const ev = inst.evs || [0, 0, 0, 0, 0, 0];
  const nat = NATURALEZAS[idn.nat] || NATURALEZAS[0];
  const nm = (k: number) => nat.sube === k ? 1.1 : nat.baja === k ? 0.9 : 1;
  const hpM = st ? hpEf(st[0], inst.nivel, idn.ivs[0], ev[0]) : hpMax(inst.nivel);
  return {
    iid: inst.iid, id: inst.id, nombre: inst.mote || d.nombres[inst.id] || ('Nº ' + inst.id),
    nivel: inst.nivel, shiny: !!inst.shiny, tipos: tiposDe(inst.id, d.tipos),
    movs: movsDe(inst, d.learnsets, d.movimientos), hpMax: hpM, hp: hpM,
    atk: st ? statEf(st[1], inst.nivel, idn.ivs[1], ev[1], nm(1)) : 60,
    def: st ? statEf(st[2], inst.nivel, idn.ivs[2], ev[2], nm(2)) : 60,
    spa: st ? statEf(st[3], inst.nivel, idn.ivs[3], ev[3], nm(3)) : 60,
    spd: st ? statEf(st[4], inst.nivel, idn.ivs[4], ev[4], nm(4)) : 60,
    spe: st ? statEf(st[5], inst.nivel, idn.ivs[5], ev[5], nm(5)) : 60,
    atkMod: 1, defMod: 1, estado: null, estadoT: 0,
    hab: idn.hab, gen: idn.gen,
  };
}
```
(Nota: `atk/def/spa/spd/spe` ahora son **efectivas**, no base. Actualizar el comentario de la línea 14 a `// stats EFECTIVAS (con IV/EV/naturaleza)`.)

- [ ] **Step 5: Ajustar `calcularDano` (líneas 119-120) para usar stats efectivas directas**

Reemplazar:
```ts
  const A = (fisico ? atacante.atk : atacante.spa) * (atacante.atkMod || 1);   // ya efectiva
  const D = (fisico ? defensor.def : defensor.spd) * (defensor.defMod || 1);
```
(Quita las llamadas `statEf(...)` que duplicaban el escalado.)

- [ ] **Step 6: Correr tests (la suite entera del core, porque cambian números)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core`
Expected: el caso nuevo PASA. **Otros casos viejos que asumían stats base pueden fallar** (ahora hay IVs/naturaleza derivados de iids como `'cpu0'`). Para cada caso de daño que rompa, recalcular el número esperado o construir el `Inst` con `ivs:[0,0,0,0,0,0], nat:0` para neutralizar. Dejar la suite verde.

- [ ] **Step 7: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: stats efectivas con IV/EV/naturaleza (combatiente + daño)"
```

---

### Task 4: combate-core — habilidades core-contained (registro + hooks en funciones puras)

**Files:**
- Modify: `web/src/lib/combate-core.ts` (registro `HABILIDADES`, hooks en `calcularDano`, `aplicarAilment`, `acierta`)
- Test: `api/src/batalla/combate-core.spec.ts`

Habilidades de esta tarea (sin orquestación): **modDano** (Espesura/Mar Llamas/Torrente, Agallas), **inmuneTipo** (Levitación, Absorbe Agua, Absorbe Fuego), **Robustez** (Sturdy), **noEstado** (Inmunidad, Insomnio, Armadura Magma), **modPrecision** (Ojo Compuesto).

- [ ] **Step 1: Escribir tests (FALLAN primero)**

```ts
import { calcularDano as cd, aplicarAilment as aa, acierta as ac } from './combate-core';
const mkC = (over: any): any => ({ iid: 't', id: 1, nombre: 'T', nivel: 50, shiny: false, tipos: ['Normal'],
  movs: [], hpMax: 100, hp: 100, atk: 100, def: 100, spa: 100, spd: 100, spe: 100,
  atkMod: 1, defMod: 1, estado: null, estadoT: 0, hab: null, gen: null, ...over });

describe('habilidades — core', () => {
  test('Levitación anula daño Tierra', () => {
    const def = mkC({ hab: 'levitate' });
    const r = cd(mkC({ tipos: ['Tierra'] }), { id: 1, nombre: 'Terremoto', tipo: 'Tierra', poder: 100 } as any, def);
    expect(r.dmg).toBe(0); expect(r.inmuneHab).toBe('levitate');
  });
  test('Absorbe Fuego anula daño Fuego', () => {
    const r = cd(mkC({ tipos: ['Fuego'] }), { id: 1, nombre: 'Lanzallamas', tipo: 'Fuego', poder: 90 } as any, mkC({ hab: 'flash-fire' }));
    expect(r.dmg).toBe(0);
  });
  test('Espesura potencia Planta con <1/3 HP', () => {
    const atkBajo = mkC({ tipos: ['Planta'], hab: 'overgrow', hp: 20, hpMax: 100 });
    const atkFull = mkC({ tipos: ['Planta'], hab: 'overgrow', hp: 100, hpMax: 100 });
    const mov: any = { id: 1, nombre: 'Latigazo', tipo: 'Planta', poder: 60, categoria: 'Físico' };
    const rng = () => 0.5;
    expect(cd(atkBajo, mov, mkC({}), rng).dmg).toBeGreaterThan(cd(atkFull, mov, mkC({}), rng).dmg);
  });
  test('Agallas potencia físico con estado', () => {
    const mov: any = { id: 1, nombre: 'Golpe', tipo: 'Normal', poder: 60, categoria: 'Físico' };
    const conEstado = mkC({ hab: 'guts', estado: 'paralisis' });   // parálisis no penaliza daño (a diferencia de quemadura)
    const sano = mkC({ hab: 'guts', estado: null });
    const rng = () => 0.5;
    expect(cd(conEstado, mov, mkC({}), rng).dmg).toBeGreaterThan(cd(sano, mov, mkC({}), rng).dmg);
  });
  test('Robustez sobrevive a 1 HP desde full', () => {
    const def = mkC({ hab: 'sturdy', hp: 100, hpMax: 100 });
    const r = cd(mkC({ tipos: ['Lucha'] }), { id: 1, nombre: 'A Bocajarro', tipo: 'Lucha', poder: 250, categoria: 'Físico' } as any, def, () => 0.99);
    expect(r.dmg).toBe(99); expect(r.sturdy).toBe(true);
  });
  test('Inmunidad bloquea veneno', () => {
    const def = mkC({ hab: 'immunity' });
    expect(aa({ id: 1, nombre: 'Tóxico', tipo: 'Veneno', ailment: 'veneno', ailmentChance: 100 } as any, mkC({}), def, () => 0)).toBe('');
    expect(def.estado).toBeNull();
  });
  test('Ojo Compuesto sube precisión', () => {
    const atk = mkC({ hab: 'compound-eyes' });
    // precisión 70 → ×1.3 = 91; rng 0.8 (=80%) ahora acierta
    expect(ac({ id: 1, nombre: 'X', tipo: 'Normal', precision: 70 } as any, () => 0.8, atk)).toBe(true);
  });
});
```

- [ ] **Step 2: Correr (debe fallar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t "habilidades — core"`
Expected: FAIL (hooks no existen; `inmuneHab`/`sturdy` no se devuelven; `acierta` ignora 3er arg).

- [ ] **Step 3: Agregar el registro + helpers en `combate-core.ts`**

Agregar antes de la sección "daño" (antes de la línea 111):
```ts
// ───────────────────────── habilidades (core-contained) ─────────────────────────
const BOOST_TIPO: Record<string, string> = { overgrow: 'Planta', blaze: 'Fuego', torrent: 'Agua' };
const ABSORBE_TIPO: Record<string, string> = { levitate: 'Tierra', 'water-absorb': 'Agua', 'flash-fire': 'Fuego' };
const NO_ESTADO: Record<string, EstadoAlt> = { immunity: 'veneno', insomnia: 'sueno', 'magma-armor': 'congelado' };

// ¿la habilidad del defensor lo hace inmune a este tipo de movimiento?
export const habInmuneTipo = (c: Combatiente, tipoMov: string): boolean => !!c.hab && ABSORBE_TIPO[c.hab] === tipoMov;
// multiplicador de daño por habilidad del ATACANTE (Espesura/Mar Llamas/Torrente, Agallas).
export function habModDano(atacante: Combatiente, mov: Mov): number {
  let m = 1;
  if (atacante.hab && BOOST_TIPO[atacante.hab] === mov.tipo && atacante.hp / atacante.hpMax < 1 / 3) m *= 1.5;
  if (atacante.hab === 'guts' && atacante.estado && esFisico(mov)) m *= 1.5;
  return m;
}
// ¿la habilidad del defensor bloquea este estado?
export const habNoEstado = (c: Combatiente, estado: EstadoAlt): boolean => !!c.hab && NO_ESTADO[c.hab] === estado;
// multiplicador de precisión por habilidad del atacante (Ojo Compuesto).
export const habModPrecision = (c: Combatiente | undefined): number => (c && c.hab === 'compound-eyes') ? 1.3 : 1;
```

- [ ] **Step 4: Aplicar hooks en `calcularDano`**

Al inicio de `calcularDano`, después de `const efec = efectividad(...)` (línea 115), antes del `if (efec === 0)`:
```ts
  if (habInmuneTipo(defensor, mov.tipo)) return { dmg: 0, efec: 0, stab: 1, crit: false, inmuneHab: defensor.hab };
```
Reemplazar la línea del `dmg` final (línea 124) y el return por:
```ts
  let dmg = Math.max(1, Math.round(baseDmg * stab * efec * quema * (crit ? 2 : 1) * rand * habModDano(atacante, mov)));
  let sturdy = false;
  if (defensor.hab === 'sturdy' && defensor.hp === defensor.hpMax && dmg >= defensor.hp) { dmg = defensor.hp - 1; sturdy = true; }
  return { dmg, efec, stab, crit, sturdy };
```
(El tipo de retorno de `calcularDano` gana campos opcionales `inmuneHab?: string|null; sturdy?: boolean`. Si hay anotación de tipo explícita, ampliarla; si es inferida, no hace falta.)

- [ ] **Step 5: Aplicar hook en `aplicarAilment`**

En `aplicarAilment`, después de la línea de inmunidad por tipo (línea 202), agregar:
```ts
  if (habNoEstado(defensor, mov.ailment)) return '';   // habilidad bloquea el estado
```

- [ ] **Step 6: Aplicar hook en `acierta`**

Reemplazar la firma + cuerpo de `acierta` (línea 170):
```ts
export const acierta = (mov: Mov, rng: Rng = Math.random, atacante?: Combatiente): boolean =>
  (rng() * 100) < (mov.precision == null ? 100 : mov.precision * habModPrecision(atacante));
```

- [ ] **Step 7: Correr (debe pasar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core`
Expected: PASS (incluye la suite nueva + las viejas siguen verdes).

- [ ] **Step 8: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: habilidades core-contained (inmunidad de tipo, boost de daño, sturdy, no-estado, precisión)"
```

---

### Task 5: combate-core — helpers de orquestación (Intimidación al entrar, Estática/Cuerpo Llama al contacto)

**Files:**
- Modify: `web/src/lib/combate-core.ts` (exportar `habAlEntrar`, `habAlContacto`)
- Test: `api/src/batalla/combate-core.spec.ts`

- [ ] **Step 1: Escribir tests (FALLAN primero)**

```ts
import { habAlEntrar, habAlContacto } from './combate-core';
describe('habilidades — orquestación', () => {
  test('Intimidación baja el Ataque del rival al entrar', () => {
    const self = mkC({ hab: 'intimidate', nombre: 'Gyarados' });
    const rival = mkC({ atkMod: 1 });
    const txt = habAlEntrar(self, rival);
    expect(rival.atkMod).toBeLessThan(1);
    expect(txt).toMatch(/Intimidaci/);
  });
  test('Intimidación no hace nada sin la habilidad', () => {
    const rival = mkC({ atkMod: 1 });
    expect(habAlEntrar(mkC({ hab: null }), rival)).toBe('');
    expect(rival.atkMod).toBe(1);
  });
  test('Estática paraliza al atacante de contacto (rng bajo)', () => {
    const def = mkC({ hab: 'static' });
    const atk = mkC({ estado: null });
    const txt = habAlContacto(def, atk, { id: 1, nombre: 'Placaje', tipo: 'Normal', poder: 40, categoria: 'Físico' } as any, () => 0.01);
    expect(atk.estado).toBe('paralisis'); expect(txt).toMatch(/paraliz/i);
  });
  test('Cuerpo Llama no actúa con movimiento especial (sin contacto)', () => {
    const def = mkC({ hab: 'flame-body' });
    const atk = mkC({ estado: null });
    expect(habAlContacto(def, atk, { id: 1, nombre: 'Rayo', tipo: 'Eléctrico', poder: 90, categoria: 'Especial' } as any, () => 0.01)).toBe('');
    expect(atk.estado).toBeNull();
  });
});
```

- [ ] **Step 2: Correr (debe fallar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t "orquestación"`
Expected: FAIL (helpers no existen).

- [ ] **Step 3: Implementar en `combate-core.ts`** (junto a los otros helpers de habilidad)

```ts
// AL ENTRAR a pista (Intimidación). Muta al rival. Devuelve texto|''.
export function habAlEntrar(self: Combatiente, rival: Combatiente): string {
  if (self.hab !== 'intimidate' || !rival || rival.hp <= 0) return '';
  rival.atkMod = Math.max(0.4, (rival.atkMod || 1) * 0.7);
  return '¡Intimidación de ' + self.nombre + '! El Ataque de ' + rival.nombre + ' bajó ↓';
}
// AL RECIBIR un golpe de CONTACTO (físico) — Estática/Cuerpo Llama. Muta al atacante. Devuelve texto|''.
export function habAlContacto(self: Combatiente, atacante: Combatiente, mov: Mov, rng: Rng = Math.random): string {
  if (!esFisico(mov) || atacante.hp <= 0 || atacante.estado) return '';
  if (self.hab === 'static' && rng() < 0.3) { atacante.estado = 'paralisis'; return '¡Estática de ' + self.nombre + ' paralizó a ' + atacante.nombre + '!'; }
  if (self.hab === 'flame-body' && rng() < 0.3 && !atacante.tipos.includes('Fuego')) { atacante.estado = 'quemadura'; return '¡Cuerpo Llama de ' + self.nombre + ' quemó a ' + atacante.nombre + '!'; }
  return '';
}
```

- [ ] **Step 4: Correr (debe pasar)**

Run: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core`
Expected: PASS (toda la suite).

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: helpers de orquestación de habilidades (Intimidación al entrar, Estática/Cuerpo Llama al contacto)"
```

---

### Task 6: Orquestadores — disparar alEntrar/alContacto en práctica (batalla.astro) y PvP (motor.ts)

**Files:**
- Modify: `web/src/pages/batalla.astro` (import + llamadas en inicio/cambio/auto-switch + post-golpe)
- Modify: `web/src/lib/batalla.js` (re-exportar `habAlEntrar`, `habAlContacto`)
- Modify: `api/src/batalla/motor.ts` (llamadas en iniciar/cambiar/postGolpe)

- [ ] **Step 1: Re-exportar los helpers en `web/src/lib/batalla.js`**

Agregar `habAlEntrar, habAlContacto` a la lista de re-exports del core (líneas 11-14):
```js
  ESTADOS, acierta, puedeActuar, aplicarAilment, tickEstado, efectividad, etiquetaEfec,
  habAlEntrar, habAlContacto,
```

- [ ] **Step 2: Importar en `batalla.astro`** (línea 82, agregar a la lista de imports)

Agregar `habAlEntrar, habAlContacto` al `import { ... } from '../lib/batalla.js';`.

- [ ] **Step 3: Disparar `habAlContacto` post-golpe en `batalla.astro`**

En la función que aplica un golpe (`aplicarGolpe`, alrededor de la línea 256 / 312, donde tras el daño el defensor sigue vivo y se aplica `aplicarAilment`), agregar después del bloque de `aplicarAilment`:
```js
      if (def.hp > 0) { const tc = habAlContacto(def, at, mov, Math.random); if (tc) { msg(tc); render(); await esperar(1000); } }
```
(`at` = atacante, `def` = defensor, `mov` = movimiento usado — usar los nombres reales de las variables locales de esa función.)

- [ ] **Step 4: Disparar `habAlEntrar` al entrar un Pokémon en `batalla.astro`**

Identificar los puntos donde un Pokémon entra a pista: (a) inicio del combate (ambos activos), (b) `cambiar(i)` (~228), (c) auto-switch tras debilitarse (~332). En cada uno, después de fijar el nuevo activo y renderizar, agregar (con el rival correspondiente):
```js
      { const te = habAlEntrar(NUEVO_ACTIVO, RIVAL_ACTIVO); if (te) { msg(te); render(); await esperar(1000); } }
```
Reemplazar `NUEVO_ACTIVO`/`RIVAL_ACTIVO` por las variables locales (ej. en `cambiar`: el aliado nuevo y el rival activo; al inicio: cada lado contra el otro).

- [ ] **Step 5: Disparar en el server `api/src/batalla/motor.ts`**

Importar del core (junto a los otros, ~línea 20):
```ts
  habAlEntrar, habAlContacto,
```
- En `postGolpe`/aplicación de golpe (donde el defensor sobrevive y se calcula el daño), tras aplicar el ailment, agregar el contacto:
```ts
  const tc = habAlContacto(def, atk, mov, Math.random); if (tc) push('habilidad', tc);
```
- En `iniciar` (al armar `equipo`, ~línea 59), y en el handler de `cambiar` (~línea 166-169) y en `autoSwitch`/`postGolpe` cuando entra el reemplazante (`push('entra', ...)`), agregar:
```ts
  const te = habAlEntrar(activoDe(yo), activoDe(rival)); if (te) push('habilidad', te);
```
(Usar las variables de cada contexto; para el inicio, disparar por ambos lados.)

- [ ] **Step 5b: Cablear `acierta` con el atacante (Ojo Compuesto) en ambos orquestadores**

Buscar las llamadas a `acierta(mov, ...)` en `web/src/pages/batalla.astro` y en `api/src/batalla/motor.ts` y pasarles el combatiente atacante como 3er argumento, para que `habModPrecision` aplique:
```js
// antes: acierta(mov)   → después: acierta(mov, Math.random, atacante)
```
(Usar la variable real del atacante en cada contexto. Si `acierta` no se llama en alguno, omitir ahí.)

- [ ] **Step 6: Verificar que compila y los tests del motor siguen verdes**

Run: `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest`
Expected: build OK, jest verde (motor.spec + combate-core.spec).

- [ ] **Step 7: Verificar el build del front**

Run (desde `web/`): `npm run build`
Expected: build OK (genera `../docs`).

- [ ] **Step 8: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/pages/batalla.astro web/src/lib/batalla.js api/src/batalla/motor.ts api/src/batalla/combate-core.ts
git commit -m "batalla: disparar habilidades al entrar (Intimidación) y al contacto (Estática/Cuerpo Llama) en práctica y PvP"
```

---

### Task 7: coleccion.js — escribir identidad al capturar + EVs (darEV) + ganarlos en práctica

**Files:**
- Modify: `web/src/lib/coleccion.js` (`atrapar`, `darEV`, `identidadDe`, `evsDe`, helpers de display)
- Modify: `web/src/pages/batalla.astro` (otorgar EVs al ganar en práctica)
- Test: `api/src/batalla/combate-core.spec.ts` (cap de darEV via función pura) — ver nota

**Nota de test:** la lógica de cap de EVs se prueba como función pura. Para no acoplar a localStorage, implementar el cálculo de cap en `combate-core.ts` como `sumarEV(evs, yields)` (pura, testeable) y que `darEV` en `coleccion.js` la use.

- [ ] **Step 1: Test de `sumarEV` (FALLA primero)** — en `combate-core.spec.ts`

```ts
import { sumarEV } from './combate-core';
describe('EVs', () => {
  test('sumarEV respeta cap 252 por stat', () => {
    expect(sumarEV([250, 0, 0, 0, 0, 0], [3, 0, 0, 0, 0, 0])).toEqual([252, 0, 0, 0, 0, 0]);
  });
  test('sumarEV respeta cap total 510', () => {
    const r = sumarEV([252, 252, 0, 0, 0, 0], [0, 0, 10, 0, 0, 0]);
    expect(r[2]).toBe(6);   // solo entran 6 hasta 510
    expect(r.reduce((a, b) => a + b, 0)).toBe(510);
  });
});
```

- [ ] **Step 2: Correr (debe fallar)** — `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t EVs` → FAIL.

- [ ] **Step 3: Implementar `sumarEV` en `combate-core.ts`**

```ts
// suma EVs respetando cap 252 por stat y 510 total. Pura.
export function sumarEV(evs: number[], yields: number[]): number[] {
  const out = (evs && evs.length === 6) ? [...evs] : [0, 0, 0, 0, 0, 0];
  let total = out.reduce((a, b) => a + b, 0);
  for (let i = 0; i < 6; i++) {
    const espacioStat = Math.min(252 - out[i], (yields[i] || 0));
    const inc = Math.max(0, Math.min(espacioStat, 510 - total));
    out[i] += inc; total += inc;
  }
  return out;
}
```

- [ ] **Step 4: Correr (debe pasar)** — `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t EVs` → PASS.

- [ ] **Step 5: Escribir identidad al capturar (`coleccion.js`)**

Agregar imports arriba del archivo:
```js
import habilidades from '../data/habilidades.json';
import yields from '../data/yields.json';
import { rolarIdentidad, identidad as identidadCore, NATURALEZAS, sumarEV } from './combate-core.ts';
```
Reemplazar el cuerpo de `atrapar` (líneas 71-76) para que escriba identidad + EVs en cero:
```js
export function atrapar(id, { shiny = false, nivel = 1 } = {}) {
  asegurarMigrado();
  const idn = rolarIdentidad(id, habilidades);
  const inst = { iid: _uid(), id, nivel, exp: 0, shiny, movs: [], creado: Date.now(),
    ivs: idn.ivs, nat: idn.nat, hab: idn.hab, gen: idn.gen, evs: [0, 0, 0, 0, 0, 0] };
  const arr = pc(); arr.push(inst); setPC(arr);
  marcarVisto(id);
  return inst;
}
```
(Si el cuerpo real difiere — p.ej. `marcarVisto` se llama distinto — conservar esas llamadas; solo sumar los campos de identidad.)

- [ ] **Step 6: Agregar helpers de identidad/EV + `darEV` en `coleccion.js`**

```js
// data de combate para derivar identidad de una instancia (para UI)
const _DATOS_ID = { habilidades };
export const identidadDe = (inst) => identidadCore(inst, _DATOS_ID);
export const evsDe = (inst) => (inst.evs && inst.evs.length === 6) ? inst.evs : [0, 0, 0, 0, 0, 0];
export const naturalezaDe = (inst) => NATURALEZAS[identidadDe(inst).nat] || NATURALEZAS[0];
export const habMeta = (key) => (habilidades.meta || {})[key] || null;
export const yieldDe = (id) => yields[String(id)] || [0, 0, 0, 0, 0, 0];

// otorga EVs a una instancia (por iid) según un vector yield. Persiste. Respeta caps.
export function darEV(iid, yieldVec) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return;
  m.evs = sumarEV(evsDe(m), yieldVec); setPC(arr);
}
```

- [ ] **Step 7: Otorgar EVs al ganar en práctica (`batalla.astro`)**

En el flujo de práctica (NO online), cuando un rival se debilita, otorgar a los Pokémon participantes del jugador el yield del rival. Importar arriba (línea 82 zona imports de coleccion en batalla.astro — verificar de qué módulo): `import { darEV, yieldDe } from '../lib/coleccion.js';`. En el punto donde el rival CPU cae (post-golpe, rama práctica), agregar:
```js
      if (!ESONLINE) { const yv = yieldDe(rivalCaido.id); equipoJugadorParticipante.forEach((c) => darEV(c.iid, yv)); }
```
Donde `rivalCaido` = el combatiente CPU debilitado y `equipoJugadorParticipante` = los combatientes del jugador que entraron en combate (mínimo el activo; si no se trackea participación, usar `[tuActivo]`). `ESONLINE` = el flag que distingue práctica de PvP en esa página.

- [ ] **Step 8: Build del front**

Run (desde `web/`): `npm run build`
Expected: OK.

- [ ] **Step 9: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/coleccion.js web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts web/src/pages/batalla.astro
git commit -m "coleccion: identidad al capturar + EVs (sumarEV con caps) + ganarlos en práctica"
```

---

### Task 8: Vitaminas (tienda) — ruta de EV pagada en Pokébolas

**Files:**
- Modify: `web/src/lib/items.js` (6 vitaminas, cat `'ev'`)
- Modify: `web/src/lib/coleccion.js` (`usarVitamina`)
- Modify: `web/src/pages/tienda.astro` (categoría `'ev'` + flujo de uso: elegir Pokémon)

- [ ] **Step 1: Agregar vitaminas en `items.js`** (después de la cat `'estado'`)

```js
  proteina: { nombre: 'Proteína', sprite: 'vitamina', precio: 30, cat: 'ev', ev: 1, evMax: 100, desc: '+10 EV de Ataque (hasta 100 por esta vía).' },
  hierro:   { nombre: 'Hierro',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 2, evMax: 100, desc: '+10 EV de Defensa (hasta 100).' },
  calcio:   { nombre: 'Calcio',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 3, evMax: 100, desc: '+10 EV de Ataque Especial (hasta 100).' },
  zinc:     { nombre: 'Zinc',     sprite: 'vitamina', precio: 30, cat: 'ev', ev: 4, evMax: 100, desc: '+10 EV de Defensa Especial (hasta 100).' },
  carburo:  { nombre: 'Carburo',  sprite: 'vitamina', precio: 30, cat: 'ev', ev: 5, evMax: 100, desc: '+10 EV de Velocidad (hasta 100).' },
  masps:    { nombre: 'Más PS',   sprite: 'vitamina', precio: 30, cat: 'ev', ev: 0, evMax: 100, desc: '+10 EV de PS (hasta 100).' },
```
(El sprite `'vitamina'` se agrega en `sprites.js` como una píldora/frasco SVG genérico color-coded por stat — ver Task 9, regla CLAUDE.md: items Pokémon = SVG, no emoji.)

- [ ] **Step 2: `usarVitamina` en `coleccion.js`**

```js
// usa una vitamina sobre una instancia: +10 EV al stat, tope 100 por vía vitamina y caps globales (252/510).
export function usarVitamina(iid, statIdx) {
  const arr = pc(); const m = arr.find((x) => x.iid === iid); if (!m) return false;
  const ev = evsDe(m);
  if (ev[statIdx] >= 100) return false;        // tope vitamina
  const yieldVec = [0, 0, 0, 0, 0, 0]; yieldVec[statIdx] = Math.min(10, 100 - ev[statIdx]);
  m.evs = sumarEV(ev, yieldVec); setPC(arr);
  return true;
}
```

- [ ] **Step 3: Tienda — categoría `'ev'` + uso**

En `tienda.astro`: agregar la categoría `'ev'` al render de la tienda (mismo patrón que `'cura'`/`'estado'`). Al "usar" una vitamina (fuera de batalla), abrir un mini-selector del PC (reusar el patrón de elegir Pokémon ya existente para items) y llamar `usarVitamina(iid, ITEMS[key].ev)`. Si no hay flujo de "usar fuera de batalla", el consumo de vitamina puede hacerse desde el modal del Pokédex (Task 9) — en ese caso, en esta tarea solo se agregan a la venta y el consumo va en Task 9. **Decisión:** venta acá; consumo desde el modal Pokédex (Task 9) para reusar el selector de instancia.

- [ ] **Step 4: Build**

Run (desde `web/`): `npm run build` → OK.

- [ ] **Step 5: Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/items.js web/src/lib/coleccion.js web/src/pages/tienda.astro
git commit -m "tienda: vitaminas (EV) en venta + usarVitamina con topes"
```

---

### Task 9: UI — panel Identidad (modal Pokédex) + línea de captura (safari) + HUD batalla + sprite vitamina

**REQUIRED SUB-SKILL:** Use `/frontend-design` para todo este trabajo visual. Estética retro-Pokédex/CRT, tema-aware (oscuro y claro), cohesiva con la app.

**Files:**
- Modify: `web/src/pages/pokedex.astro` (panel "Identidad" en `poke-modal-cuerpo` + consumo de vitaminas)
- Modify: `web/src/pages/safari.astro` (línea de identidad al capturar)
- Modify: `web/src/pages/batalla.astro` (habilidad + ♂/♀ en el HUD)
- Modify: `web/src/lib/sprites.js` (sprite `vitamina` SVG, color-coded por stat)

- [ ] **Step 1: Helpers de presentación (en `pokedex.astro` o `coleccion.js`)**

```js
// % de IVs (0-100) y estrellas (0-4) para el header GO.
export const ivPct = (ivs) => Math.round((ivs.reduce((a, b) => a + b, 0) / 186) * 100);
export const ivEstrellas = (ivs) => { const p = ivPct(ivs); return p >= 90 ? 4 : p >= 75 ? 3 : p >= 50 ? 2 : p >= 25 ? 1 : 0; };
// frase del "Juez" por IV individual (0-31).
export const juezIV = (iv) => iv === 31 ? '¡Inmejorable!' : iv >= 26 ? 'Fantástico' : iv >= 16 ? 'Muy bueno' : iv >= 1 ? 'Normal' : 'Flojo';
```

- [ ] **Step 2: Panel "Identidad" en el modal del Pokédex**

En la función que arma el HTML de `poke-modal-cuerpo` (instancia seleccionada), agregar un bloque que use `identidadDe(inst)`, `evsDe(inst)`, `naturalezaDe(inst)`, `habMeta(...)`:
- **Header GO:** `ivPct` + estrellas (★) + frase resumen.
- **Por-stat:** 6 filas (PS/Atq/Def/AtEsp/DefEsp/Vel) con barra IV 0–31 + valor + `juezIV`. Mostrar también la barra EV 0–252 (color distinto) y total/510.
- **Naturaleza:** nombre + stat ↑ (clase color "sube") / ↓ ("baja"); si neutra, "neutra".
- **Habilidad:** `habMeta(idn.hab).nombre` + `.desc`. Si `efecto:false`, sin badge; si `true`, badge sutil "activa".
- **Género:** ♂ (azul) / ♀ (rosa) junto al nombre; genderless → sin símbolo.
- **Consumo de vitaminas:** botones de las vitaminas que el jugador posea (`tieneItem`), que llamen `usarVitamina(inst.iid, statIdx)` y re-rendericen (esto cierra el flujo de Task 8 Step 3).

Diseñar con `/frontend-design`. Tema-aware.

- [ ] **Step 3: Línea de identidad al capturar (`safari.astro`)**

Tras una captura exitosa (donde se muestra "¡Atrapaste a X!"), agregar una línea con la identidad del `inst` devuelto por `atrapar`: símbolo de género, `IVs NN%`, naturaleza, habilidad. Ej.: `✨ ♀ · IVs 87% · Modesta · Espesura`. Usar los helpers + `habMeta`.

- [ ] **Step 4: HUD de batalla (`batalla.astro`)**

En el cuadro del HUD de cada combatiente, mostrar el nombre de la **habilidad** (chiquito, bajo el nombre) y el símbolo **♂/♀**. Datos desde el `Combatiente` (`c.hab` → `habMeta(c.hab)?.nombre`, `c.gen`).

- [ ] **Step 5: Sprite `vitamina` en `sprites.js`**

Agregar a `itemSvg` (o el helper correspondiente) un caso `vitamina`: una píldora/frasco SVG simple, color-coded por stat (parámetro de color), congruente con el resto de items (mismo grosor de contorno/brillo). Verificar el set junto.

- [ ] **Step 6: Verificación visual (screenshot del dev server)**

Run (desde `web/`): `npm run dev` y abrir el modal del Pokédex de una instancia. Sacar **screenshot** del panel Identidad en tema oscuro y claro. Confirmar coherencia visual (barras, colores de naturaleza, género, habilidad). Repetir para la línea de safari y el HUD de batalla.

- [ ] **Step 7: Build + Commit**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/pokedex.astro web/src/pages/safari.astro web/src/pages/batalla.astro web/src/lib/sprites.js web/src/lib/coleccion.js docs
git commit -m "ui: panel Identidad (IVs/EVs/naturaleza/habilidad/género) en pokédex + safari + HUD + sprite vitamina"
```

---

### Task 10: Documentación (ayuda) + verificación final + build

**Files:**
- Modify: `web/src/pages/ayuda.astro` (sección de identidad/IVs/naturalezas/habilidades/EVs)
- Modify: `docs/` (rebuild)

- [ ] **Step 1: Documentar en `ayuda.astro`**

Agregar una sección (estilo de las existentes) que explique: cada Pokémon es único (IVs fijos, naturaleza, género, habilidad); cómo leer la tasación del modal; qué hacen las habilidades del set curado; cómo se entrenan EVs (peleando vs CPU + vitaminas) y sus topes. Sin pistas de solución (regla del proyecto aplica a consignas, no a ayuda — acá está bien explicar).

- [ ] **Step 2: Suite completa verde**

Run: `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest`
Expected: build NestJS OK, **jest 100% verde** (combate-core.spec + motor.spec).

- [ ] **Step 3: Build del front + verificación de páginas**

Run (desde `web/`): `npm run build`
Expected: OK. Abrir en dev: pokédex (modal Identidad), safari (captura), batalla (HUD + habilidades disparando), tienda (vitaminas). Sin errores JS en consola.

- [ ] **Step 4: Commit final**

```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/pages/ayuda.astro docs
git commit -m "docs: ayuda al día con identidad por Pokémon (IVs/naturalezas/habilidades/EVs)"
```

---

## Notas para el ejecutor

- **Sync obligatorio:** cualquier cambio en `web/src/lib/combate-core.ts` o en `web/src/data/*.json` requiere `cd api && node scripts/sync-batalla-data.mjs` ANTES de correr jest o el build de la API. El archivo `api/src/batalla/combate-core.ts` es GENERADO — no editarlo a mano.
- **Compat de números:** Task 3 cambia stats efectivas → algunos asserts viejos de daño en `combate-core.spec.ts` cambiarán. Recalcular o neutralizar con `ivs:[0,0,0,0,0,0], nat:0` en los `Inst` de esos tests.
- **PvP EVs / deploy Pi:** otorgar EVs en PvP y el redeploy de la imagen arm64 a la Raspberry son **owner-gated** (fuera de este plan). El motor PvP ya queda con habilidades; el deploy lo corre el dueño (ver CLAUDE.md, sección Pi).
- **Sin atribución Claude** en los commits.
```
