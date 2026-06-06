import {
  efectividad, calcularDano, aplicarEstado, danoSuper, combatiente, hpMax,
  crearCombate, aplicarAccion, chequearFin, EstadoCombate, Combatiente, Mov,
} from './motor';

const rng0 = () => 0;          // determinista: rand = 0.85
const inst = (iid: string, id: number, nivel = 30, movs: number[] = []) => ({ iid, id, nivel, movs });

// Charmander(4)=Fuego, Bulbasaur(1)=Planta/Veneno → Fuego x2 contra Bulbasaur.
function combateBasico(): EstadoCombate {
  return crearCombate('r1', [
    { uid: 'A', nombre: 'Ash', equipo: [inst('a1', 4), inst('a2', 7)] },
    { uid: 'B', nombre: 'Gary', equipo: [inst('b1', 1), inst('b2', 152)] },
  ], 'A');
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

describe('máquina de estado de la sala', () => {
  it('crearCombate arma 2 jugadores con equipos y primer turno', () => {
    const e = combateBasico();
    expect(e.fase).toBe('combate');
    expect(e.turno).toBe('A');
    expect(e.jugadores).toHaveLength(2);
    expect(e.jugadores[0].equipo.length).toBe(2);
    expect(e.jugadores[0].equipo[0].hp).toBe(hpMax(30));
  });

  it('un ataque alterna el turno y carga la barra de súper', () => {
    const e = combateBasico();
    const r = aplicarAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    expect(r.error).toBeUndefined();
    expect(r.estado.turno).toBe('B');
    expect(r.estado.jugadores[0].super).toBeGreaterThan(0);
    expect(r.estado.jugadores[1].equipo[0].hp).toBeLessThan(hpMax(30));
  });

  it('rechaza una acción fuera de turno', () => {
    const e = combateBasico();
    const r = aplicarAccion(e, 'B', { tipo: 'mover', i: 0 }, rng0);
    expect(r.error).toBe('no-es-tu-turno');
    expect(e.turno).toBe('A');
  });

  it('cambiar de Pokémon cuesta el turno', () => {
    const e = combateBasico();
    const r = aplicarAccion(e, 'A', { tipo: 'cambiar', idx: 1 }, rng0);
    expect(r.error).toBeUndefined();
    expect(r.estado.jugadores[0].activo).toBe(1);
    expect(r.estado.turno).toBe('B');
  });

  it('súper: pausa, solo lo resuelve su dueño, aplica daño grande', () => {
    const e = combateBasico();
    e.jugadores[0].super = 100;
    const reto = aplicarAccion(e, 'A', { tipo: 'super' }, rng0);
    expect(reto.estado.fase).toBe('super');
    expect(reto.estado.superDe).toBe('A');
    // el rival no puede resolver el súper ajeno
    expect(aplicarAccion(e, 'B', { tipo: 'superResuelto', calidad: 1 }, rng0).error).toBe('no-es-tu-super');
    const hpAntes = e.jugadores[1].equipo[0].hp;
    const res = aplicarAccion(e, 'A', { tipo: 'superResuelto', calidad: 1 }, rng0);
    expect(res.error).toBeUndefined();
    expect(e.jugadores[1].equipo[0].hp).toBeLessThan(hpAntes);
    expect(e.fase).toBe('combate');
    expect(e.jugadores[0].super).toBe(0);
    expect(e.turno).toBe('B');
  });

  it('cuando el equipo rival llega a 0, declara ganador (fin)', () => {
    const e = combateBasico();
    // dejar a B con un solo Pokémon casi muerto
    e.jugadores[1].equipo = [e.jugadores[1].equipo[0]];
    e.jugadores[1].equipo[0].hp = 1;
    const r = aplicarAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    expect(r.estado.fase).toBe('fin');
    expect(r.estado.ganador).toBe('A');
    expect(chequearFin(r.estado)).toBe('A');
  });

  it('al debilitar el activo (con otro vivo) hace auto-switch sin terminar', () => {
    const e = combateBasico();
    e.jugadores[1].equipo[0].hp = 1;     // el activo de B cae, pero le queda b2
    const r = aplicarAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0);
    expect(r.estado.fase).toBe('combate');
    expect(r.estado.jugadores[1].activo).toBe(1);
    expect(r.estado.turno).toBe('B');
  });

  it('rendirse hace ganar al rival', () => {
    const e = combateBasico();
    const r = aplicarAccion(e, 'B', { tipo: 'rendirse' }, rng0);
    expect(r.estado.fase).toBe('fin');
    expect(r.estado.ganador).toBe('A');
  });

  it('no acepta acciones tras el fin', () => {
    const e = combateBasico();
    aplicarAccion(e, 'B', { tipo: 'rendirse' }, rng0);
    expect(aplicarAccion(e, 'A', { tipo: 'mover', i: 0 }, rng0).error).toBe('combate-terminado');
  });
});
