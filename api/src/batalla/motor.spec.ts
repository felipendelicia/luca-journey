import {
  efectividad, calcularDano, aplicarEstado, danoSuper, combatiente, hpMax,
  crearCombate, elegirAccion, chequearFin, EstadoCombate, Mov,
  acierta, puedeActuar, aplicarAilment, tickEstado,
} from './motor';

const rng0 = () => 0;          // determinista: rand = 0.85
const inst = (iid: string, id: number, nivel = 30, movs: number[] = []) => ({ iid, id, nivel, movs });

// helper: arma un combate simultáneo con 2 jugadores A/B
function combate(eqA: any[], eqB: any[]): EstadoCombate {
  return crearCombate('r', [
    { uid: 'A', nombre: 'Ash', equipo: eqA },
    { uid: 'B', nombre: 'Gary', equipo: eqB },
  ], 'A');
}

// Charmander(4)=Fuego, Bulbasaur(1)=Planta/Veneno → Fuego x2 contra Bulbasaur.
function combateBasico(): EstadoCombate {
  return combate([inst('a1', 4), inst('a2', 7)], [inst('b1', 1), inst('b2', 152)]);
}

describe('efectividad de tipos', () => {
  it('Fuego es muy eficaz contra Planta', () => {
    expect(efectividad('Fuego', ['Planta'])).toBe(2);
    expect(efectividad('Fuego', ['Planta', 'Veneno'])).toBe(2);   // x2 * x1
  });
  it('Agua no es muy eficaz contra Planta; Eléctrico no afecta a Tierra', () => {
    expect(efectividad('Agua', ['Planta'])).toBe(0.5);
    expect(efectividad('Eléctrico', ['Tierra'])).toBe(0);
  });
});

describe('calcularDano', () => {
  it('aplica el multiplicador super-eficaz (más daño que neutro)', () => {
    const atk = combatiente(inst('x', 4, 30));
    const defPlanta = combatiente(inst('y', 1, 30));   // Planta/Veneno
    const defNeutro = combatiente(inst('z', 19, 30));   // Rattata = Normal
    const mov: Mov = { id: 99, nombre: 'Llamarada', tipo: 'Fuego', poder: 60 };
    const sup = calcularDano(atk, mov, defPlanta, rng0);
    const neu = calcularDano(atk, mov, defNeutro, rng0);
    expect(sup.efec).toBe(2);
    expect(sup.dmg).toBeGreaterThan(neu.dmg);
  });
});

describe('aplicarEstado', () => {
  it('un movimiento que baja el Ataque reduce el atkMod del rival', () => {
    const atk = combatiente(inst('x', 4));
    const def = combatiente(inst('y', 1));
    const mov: Mov = { id: 1, nombre: 'Malicioso', tipo: 'Normal', categoria: 'Estado', desc: 'Baja el Ataque del rival.' };
    aplicarEstado(mov, atk, def);
    expect(def.atkMod).toBeLessThan(1);
  });
});

describe('danoSuper', () => {
  it('pega bastante más que un golpe normal', () => {
    const atk = combatiente(inst('x', 4, 30));
    const def = combatiente(inst('y', 1, 30));
    const normal = calcularDano(atk, atk.movs[0], def, rng0);
    const sup = danoSuper(atk, def, 1, rng0);
    expect(sup.dmg).toBeGreaterThan(normal.dmg * 1.5);
  });
});

describe('combate SIMULTÁNEO', () => {
  it('crearCombate arma 2 jugadores en fase combate, acciones vacías', () => {
    const e = combateBasico();
    expect(e.fase).toBe('combate');
    expect(e.acciones['A']).toBeNull();
    expect(e.acciones['B']).toBeNull();
    expect(e.jugadores).toHaveLength(2);
    expect(e.jugadores[0].equipo.length).toBe(2);
    expect(e.jugadores[0].equipo[0].hp).toBe(e.jugadores[0].equipo[0].hpMax);
  });

  it('no resuelve hasta que ambos eligen', () => {
    const e = combate([inst('a1', 25, 50)], [inst('b1', 143, 50)]);   // Pikachu vs Snorlax
    const r1 = elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    expect(r1.listo).toBe(true);
    expect(r1.eventos.length).toBe(0);
    expect(e.acciones['A']).not.toBeNull();   // A quedó almacenada
    expect(e.acciones['B']).toBeNull();
    const r2 = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(r2.eventos.length).toBeGreaterThan(0);   // ahora SÍ resuelve
    expect(e.acciones['A']).toBeNull();             // limpia tras resolver
    expect(e.acciones['B']).toBeNull();
  });

  it('re-pick permitido si el rival no eligió', () => {
    const e = combate([inst('a1', 25, 50)], [inst('b1', 143, 50)]);
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    const r = elegirAccion(e, 'A', { tipo: 'mover', i: 1 }, rng0);
    expect(r.error).toBeUndefined();
    expect(e.acciones['A']!.i).toBe(1);   // sobrescribió la elección anterior
    expect(e.acciones['B']).toBeNull();   // sigue sin resolver
  });

  it('el más rápido (Pikachu) pega primero', () => {
    const e = combate([inst('a1', 25, 50)], [inst('b1', 143, 50)]);   // Pikachu spe>Snorlax
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    const movs = r.eventos.filter((ev: any) => ev.t === 'mover');
    expect(movs.length).toBeGreaterThan(0);
    expect(movs[0].uid).toBe('A');   // A (Pikachu, más rápido) pega primero
  });

  it('KO sin banca → fin con el ganador correcto', () => {
    const e = combate([inst('a1', 150, 90)], [inst('b1', 129, 2)]);   // Mewtwo vs Magikarp lvl2
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.fase).toBe('fin');         // Mewtwo (rápido) noquea al Magikarp en un golpe
    expect(e.ganador).toBe('A');
    expect(chequearFin(e)).toBe('A');
    expect(r.eventos.some((ev: any) => ev.t === 'fin')).toBe(true);
  });

  it('acciones quedan limpias tras una ronda resuelta (sin KO)', () => {
    const e = combate([inst('a1', 25, 50)], [inst('b1', 143, 50)]);
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.fase).toBe('combate');
    expect(e.acciones['A']).toBeNull();
    expect(e.acciones['B']).toBeNull();
    expect(e.turnoN).toBe(2);   // avanzó de ronda
  });

  it('cambiar de Pokémon se resuelve junto a la ronda', () => {
    const e = combateBasico();
    elegirAccion(e, 'A', { tipo: 'cambiar', idx: 1 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(r.eventos.some((ev: any) => ev.t === 'cambiar')).toBe(true);
    expect(e.jugadores[0].activo).toBe(1);
  });

  it('rechaza cambio inválido (índice debilitado)', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[1].hp = 0;
    const r = elegirAccion(e, 'A', { tipo: 'cambiar', idx: 1 }, rng0);
    expect(r.error).toBe('debilitado');
    expect(e.acciones['A']).toBeNull();
  });

  it('súper en slot: golpe grande, gasta la barra, evento super', () => {
    const e = combate([inst('a1', 4, 30)], [inst('b1', 1, 30)]);
    e.jugadores[0].super = 100;
    const hpAntes = e.jugadores[1].equipo[0].hp;
    elegirAccion(e, 'A', { tipo: 'super', calidad: 1 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(r.eventos.some((ev: any) => ev.t === 'super')).toBe(true);
    expect(e.jugadores[1].equipo[0].hp).toBeLessThan(hpAntes);
    expect(e.jugadores[0].super).toBe(0);
  });

  it('súper rechazado si la barra no está llena', () => {
    const e = combate([inst('a1', 4, 30)], [inst('b1', 1, 30)]);
    e.jugadores[0].super = 50;
    const r = elegirAccion(e, 'A', { tipo: 'super', calidad: 1 }, rng0);
    expect(r.error).toBe('super-no-listo');
  });

  it('reemplazo: tras un KO con banca, pasa a fase reemplazo y luego vuelve a combate', () => {
    const e = combate([inst('a1', 150, 90)], [inst('b1', 129, 2), inst('b2', 1, 30)]);
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.fase).toBe('reemplazo');
    expect(e.reemplazan).toContain('B');
    const r2 = elegirAccion(e, 'B', { tipo: 'reemplazo', idx: 1 }, rng0);
    expect(r2.error).toBeUndefined();
    expect(e.jugadores[1].activo).toBe(1);
    expect(e.fase).toBe('combate');
    expect(e.acciones['A']).toBeNull();
    expect(e.acciones['B']).toBeNull();
  });

  it('rendirse hace ganar al rival', () => {
    const e = combateBasico();
    const r = elegirAccion(e, 'B', { tipo: 'rendirse' }, rng0);
    expect(e.fase).toBe('fin');
    expect(e.ganador).toBe('A');
    expect(r.eventos.length).toBeGreaterThan(0);
  });

  it('no acepta acciones tras el fin', () => {
    const e = combateBasico();
    elegirAccion(e, 'B', { tipo: 'rendirse' }, rng0);
    expect(elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0).error).toBe('combate-terminado');
  });

  it('carga la barra de súper al atacar', () => {
    const e = combate([inst('a1', 25, 50)], [inst('b1', 143, 50)]);
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    // A (Pikachu, más rápido) actúa → su barra carga
    expect(e.jugadores[0].super).toBeGreaterThan(0);
  });
});

describe('estados alterados + fallar', () => {
  const c = () => combatiente(inst('x', 4, 30));

  it('acierta según la precisión', () => {
    expect(acierta({ id: 1, nombre: 'm', tipo: 'Normal', precision: 0 }, () => 0.5)).toBe(false);
    expect(acierta({ id: 1, nombre: 'm', tipo: 'Normal', precision: 100 }, () => 0.99)).toBe(true);
    expect(acierta({ id: 1, nombre: 'm', tipo: 'Normal' }, () => 0.99)).toBe(true);   // sin precision = siempre
  });

  it('veneno y quemadura quitan ~1/8 del HP máximo', () => {
    const v = c(); v.estado = 'veneno';
    const tk = tickEstado(v);
    expect(tk.dmg).toBe(Math.floor(v.hpMax / 8));
    expect(v.hp).toBe(v.hpMax - tk.dmg);
  });

  it('quemadura reduce el daño físico a la mitad', () => {
    const atk = c(); const def = combatiente(inst('y', 1, 30));
    const mov: Mov = { id: 1, nombre: 'Golpe', tipo: 'Normal', poder: 80, categoria: 'Físico' };
    const normal = calcularDano(atk, mov, def, rng0).dmg;
    atk.estado = 'quemadura';
    const quemado = calcularDano(atk, mov, def, rng0).dmg;
    expect(quemado).toBeLessThan(normal);
  });

  it('dormido pierde el turno y se despierta al agotar el contador', () => {
    const d = c(); d.estado = 'sueno'; d.estadoT = 2;
    expect(puedeActuar(d, () => 0.9).actua).toBe(false);   // T:2->1
    const r = puedeActuar(d, () => 0.9);                    // T:1->0 → despierta
    expect(r.actua).toBe(true); expect(d.estado).toBeNull();
  });

  it('paralizado a veces no se mueve (rng < 0.25)', () => {
    const p = c(); p.estado = 'paralisis';
    expect(puedeActuar(p, () => 0.1).actua).toBe(false);
    expect(puedeActuar(p, () => 0.9).actua).toBe(true);
  });

  it('congelado no actúa, pero un 20% se descongela', () => {
    const f = c(); f.estado = 'congelado';
    expect(puedeActuar(f, () => 0.9).actua).toBe(false);
    const r = puedeActuar(f, () => 0.05); expect(r.actua).toBe(true); expect(f.estado).toBeNull();
  });

  it('confuso a veces se golpea a sí mismo', () => {
    const cf = c(); cf.estado = 'confusion'; cf.estadoT = 3; const hp0 = cf.hp;
    const r = puedeActuar(cf, () => 0.1);   // 0.1 < 0.33 → autogolpe
    expect(r.actua).toBe(false); expect(r.autogolpe).toBeGreaterThan(0); expect(cf.hp).toBeLessThan(hp0);
  });

  it('aplicarAilment respeta la chance y un solo estado a la vez', () => {
    const atk = c(); const def = combatiente(inst('y', 19, 30));   // Rattata (Normal): no es inmune al veneno
    const tox: Mov = { id: 92, nombre: 'Tóxico', tipo: 'Veneno', categoria: 'Estado', ailment: 'veneno', ailmentChance: 0 };  // 0 = garantizado
    expect(aplicarAilment(tox, atk, def, () => 0.5)).toContain('envenenado');
    expect(def.estado).toBe('veneno');
    // ya tiene estado → no se sobreescribe
    const slp: Mov = { id: 1, nombre: 'x', tipo: 'Psíquico', ailment: 'sueno', ailmentChance: 100 };
    expect(aplicarAilment(slp, atk, def, () => 0.1)).toBe('');
    expect(def.estado).toBe('veneno');
  });

  it('un ataque inmune (Normal vs Fantasma) hace 0 daño y avisa "no afecta"', () => {
    // Jolteon(135, rápido) usa un move Normal contra Gengar(94)=Fantasma → Normal x0 Fantasma.
    const e = combate([inst('a', 135)], [inst('b', 94)]);
    e.jugadores[0].equipo[0].movs = [{ id: 1, nombre: 'Placaje', tipo: 'Normal', poder: 80 } as Mov];
    const hp0 = e.jugadores[1].equipo[0].hp;
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.jugadores[1].equipo[0].hp).toBe(hp0);   // sin daño
    expect(r.eventos.some((ev: any) => /no afecta/i.test(ev.texto))).toBe(true);
  });

  it('un ataque que falla (precisión 0) no hace daño', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[0].movs = [{ id: 1, nombre: 'Falla', tipo: 'Normal', poder: 80, precision: 0 } as Mov];
    const hp0 = e.jugadores[1].equipo[0].hp;
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, () => 0.99);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, () => 0.99);
    expect(r.error).toBeUndefined();
    expect(e.jugadores[1].equipo[0].hp).toBe(hp0);   // no daño del move fallado de A
  });
});

describe('items en PvP (cura/estado/revivir)', () => {
  it('antídoto cura el envenenamiento del activo', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[0].estado = 'veneno';
    elegirAccion(e, 'A', { tipo: 'pocion', itemId: 'antidoto' }, rng0);
    const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(r.error).toBeUndefined();
    expect(e.jugadores[0].equipo[0].estado).toBeNull();
  });
  it('antídoto sin veneno se rechaza', () => {
    const e = combateBasico();
    expect(elegirAccion(e, 'A', { tipo: 'pocion', itemId: 'antidoto' }, rng0).error).toBe('no-aplica');
    expect(e.acciones['A']).toBeNull();
  });
  it('revivir trae de vuelta a un debilitado al 50% HP', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[1].hp = 0;
    elegirAccion(e, 'A', { tipo: 'pocion', itemId: 'revivir' }, rng0);
    elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    const revivido = e.jugadores[0].equipo[1];
    expect(revivido.hp).toBe(Math.round(revivido.hpMax * 0.5));
  });
});

describe('velocidad y PP en la sala', () => {
  it('un move sin PP recurre a Forcejeo cuando no queda nada', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[0].movs = [{ id: 5, nombre: 'X', tipo: 'Normal', poder: 40, pp: 0, ppMax: 5 } as Mov];
    const hp0 = e.jugadores[1].equipo[0].hp;
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.jugadores[1].equipo[0].hp).toBeLessThan(hp0);   // Forcejeo igual pegó
  });
  it('consume PP al usar un movimiento', () => {
    const e = combateBasico();
    e.jugadores[0].equipo[0].movs = [{ id: 5, nombre: 'X', tipo: 'Normal', poder: 40, pp: 3, ppMax: 5 } as Mov];
    elegirAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    elegirAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(e.jugadores[0].equipo[0].movs[0].pp).toBe(2);
  });
});
