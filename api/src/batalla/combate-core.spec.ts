// Pruebas finas del NÚCLEO de combate (reglas puras, sin red ni estado de sala).
import {
  efectividad, etiquetaEfec, hpMax, hpEf, statEf, esFisico, tiraCritico, CRIT_CHANCE, FORCEJEO,
  esEstado, calcularDano, aplicarEstado, danoSuper, elegirCPU, acierta, puedeActuar,
  aplicarAilment, tickEstado, combatiente, movsDe, tiposDe, Combatiente, Mov, DatosCombate,
} from './combate-core';

// combatiente sintético (no necesita data real): se sobreescribe lo que cada test precise.
const luchador = (over: Partial<Combatiente> = {}): Combatiente => ({
  iid: 'x', id: 1, nombre: 'Test', nivel: 30, shiny: false, tipos: ['Normal'],
  movs: [], hpMax: hpEf(60, 30), hp: hpEf(60, 30), atkMod: 1, defMod: 1, estado: null, estadoT: 0,
  atk: 60, def: 60, spa: 60, spd: 60, spe: 60, ...over,
});
const mov = (o: Partial<Mov> = {}): Mov => ({ id: 1, nombre: 'M', tipo: 'Normal', poder: 50, ...o });
const rng = (v: number) => () => v;       // rng determinista
const rng0 = rng(0);                       // rand = 0.85 en calcularDano

// ───────────────────────── efectividad de tipos ─────────────────────────
describe('efectividad: tabla de tipos', () => {
  it('neutral = 1', () => expect(efectividad('Normal', ['Normal'])).toBe(1));
  it('súper eficaz simple = 2', () => expect(efectividad('Fuego', ['Planta'])).toBe(2));
  it('poco eficaz simple = 0.5', () => expect(efectividad('Fuego', ['Agua'])).toBe(0.5));
  it('inmune = 0', () => {
    expect(efectividad('Normal', ['Fantasma'])).toBe(0);
    expect(efectividad('Eléctrico', ['Tierra'])).toBe(0);
    expect(efectividad('Lucha', ['Fantasma'])).toBe(0);
    expect(efectividad('Tierra', ['Volador'])).toBe(0);
  });
  it('doble tipo apila a 4× (doble súper)', () => {
    expect(efectividad('Eléctrico', ['Agua', 'Volador'])).toBe(4);
    expect(efectividad('Planta', ['Agua', 'Tierra'])).toBe(4);
  });
  it('doble tipo apila a 0.25× (doble resistencia)', () => {
    expect(efectividad('Fuego', ['Agua', 'Roca'])).toBe(0.25);
  });
  it('una inmunidad anula todo (×0)', () => {
    expect(efectividad('Eléctrico', ['Agua', 'Tierra'])).toBe(0);   // x2 Agua × x0 Tierra
  });
  it('2× × 0.5× se cancela a 1', () => {
    expect(efectividad('Fuego', ['Planta', 'Fuego'])).toBe(1);
  });
  it('tipo atacante desconocido → 1 (no rompe)', () => {
    expect(efectividad('Luz', ['Normal'])).toBe(1);
  });
  it('sin tipos defensor → 1', () => {
    expect(efectividad('Fuego', [])).toBe(1);
    expect(efectividad('Fuego', undefined as any)).toBe(1);
  });
});

describe('etiquetaEfec', () => {
  it('mapea el multiplicador al cartel', () => {
    expect(etiquetaEfec(0)).toBe('No afecta…');
    expect(etiquetaEfec(4)).toBe('¡Es muy eficaz!');
    expect(etiquetaEfec(2)).toBe('¡Es muy eficaz!');
    expect(etiquetaEfec(0.5)).toBe('No es muy eficaz…');
    expect(etiquetaEfec(0.25)).toBe('No es muy eficaz…');
    expect(etiquetaEfec(1)).toBe('');
  });
});

// ───────────────────────── helpers básicos ─────────────────────────
describe('hpMax / FORCEJEO / esEstado / tiposDe', () => {
  it('hpMax = 40 + nivel*5', () => {
    expect(hpMax(0)).toBe(40);
    expect(hpMax(1)).toBe(45);
    expect(hpMax(30)).toBe(190);
    expect(hpMax(50)).toBe(290);
  });
  it('FORCEJEO es Normal poder 40', () => {
    expect(FORCEJEO.tipo).toBe('Normal');
    expect(FORCEJEO.poder).toBe(40);
  });
  it('esEstado: categoría Estado o sin poder', () => {
    expect(esEstado(mov({ categoria: 'Estado', poder: 0 }))).toBe(true);
    expect(esEstado(mov({ poder: 0 }))).toBe(true);
    expect(esEstado(mov({ poder: undefined }))).toBe(true);
    expect(esEstado(mov({ poder: 50 }))).toBe(false);
  });
  it('tiposDe usa la data o cae a Normal', () => {
    expect(tiposDe(4, { '4': ['Fuego'] })).toEqual(['Fuego']);
    expect(tiposDe(999, {})).toEqual(['Normal']);
  });
});

// ───────────────────────── daño ─────────────────────────
describe('calcularDano', () => {
  it('STAB (1.5×) cuando el tipo del move coincide con el del atacante', () => {
    const conStab = calcularDano(luchador({ tipos: ['Fuego'] }), mov({ tipo: 'Fuego' }), luchador(), rng0);
    const sinStab = calcularDano(luchador({ tipos: ['Agua'] }), mov({ tipo: 'Fuego' }), luchador(), rng0);
    expect(conStab.stab).toBe(1.5);
    expect(sinStab.stab).toBe(1);
    expect(conStab.dmg).toBeGreaterThan(sinStab.dmg);
  });
  it('súper eficaz pega más que neutral y resistido pega menos', () => {
    const atk = luchador({ tipos: ['Agua'] }), m = mov({ tipo: 'Fuego', poder: 60 });
    const sup = calcularDano(atk, m, luchador({ tipos: ['Planta'] }), rng0);
    const neu = calcularDano(atk, m, luchador({ tipos: ['Normal'] }), rng0);
    const res = calcularDano(atk, m, luchador({ tipos: ['Agua'] }), rng0);
    expect(sup.dmg).toBeGreaterThan(neu.dmg);
    expect(neu.dmg).toBeGreaterThan(res.dmg);
  });
  it('contra inmune: efec=0 y daño 0 (no afecta)', () => {
    const r = calcularDano(luchador(), mov({ tipo: 'Normal' }), luchador({ tipos: ['Fantasma'] }), rng0);
    expect(r.efec).toBe(0);
    expect(r.dmg).toBe(0);
  });
  it('siempre al menos 1 de daño', () => {
    const r = calcularDano(luchador({ nivel: 1 }), mov({ poder: 1 }), luchador({ defMod: 2.2 }), rng0);
    expect(r.dmg).toBeGreaterThanOrEqual(1);
  });
  it('mayor nivel del atacante → más daño', () => {
    const lo = calcularDano(luchador({ nivel: 5 }), mov(), luchador(), rng0).dmg;
    const hi = calcularDano(luchador({ nivel: 50 }), mov(), luchador(), rng0).dmg;
    expect(hi).toBeGreaterThan(lo);
  });
  it('atkMod sube y defMod baja el daño', () => {
    const base = calcularDano(luchador(), mov(), luchador(), rng0).dmg;
    const conAtk = calcularDano(luchador({ atkMod: 2 }), mov(), luchador(), rng0).dmg;
    const conDef = calcularDano(luchador(), mov(), luchador({ defMod: 2 }), rng0).dmg;
    expect(conAtk).toBeGreaterThan(base);
    expect(conDef).toBeLessThan(base);
  });
  it('quemadura reduce solo el daño FÍSICO (no el especial)', () => {
    const fis = mov({ categoria: 'Físico', poder: 80 });
    const esp = mov({ categoria: 'Especial', poder: 80 });
    const fisNormal = calcularDano(luchador(), fis, luchador(), rng0).dmg;
    const fisQuemado = calcularDano(luchador({ estado: 'quemadura' }), fis, luchador(), rng0).dmg;
    const espNormal = calcularDano(luchador(), esp, luchador(), rng0).dmg;
    const espQuemado = calcularDano(luchador({ estado: 'quemadura' }), esp, luchador(), rng0).dmg;
    expect(fisQuemado).toBeLessThan(fisNormal);
    expect(espQuemado).toBe(espNormal);   // especial no se afecta
  });
  it('el rng mueve el daño en el rango 0.85–1.0', () => {
    const min = calcularDano(luchador({ nivel: 50 }), mov({ poder: 100 }), luchador(), rng(0)).dmg;
    const max = calcularDano(luchador({ nivel: 50 }), mov({ poder: 100 }), luchador(), rng(0.999)).dmg;
    expect(max).toBeGreaterThan(min);
  });
  it('poder ausente usa 40 por defecto', () => {
    const conPoder = calcularDano(luchador(), mov({ poder: 40 }), luchador(), rng0).dmg;
    const sinPoder = calcularDano(luchador(), mov({ poder: undefined }), luchador(), rng0).dmg;
    expect(sinPoder).toBe(conPoder);
  });
});

// ───────────────────────── movimientos de estado (stat mods) ─────────────────────────
describe('aplicarEstado (sube/baja stats)', () => {
  it('“baja el Ataque del rival” reduce atkMod del defensor (×0.7)', () => {
    const def = luchador();
    const txt = aplicarEstado(mov({ categoria: 'Estado', desc: 'Baja el Ataque del rival.' }), luchador(), def);
    expect(def.atkMod).toBeCloseTo(0.7, 5);
    expect(txt).toMatch(/Ataque.*bajó/);
  });
  it('“sube la Defensa” aumenta defMod del atacante (×1.4)', () => {
    const atk = luchador();
    aplicarEstado(mov({ categoria: 'Estado', desc: 'Aumenta la Defensa del usuario.' }), atk, luchador());
    expect(atk.defMod).toBeCloseTo(1.4, 5);
  });
  it('bajar repetido tiene piso 0.4', () => {
    const def = luchador();
    const m = mov({ categoria: 'Estado', desc: 'Baja el Ataque.' });
    for (let i = 0; i < 8; i++) aplicarEstado(m, luchador(), def);
    expect(def.atkMod).toBe(0.4);
  });
  it('subir repetido tiene techo 2.2', () => {
    const atk = luchador();
    const m = mov({ categoria: 'Estado', desc: 'Sube el Ataque.' });
    for (let i = 0; i < 8; i++) aplicarEstado(m, atk, luchador());
    expect(atk.atkMod).toBe(2.2);
  });
  it('sin stat reconocible no hace nada', () => {
    const def = luchador();
    const txt = aplicarEstado(mov({ categoria: 'Estado', desc: 'Hace algo raro.' }), luchador(), def);
    expect(txt).toBe('…pero no tuvo mucho efecto.');
    expect(def.atkMod).toBe(1);
  });
});

// ───────────────────────── SÚPER / IA ─────────────────────────
describe('danoSuper', () => {
  it('elige el movimiento de mayor efectividad', () => {
    const atk = luchador({ tipos: ['Agua'], movs: [mov({ tipo: 'Normal', poder: 60 }), mov({ tipo: 'Agua', poder: 50 })] });
    const def = luchador({ tipos: ['Fuego'] });   // Agua x2 Fuego
    const r = danoSuper(atk, def, 1, rng0);
    expect(r.mov.tipo).toBe('Agua');
  });
  it('mayor calidad → más daño (×2 a ×3.5)', () => {
    const atk = luchador({ movs: [mov({ poder: 80 })] });
    const lo = danoSuper(atk, luchador(), 0, rng0).dmg;
    const hi = danoSuper(atk, luchador(), 1, rng0).dmg;
    expect(hi).toBeGreaterThan(lo);
  });
  it('pega bastante más que un golpe normal', () => {
    const atk = luchador({ movs: [mov({ poder: 80 })] });
    const normal = calcularDano(atk, atk.movs[0], luchador(), rng0).dmg;
    const sup = danoSuper(atk, luchador(), 1, rng0).dmg;
    expect(sup).toBeGreaterThan(normal * 1.5);
  });
});

describe('elegirCPU', () => {
  it('prioriza efectividad × poder', () => {
    const atk = luchador({ movs: [
      mov({ id: 1, tipo: 'Fuego', poder: 40 }),   // vs Planta: 2×40 = 80
      mov({ id: 2, tipo: 'Normal', poder: 60 }),  // vs Planta: 1×60 = 60
    ] });
    expect(elegirCPU(atk, luchador({ tipos: ['Planta'] })).id).toBe(1);
  });
  it('evita el movimiento inmune aunque tenga más poder', () => {
    const atk = luchador({ movs: [
      mov({ id: 1, tipo: 'Normal', poder: 100 }),  // vs Fantasma: 0
      mov({ id: 2, tipo: 'Fuego', poder: 40 }),    // vs Fantasma: 1×40
    ] });
    expect(elegirCPU(atk, luchador({ tipos: ['Fantasma'] })).id).toBe(2);
  });
});

// ───────────────────────── precisión / estados ─────────────────────────
describe('acierta (precisión)', () => {
  it('precision 0 nunca; 100 siempre; sin precision = siempre', () => {
    expect(acierta(mov({ precision: 0 }), rng(0))).toBe(false);
    expect(acierta(mov({ precision: 100 }), rng(0.99))).toBe(true);
    expect(acierta(mov({ precision: null }), rng(0.99))).toBe(true);
    expect(acierta(mov({ precision: undefined }), rng(0.99))).toBe(true);
  });
  it('umbral exacto: rng*100 < precision', () => {
    expect(acierta(mov({ precision: 50 }), rng(0.49))).toBe(true);
    expect(acierta(mov({ precision: 50 }), rng(0.50))).toBe(false);   // 50 < 50 = false
  });
});

describe('puedeActuar (sueño/congelado/parálisis/confusión)', () => {
  it('congelado: 80% sigue congelado, 20% se descongela', () => {
    const f = luchador({ estado: 'congelado' });
    expect(puedeActuar(f, rng(0.9)).actua).toBe(false);
    const r = puedeActuar(f, rng(0.1)); expect(r.actua).toBe(true); expect(f.estado).toBeNull();
  });
  it('sueño: pierde turnos y despierta al agotar el contador', () => {
    const d = luchador({ estado: 'sueno', estadoT: 2 });
    expect(puedeActuar(d, rng(0.9)).actua).toBe(false);   // 2→1
    const r = puedeActuar(d, rng(0.9));                    // 1→0 despierta
    expect(r.actua).toBe(true); expect(d.estado).toBeNull();
  });
  it('parálisis: ~25% no se mueve', () => {
    const p = luchador({ estado: 'paralisis' });
    expect(puedeActuar(p, rng(0.1)).actua).toBe(false);
    expect(puedeActuar(p, rng(0.9)).actua).toBe(true);
    expect(p.estado).toBe('paralisis');   // la parálisis no se cura sola
  });
  it('confusión: a veces se autogolpea y dura un contador', () => {
    const cf = luchador({ estado: 'confusion', estadoT: 3 });
    const hp0 = cf.hp;
    const r = puedeActuar(cf, rng(0.1));   // 0.1<0.33 → autogolpe
    expect(r.actua).toBe(false);
    expect(r.autogolpe).toBeGreaterThan(0);
    expect(cf.hp).toBeLessThan(hp0);
  });
  it('confusión: se sale al agotar el contador', () => {
    const cf = luchador({ estado: 'confusion', estadoT: 1 });
    const r = puedeActuar(cf, rng(0.9));   // 1→0 sale
    expect(r.actua).toBe(true); expect(cf.estado).toBeNull();
  });
  it('sin estado: siempre actúa', () => {
    expect(puedeActuar(luchador(), rng(0.0)).actua).toBe(true);
  });
});

describe('aplicarAilment', () => {
  it('aplica el estado si pasa la chance y el rival está sano', () => {
    const def = luchador();
    const txt = aplicarAilment(mov({ ailment: 'veneno', ailmentChance: 100 }), luchador(), def, rng(0.5));
    expect(def.estado).toBe('veneno');
    expect(txt).toMatch(/envenenado/);
  });
  it('respeta la chance (no aplica si el rng no entra)', () => {
    const def = luchador();
    aplicarAilment(mov({ ailment: 'paralisis', ailmentChance: 30 }), luchador(), def, rng(0.5));  // 50 >= 30
    expect(def.estado).toBeNull();
  });
  it('no sobreescribe un estado existente', () => {
    const def = luchador({ estado: 'veneno' });
    aplicarAilment(mov({ ailment: 'sueno', ailmentChance: 100 }), luchador(), def, rng(0.1));
    expect(def.estado).toBe('veneno');
  });
  it('no aplica a un debilitado (hp<=0)', () => {
    const def = luchador({ hp: 0 });
    aplicarAilment(mov({ ailment: 'quemadura', ailmentChance: 100 }), luchador(), def, rng(0.1));
    expect(def.estado).toBeNull();
  });
  it('un move de Fuego descongela al defensor', () => {
    const def = luchador({ estado: 'congelado' });
    aplicarAilment(mov({ tipo: 'Fuego' }), luchador(), def, rng(0.9));
    expect(def.estado).toBeNull();
  });
  it('sueño y confusión arrancan con contador > 0', () => {
    const d1 = luchador();
    aplicarAilment(mov({ ailment: 'sueno', ailmentChance: 100 }), luchador(), d1, rng(0));
    expect(d1.estadoT).toBeGreaterThanOrEqual(1);
    const d2 = luchador();
    aplicarAilment(mov({ ailment: 'confusion', ailmentChance: 100 }), luchador(), d2, rng(0));
    expect(d2.estadoT).toBeGreaterThanOrEqual(1);
  });
});

describe('tickEstado (veneno/quemadura por turno)', () => {
  it('veneno y quemadura quitan floor(hpMax/8)', () => {
    for (const est of ['veneno', 'quemadura'] as const) {
      const c = luchador({ estado: est });
      const r = tickEstado(c);
      expect(r.dmg).toBe(Math.floor(c.hpMax / 8));
      expect(c.hp).toBe(c.hpMax - r.dmg);
    }
  });
  it('sin estado de daño no hace nada', () => {
    const c = luchador({ estado: 'paralisis' });
    expect(tickEstado(c).dmg).toBe(0);
    expect(c.hp).toBe(c.hpMax);
  });
  it('un debilitado no recibe daño residual', () => {
    const c = luchador({ estado: 'veneno', hp: 0 });
    expect(tickEstado(c).dmg).toBe(0);
  });
  it('no baja de 0 HP', () => {
    const c = luchador({ estado: 'veneno', hp: 1 });
    tickEstado(c);
    expect(c.hp).toBe(0);
  });
});

// ───────────────────────── stats base + críticos (Gen 3) ─────────────────────────
describe('stats efectivas (Gen 3)', () => {
  it('statEf = floor(2*base*L/100)+5', () => {
    expect(statEf(100, 50)).toBe(105);
    expect(statEf(60, 30)).toBe(41);
    expect(statEf(undefined as any, 30)).toBe(statEf(60, 30));   // default 60
  });
  it('hpEf = floor(2*base*L/100)+L+10', () => {
    expect(hpEf(160, 30)).toBe(136);   // Snorlax
    expect(hpEf(45, 30)).toBe(67);     // Caterpie
  });
  it('esFisico: categoría manda; si falta, por tipo (como Gen 3)', () => {
    expect(esFisico(mov({ tipo: 'Fuego', categoria: 'Físico' }))).toBe(true);
    expect(esFisico(mov({ tipo: 'Normal', categoria: 'Especial' }))).toBe(false);
    expect(esFisico(mov({ tipo: 'Normal' }))).toBe(true);    // Normal = físico por tipo
    expect(esFisico(mov({ tipo: 'Fuego' }))).toBe(false);    // Fuego = especial por tipo
  });
});

describe('golpes críticos', () => {
  it('CRIT_CHANCE = 1/16 y tiraCritico respeta el umbral', () => {
    expect(CRIT_CHANCE).toBeCloseTo(1 / 16, 6);
    expect(tiraCritico(rng(0))).toBe(true);        // 0 < 0.0625
    expect(tiraCritico(rng(0.5))).toBe(false);
  });
  it('un crítico pega ~2× (mismo rng) y marca crit', () => {
    const atk = luchador(), m = mov({ poder: 80 }), def = luchador();
    const normal = calcularDano(atk, m, def, rng0, false).dmg;
    const cr = calcularDano(atk, m, def, rng0, true);
    expect(cr.dmg).toBeGreaterThanOrEqual(normal * 2 - 1);
    expect(cr.dmg).toBeLessThanOrEqual(normal * 2 + 1);
    expect(cr.crit).toBe(true);
  });
});

describe('stats base en el daño', () => {
  it('mayor Ataque → más daño físico (Snorlax > Caterpie)', () => {
    const m = mov({ tipo: 'Normal', categoria: 'Físico', poder: 80 });
    const dS = calcularDano(luchador({ atk: 110 }), m, luchador(), rng0).dmg;
    const dC = calcularDano(luchador({ atk: 30 }), m, luchador(), rng0).dmg;
    expect(dS).toBeGreaterThan(dC);
  });
  it('mayor Defensa → recibe menos', () => {
    const m = mov({ categoria: 'Físico', poder: 80 });
    const blando = calcularDano(luchador(), m, luchador({ def: 30 }), rng0).dmg;
    const duro = calcularDano(luchador(), m, luchador({ def: 160 }), rng0).dmg;
    expect(duro).toBeLessThan(blando);
  });
  it('físico usa Atk/Def; especial usa At.Esp/Def.Esp', () => {
    const atk = luchador({ atk: 130, spa: 30 });   // fuerte físico, flojo especial
    const def = luchador();
    const fis = calcularDano(atk, mov({ tipo: 'Normal', categoria: 'Físico', poder: 80 }), def, rng0).dmg;
    const esp = calcularDano(atk, mov({ tipo: 'Normal', categoria: 'Especial', poder: 80 }), def, rng0).dmg;
    expect(fis).toBeGreaterThan(esp);
  });
});

describe('inmunidad de estado por tipo (Gen 3)', () => {
  it('Fuego no se quema', () => {
    const def = luchador({ tipos: ['Fuego'] });
    aplicarAilment(mov({ ailment: 'quemadura', ailmentChance: 100 }), luchador(), def, rng(0));
    expect(def.estado).toBeNull();
  });
  it('Hielo no se congela', () => {
    const def = luchador({ tipos: ['Hielo'] });
    aplicarAilment(mov({ tipo: 'Agua', ailment: 'congelado', ailmentChance: 100 }), luchador(), def, rng(0));
    expect(def.estado).toBeNull();
  });
  it('Veneno y Acero no se envenenan', () => {
    for (const t of ['Veneno', 'Acero']) {
      const def = luchador({ tipos: [t] });
      aplicarAilment(mov({ ailment: 'veneno', ailmentChance: 100 }), luchador(), def, rng(0));
      expect(def.estado).toBeNull();
    }
  });
  it('un tipo NO inmune sí recibe el estado', () => {
    const def = luchador({ tipos: ['Agua'] });
    aplicarAilment(mov({ ailment: 'quemadura', ailmentChance: 100 }), luchador(), def, rng(0));
    expect(def.estado).toBe('quemadura');
  });
});

// ───────────────────────── construcción con data inyectada ─────────────────────────
describe('movsDe / combatiente (data inyectada)', () => {
  const datos: DatosCombate = {
    nombres: { 4: 'Charmander' },
    tipos: { '4': ['Fuego'] },
    learnsets: { '4': [{ m: 10, n: 1 }, { m: 11, n: 5 }, { m: 12, n: 60 }] },
    movimientos: {
      '10': { nombre: 'Ascuas', tipo: 'Fuego', poder: 40 },
      '11': { nombre: 'Lanzallamas', tipo: 'Fuego', poder: 90 },
      '12': { nombre: 'Sofoco', tipo: 'Fuego', poder: 130 },
    },
  };
  it('usa los movimientos elegidos si la instancia los trae', () => {
    const ms = movsDe({ iid: 'a', id: 4, nivel: 30, movs: [11] }, datos.learnsets, datos.movimientos);
    expect(ms).toHaveLength(1);
    expect(ms[0].nombre).toBe('Lanzallamas');
  });
  it('sin elegir: top-4 por poder de los desbloqueados por nivel', () => {
    const ms = movsDe({ iid: 'a', id: 4, nivel: 30 }, datos.learnsets, datos.movimientos);
    // a nivel 30, el de poder 130 (n:60) NO está desbloqueado → quedan Lanzallamas(90) y Ascuas(40)
    expect(ms.map((m) => m.nombre)).toEqual(['Lanzallamas', 'Ascuas']);
  });
  it('sin movimientos posibles → FORCEJEO', () => {
    const ms = movsDe({ iid: 'a', id: 999, nivel: 5 }, datos.learnsets, datos.movimientos);
    expect(ms).toEqual([FORCEJEO]);
  });
  it('combatiente queda listo: hp lleno, mods en 1, sin estado', () => {
    const c = combatiente({ iid: 'a', id: 4, nivel: 20 }, datos);
    expect(c.nombre).toBe('Charmander');
    expect(c.tipos).toEqual(['Fuego']);
    expect(c.hp).toBe(hpMax(20));
    expect(c.hpMax).toBe(hpMax(20));
    expect(c.atkMod).toBe(1);
    expect(c.defMod).toBe(1);
    expect(c.estado).toBeNull();
    expect(c.movs.length).toBeGreaterThan(0);
  });
  it('respeta el mote por sobre el nombre', () => {
    const c = combatiente({ iid: 'a', id: 4, nivel: 20, mote: 'Chizu' }, datos);
    expect(c.nombre).toBe('Chizu');
  });
});
