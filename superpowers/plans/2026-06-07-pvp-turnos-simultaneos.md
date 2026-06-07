# PvP turnos simultáneos + UX + typewriter — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rehacer el combate PvP a selección **simultánea** (ambos eligen, se resuelve por prioridad/velocidad), con súper en paralelo, timeout/auto-move, UX clara de los flujos y texto que se escribe letra por letra (FireRed) con ritmo más lento.

**Architecture:** Reglas puras en `web/src/lib/combate-core.ts` (fuente única; `api/scripts/sync-batalla-data.mjs` la copia a `api/src/batalla/`; tests jest en `api/`). La máquina de estado de la ronda vive en `api/src/batalla/motor.ts` (server-autoritativo). El gateway (`salas.service.ts`) maneja timer/auto-move/forfeit y emite eventos de ronda. El cliente (`batalla.astro` + `batalla-online.js`) maneja selección, bloqueo, reveal, reemplazo y la narración typewriter (compartida con práctica).

**Tech Stack:** TypeScript (combate-core/motor/salas, NestJS+socket.io), JS módulos (batalla-online), Astro (batalla.astro), Jest (api), `/frontend-design` para UI.

**Convención:** specs/plans en `superpowers/` (raíz). Sin atribución Claude. UI → `/frontend-design`. Core: editar `web/src/lib/combate-core.ts`, `cd api && node scripts/sync-batalla-data.mjs`, tests en `api/src/batalla/combate-core.spec.ts`. `api/src/batalla/combate-core.ts` es GENERADO. Spec: `superpowers/specs/2026-06-07-pvp-turnos-simultaneos-design.md`.

**Contexto actual (motor.ts):**
- `EstadoCombate { roomId; jugadores:[J,J]; turno:string; fase:'seleccion'|'combate'|'super'|'fin'; ganador?; superDe?; eventos:Evento[]; turnoN }`. `JugadorEstado { uid; nombre; equipo:Combatiente[]; activo; super; listo }`. `Combatiente` tiene `id,hp,hpMax,spe,movs,estado,...,iid`.
- `aplicarAccion(e, uid, accion)` resuelve UNA acción (mover/cambiar/pocion/super/superResuelto/rendirse) y `pasarTurno`. Helpers: `activoDe(j)`, `rivalDe(e,uid)`, `jugadorDe(e,uid)`, `vivos(j)`, `postGolpe`, `autoSwitch`, `snapshot(e)`. Constantes `SUPER_MAX=100`, `SUPER_GANANCIA=25`, `POCION_CURA`, `CURA_ESTADO`, `REVIVE`.
- `salas.service.arrancar` emite `estado`+`tuTurno`; `accion(client,uid,accion)` llama `aplicarAccion`, emite `estado`, maneja `super`/`fin`/`tuTurno`.
- `batalla-online.js`: `mover(i)/cambiar(idx)/usarPocion(id)/lanzarSuper()/resolverSuper(cal)/rendirse()`, `onBatalla(ev,fn)`.
- `batalla.astro` modo En vivo: `renderOnline()`, `finOnline()`, menú de acción, panel de súper (reto), banca.

---

### Task 1: `combate-core.ts` — prioridad de movimientos + orden de lanzadores (puro + tests)

**Files:** Modify `web/src/lib/combate-core.ts`; Test `api/src/batalla/combate-core.spec.ts`.

- [ ] **Step 1: Test (FALLA)** — APPEND a `api/src/batalla/combate-core.spec.ts`:
```ts
import { prioridadMov, ordenLanzadores, PRIORIDAD_MOV } from './combate-core';
describe('orden de turno (PvP simultáneo)', () => {
  test('prioridadMov: del mapa o 0 por default', () => {
    expect(prioridadMov({ id: 1, nombre: 'Ataque Rápido', tipo: 'Normal' } as any)).toBe(1);
    expect(prioridadMov({ id: 2, nombre: 'Placaje', tipo: 'Normal' } as any)).toBe(0);
    expect(typeof PRIORIDAD_MOV).toBe('object');
  });
  test('ordenLanzadores: mayor prioridad va primero', () => {
    expect(ordenLanzadores({ prio: 1, spe: 10 }, { prio: 0, spe: 99 }, () => 0.5)).toBeLessThan(0);
  });
  test('ordenLanzadores: misma prioridad → mayor velocidad primero', () => {
    expect(ordenLanzadores({ prio: 0, spe: 120 }, { prio: 0, spe: 80 }, () => 0.5)).toBeLessThan(0);
  });
  test('ordenLanzadores: empate total → desempate por rng (determinista)', () => {
    const a = { prio: 0, spe: 80 }, b = { prio: 0, spe: 80 };
    expect(ordenLanzadores(a, b, () => 0.0)).toBeLessThan(0);   // rng<0.5 → A primero
    expect(ordenLanzadores(a, b, () => 0.9)).toBeGreaterThan(0); // rng>=0.5 → B primero
  });
});
```

- [ ] **Step 2: Correr (FALLA)**: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core -t "orden de turno"` → FAIL.

- [ ] **Step 3: Implementar en `web/src/lib/combate-core.ts`** (cerca de `calcularDano`):
```ts
// ───────────────────────── orden de turno (PvP simultáneo) ─────────────────────────
// prioridad de movimiento (mapa curado por NOMBRE ES; default 0). Los positivos pegan antes.
export const PRIORIDAD_MOV: Record<string, number> = {
  'Velocidad Extrema': 2,
  'Ataque Rápido': 1, 'Aqua Jet': 1, 'Sombra Vil': 1, 'Bote': 1, 'As Aéreo': 1, 'Bala Roca': 1, 'Viento Hielo': 1,
  'Protección': 4, 'Detección': 4, 'Anticipo': 1,
};
export const prioridadMov = (mov: Mov): number => PRIORIDAD_MOV[mov?.nombre || ''] ?? 0;
// orden de dos lanzadores: prioridad desc, luego velocidad desc, luego desempate por rng. <0 = A primero.
export function ordenLanzadores(a: { prio: number; spe: number }, b: { prio: number; spe: number }, rng: Rng = Math.random): number {
  if (a.prio !== b.prio) return b.prio - a.prio;
  if (a.spe !== b.spe) return b.spe - a.spe;
  return rng() < 0.5 ? -1 : 1;
}
```
(El plan asume que los nombres del mapa existen en `movimientos.json`; los que no, simplemente nunca matchean → prioridad 0. No rompe.)

- [ ] **Step 4: Correr (PASA)**: `cd api && node scripts/sync-batalla-data.mjs && npx jest combate-core` → toda verde.

- [ ] **Step 5: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/combate-core.ts api/src/batalla/combate-core.ts api/src/batalla/combate-core.spec.ts
git commit -m "core: prioridad de movimientos + ordenLanzadores (PvP simultáneo) — puro + tests"
```

---

### Task 2: `motor.ts` — máquina de estado SIMULTÁNEA (elegirAccion + resolverRonda)

**Files:** Modify `api/src/batalla/motor.ts`; Test `api/src/batalla/motor.spec.ts`.

Esta es la tarea central. READ `api/src/batalla/motor.ts` entero primero (especialmente el `switch` de `aplicarAccion`, que tiene la lógica de daño/estado/contacto/súper a REUSAR).

**Diseño:**
- `Accion = { tipo: 'mover'|'cambiar'|'pocion'|'super'|'reemplazo'|'rendirse'; i?: number; idx?: number; itemId?: string; calidad?: number }`.
- `EstadoCombate` cambia: `fase: 'seleccion'|'combate'|'reemplazo'|'fin'` (se va `'super'`); agrega `acciones: Record<string, Accion|null>`; `timeouts: Record<string, number>`; `reemplazan?: string[]` (uids que deben reemplazar). Se quitan `turno`/`superDe` del uso (dejar `turno` opcional para compat de snapshot si hace falta, pero la lógica usa `acciones`). Mantener `turnoN` como nº de ronda.
- Importar de `./combate-core`: `prioridadMov, ordenLanzadores` (sumar al import existente).

**Step 1: Tests (FALLAN)** — REEMPLAZAR el contenido de `api/src/batalla/motor.spec.ts` por tests del modelo simultáneo (read el archivo viejo para reusar helpers de armado de estado). Tests mínimos:
```ts
import { crearCombate, elegirAccion, EstadoCombate } from './motor';
// helper: arma un combate de 1 mon por lado con stats controlados via Inst (nivel fijo)
function combate(): EstadoCombate {
  return crearCombate('r', [
    { uid: 'A', nombre: 'A', equipo: [{ iid: 'a1', id: 25, nivel: 50 }] },   // Pikachu (rápido)
    { uid: 'B', nombre: 'B', equipo: [{ iid: 'b1', id: 143, nivel: 50 }] },  // Snorlax (lento)
  ], 'A');
}
test('elegirAccion no resuelve hasta que ambos eligen', () => {
  const e = combate();
  const r1 = elegirAccion(e, 'A', { tipo: 'mover', i: 0 });
  expect(r1.listo).toBe(true);                  // A eligió, espera a B
  expect(e.acciones['A']).toBeTruthy();
  expect(e.acciones['B']).toBeNull();
  const r2 = elegirAccion(e, 'B', { tipo: 'mover', i: 0 });
  expect(r2.eventos.length).toBeGreaterThan(0); // ambos → resolvió la ronda
  expect(e.acciones['A']).toBeNull();           // limpiado para la próxima
});
test('se puede re-elegir mientras el rival no eligió', () => {
  const e = combate();
  elegirAccion(e, 'A', { tipo: 'mover', i: 0 });
  const r = elegirAccion(e, 'A', { tipo: 'mover', i: 1 });  // cambia su jugada
  expect(r.error).toBeUndefined();
  expect(e.acciones['A'].i).toBe(1);
});
test('el más rápido pega primero (Pikachu antes que Snorlax)', () => {
  const e = combate();
  elegirAccion(e, 'A', { tipo: 'mover', i: 0 });
  const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 });
  const movs = r.eventos.filter((ev) => ev.t === 'mover');
  expect(movs[0].uid).toBe('A');   // Pikachu (más rápido) primero
});
test('debilitado dispara reemplazo (si hay banca)', () => {
  // armar B con 1 mon de 1 HP y A con un golpe fuerte → B cae → si B tuviera banca, fase reemplazo;
  // con 1 solo mon, fase 'fin' y ganador A.
  const e = crearCombate('r', [
    { uid: 'A', nombre: 'A', equipo: [{ iid: 'a1', id: 150, nivel: 80 }] },
    { uid: 'B', nombre: 'B', equipo: [{ iid: 'b1', id: 10, nivel: 2 }] },
  ], 'A');
  elegirAccion(e, 'A', { tipo: 'mover', i: 0 });
  const r = elegirAccion(e, 'B', { tipo: 'mover', i: 0 });
  expect(['fin', 'reemplazo', 'combate']).toContain(e.fase);
});
```
(Ajustar los ids/niveles a especies reales del data; el objetivo es: simultaneidad, re-pick, orden por velocidad, y que un debilitado lleve a `fin`/`reemplazo`. El subagente puede afinar los asserts con números reales.)

**Step 2: Correr (FALLA)**: `cd api && node scripts/sync-batalla-data.mjs && npx jest motor` → FAIL (`elegirAccion` no existe).

**Step 3: Implementar en `motor.ts`:**
1. Tipos/estado: agregar `Accion`, ampliar `Fase` a `'seleccion'|'combate'|'reemplazo'|'fin'`, agregar a `EstadoCombate` `acciones`/`timeouts`/`reemplazan?`. En `crearCombate`, inicializar `acciones: { [uidA]: null, [uidB]: null }`, `timeouts: { [uidA]: 0, [uidB]: 0 }`, `fase: 'combate'`, además de lo que ya hace (equipos, eventos del habAlEntrar inicial).
2. Extraer la lógica de un movimiento/súper a un helper reusable a partir del `case 'mover'` y `case 'superResuelto'` actuales:
```ts
// ejecuta el movimiento/súper del jugador `yo` contra `rival`. Empuja eventos. NO pasa turno ni auto-switch.
function ejecutarAtaque(e: EstadoCombate, yo: JugadorEstado, rival: JugadorEstado, acc: Accion, push: PushFn, rng: Rng) {
  const atk = activoDe(yo), def = activoDe(rival);
  if (atk.hp <= 0) return;                       // cayó antes de actuar (por el golpe del rival)
  if (acc.tipo === 'super') {
    const cal = Math.max(0, Math.min(1, acc.calidad ?? 0));
    const r = danoSuper(atk, def, cal, rng); def.hp = Math.max(0, def.hp - r.dmg); yo.super = 0;
    push('super', `⚡ ¡SÚPER de ${atk.nombre}! ${r.mov.nombre} causa ${r.dmg} de daño.`, { dmg: r.dmg, uid: yo.uid });
    return;
  }
  // === mover: copiar la lógica del case 'mover' actual (PP, puedeActuar, acierta, esEstado/calcularDano,
  // aplicarAilment, habAlContacto, ganancia de súper) — los pushes llevan { uid: yo.uid } ===
  ...
}
```
3. `elegirAccion(e, uid, accion, rng = Math.random): { estado, eventos, listo?, error? }`:
   - `if (e.fase === 'fin') return err`. `rendirse` → fin (ganador rival).
   - **fase 'reemplazo'**: aceptar solo de los uids en `e.reemplazan`; setear `jugadorDe(uid).activo = accion.idx` (validando vivo); sacarlo de `reemplazan`; push `entra` + `habAlEntrar`. Cuando `reemplazan` vacío → `fase:'combate'`, limpiar `acciones`, `turnoN++`. Devolver eventos.
   - **fase 'combate'**: validar (no debilitado para mover; súper solo si `yo.super>=SUPER_MAX`; cambio válido; etc.). `e.acciones[uid] = accion; e.timeouts[uid] = 0`. Si **ambos** `acciones` no-null → `return resolverRonda(e, rng)`. Si no → `return { estado:e, eventos:[], listo:true }`.
4. `resolverRonda(e, rng): { estado, eventos }`:
   - `const eventos: Evento[] = []; const push = (t,texto,extra={}) => { const ev={t,texto,...extra}; eventos.push(ev); e.eventos.push(ev); };`
   - `const [jA, jB] = e.jugadores; const aA = e.acciones[jA.uid]!, aB = e.acciones[jB.uid]!;`
   - **cambios**: para cada (j, acc) con `acc.tipo==='cambiar'`: `j.activo = acc.idx`; push `cambiar`; `habAlEntrar(activoDe(j), activoDe(rivalDe(e,j.uid)))`.
   - **pociones**: para cada `acc.tipo==='pocion'`: aplicar (copiar la lógica del `case 'pocion'` actual).
   - **ataques**: armar `lanz = [{j:jA, acc:aA},{j:jB, acc:aB}].filter(x => x.acc.tipo==='mover'||x.acc.tipo==='super')`. Ordenar con `ordenLanzadores({prio: acc.tipo==='super'?0:prioridadMov(activoDe(j).movs[acc.i??0]||FORCEJEO), spe: activoDe(j).spe}, ...)`. Para cada en orden: `ejecutarAtaque(e, x.j, rivalDe(e,x.j.uid), x.acc, push, rng)`.
   - **DOT**: `for (const j of e.jugadores) { const tk = tickEstado(activoDe(j)); if (tk.dmg) push('dot', tk.texto, { dmg: tk.dmg, uid: j.uid }); }`
   - **fin/reemplazo**: `const fin = chequearFin(e); if (fin) { e.fase='fin'; e.ganador=fin; push('fin', ...); return {estado:e,eventos}; }`. Luego `e.reemplazan = e.jugadores.filter(j => activoDe(j).hp<=0 && vivos(j)>0).map(j=>j.uid);` Si `reemplazan.length` → `e.fase='reemplazo'` (no limpiar acciones aún; el cliente pedirá reemplazo). Si no → limpiar `acciones`=null/null, `turnoN++`, `fase` sigue `combate`.
   - return `{estado:e, eventos}`.
5. `snapshot(e)`: incluir `fase`, `reemplazan`, `acciones` solo como "quién ya eligió" (NO revelar la acción del rival: emitir `elegidos: { [uid]: !!e.acciones[uid] }` en vez de las acciones crudas). Mantener el resto (equipos, hp, activos, super, turnoN, ganador).
6. Quitar/retirar `pasarTurno` y el viejo `aplicarAccion` (o dejar `aplicarAccion` como wrapper deprecado que llama `elegirAccion`). `chequearFin`, `autoSwitch`, `postGolpe` se reusan/ajustan.

**Step 4: Correr (PASA)**: `cd api && node scripts/sync-batalla-data.mjs && npx jest motor` → verde. Ajustar asserts a números reales si hace falta (sin debilitarlos).

**Step 5: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api/src/batalla/motor.ts api/src/batalla/motor.spec.ts
git commit -m "motor: combate PvP SIMULTÁNEO (elegirAccion + resolverRonda: cambios→ítems→moves por prioridad/velocidad, reemplazo, súper en slot)"
```

---

### Task 3: `salas.service.ts` + gateway — timer de ronda, auto-move, forfeit, eventos

**Files:** Modify `api/src/batalla/salas.service.ts` (y `batalla.gateway.ts` si mapea eventos).

READ `salas.service.ts` (`arrancar`, `accion`, `finalizar`, timers de gracia).

- [ ] **Step 1: Reemplazar el handler `accion`** para el modelo simultáneo:
  - `elegir(client, uid, accion)`: `const r = elegirAccion(sala.estado, uid, accion);` si `r.error` → emitir error. Emitir a la sala `snapshot` actualizado. Avisar al rival `rivalListo` (para habilitar/deshabilitar "cambiar"). Si la ronda **resolvió** (`r.eventos.length` y `acciones` quedaron limpias / o fase cambió) → emitir `resolucion { snap: snapshot(estado), eventos: r.eventos }` a ambos; si `fase==='reemplazo'` emitir `reemplazo { uids: estado.reemplazan }`; si `fase==='fin'` → `finalizar`. Si solo se guardó (espera) → emitir `esperando` al que eligió.
  - mapear el emit del cliente `elegir` (Task 4) a este handler.
- [ ] **Step 2: Timer de ronda.** Al entrar a una ronda de selección (en `arrancar` y tras cada `resolución`/`reemplazo` que vuelve a `combate`), arrancar `sala.rondaTimer = setTimeout(() => this.timeoutRonda(sala), 30000)` y emitir `ronda { deadline: Date.now()+30000 }`. En `timeoutRonda`: para cada uid sin `sala.estado.acciones[uid]`, setear `elegirAccion(estado, uid, { tipo:'mover', i: idxDeElegirCPU(estado, uid) })` (usar `elegirCPU(activoDe(yo), activoDe(rival))` → encontrar el índice del mov elegido; o agregar un helper en motor que devuelva la acción CPU) y `estado.timeouts[uid]++`. Si algún `timeouts[uid] >= 3` → fin por inactividad (`ganador` = rival), `finalizar`. Si no, resolver normal y emitir `resolucion`. Limpiar el timer al resolver/al elegir ambos.
- [ ] **Step 3: Reemplazo.** En fase `reemplazo`, el handler `elegir` acepta `{tipo:'reemplazo', idx}` de los uids en `reemplazan`; cuando se completan, vuelve a `combate` y arranca nuevo timer + `ronda`.
- [ ] **Step 4: Verificar build + jest**: `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest` → nest build OK, jest verde.
- [ ] **Step 5: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add api/src/batalla/salas.service.ts api/src/batalla/batalla.gateway.ts
git commit -m "pvp gateway: ronda simultánea con timer 30s, auto-move por timeout (elegirCPU) + forfeit a 3, eventos ronda/rivalListo/resolucion/reemplazo"
```

---

### Task 4: `batalla-online.js` — API cliente del nuevo protocolo

**Files:** Modify `web/src/lib/batalla-online.js`.

- [ ] **Step 1:** Reemplazar los emits de acción por uno unificado y agregar el reemplazo:
```js
export const elegir = (accion) => emit('elegir', accion);           // {tipo:'mover',i} | {tipo:'cambiar',idx} | {tipo:'pocion',itemId} | {tipo:'super',calidad} | {tipo:'rendirse'}
export const elegirReemplazo = (idx) => emit('elegir', { tipo: 'reemplazo', idx });
```
Mantener `rendirse` (= `elegir({tipo:'rendirse'})`). Quitar `mover/cambiar/usarPocion/lanzarSuper/resolverSuper` o reescribirlos como wrappers de `elegir`. `onBatalla` igual.
- [ ] **Step 2: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
git add web/src/lib/batalla-online.js
git commit -m "batalla-online: protocolo de acción unificado (elegir) + reemplazo"
```

---

### Task 5: `batalla.astro` — UX/UI de la ronda simultánea (online)

**REQUIRED SUB-SKILL:** `/frontend-design`. Tema-aware, FireRed/CRT.

**Files:** Modify `web/src/pages/batalla.astro`, `web/src/styles/global.css`.

- [ ] **Step 1:** Banner de estado (`#bt-estado-online`) + barra de timer. READ el modo En vivo (`renderOnline`, `finOnline`, el menú de acción, el panel de súper).
- [ ] **Step 2:** Cablear los eventos nuevos: `online.onBatalla('ronda', ({deadline}) => abrirSeleccion(deadline))`, `'rivalListo'`, `'resolucion', ({snap,eventos}) => animarRonda(snap, eventos)`, `'reemplazo', ({uids}) => pedirReemplazo(uids)`, `'fin'`. Reemplazar el viejo `'tuTurno'`/`'estado'`.
- [ ] **Step 3:** Selección: el menú (Luchar/Mochila/Cambiar/Súper) ahora **elige** vía `online.elegir({...})`. Al elegir, mostrar `✓ Elegiste: X · ⏳ Esperando al rival…` con botón **Cambiar** (habilitado hasta `rivalListo` o fin del timer); re-`elegir` reemplaza. Súper abre el reto inline; al resolver → `online.elegir({tipo:'super', calidad})`.
- [ ] **Step 4:** Timer: animar la barra hacia `deadline`. Reveal: al llegar `resolucion`, breve "¡Listos!" + (opcional) "▶ primero" según el primer evento `mover`; luego animar los eventos en orden (con `narrar()` de Task 6). Reemplazo: modal de banca para los `uids` propios; si es el otro, "Esperando que [rival] elija".
- [ ] **Step 5:** Estilos en `global.css` (banner, timer, chip de bloqueo, modal de reemplazo). Tema-aware.
- [ ] **Step 6: Build + screenshot** (Playwright, mock de eventos o seed): `cd web && npm run build` → OK.
- [ ] **Step 7: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/batalla.astro web/src/styles/global.css docs
git commit -m "batalla(online): UX de ronda simultánea (banner estado, timer, jugada bloqueada/cambiable, reveal, reemplazo)"
```

---

### Task 6: `batalla.astro` — typewriter `narrar()` + ritmo (práctica + online)

**REQUIRED SUB-SKILL:** `/frontend-design`.

**Files:** Modify `web/src/pages/batalla.astro`, `web/src/styles/global.css`.

- [ ] **Step 1: Helper `narrar(texto, {skip=true})`** que escribe en el cuadro FireRed letra por letra (~24ms/char), muestra un `▼` parpadeando al terminar, y permite **tap/click para saltear** (mostrar línea completa). Devuelve `Promise` que resuelve al terminar la línea + una pausa corta (~450ms). Respetar `prefers-reduced-motion` (texto directo, sin animación).
```js
let _narrarSkip = null;
function narrar(texto, opts = {}) {
  const box = $('bt-texto') /* el id real del cuadro FireRed */;
  return new Promise((resolve) => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) { box.textContent = texto; setTimeout(resolve, 350); return; }
    let i = 0; box.classList.add('escribiendo'); box.textContent = '';
    const tick = () => {
      if (i >= texto.length) { box.classList.remove('escribiendo'); box.classList.add('listo'); _narrarSkip = null; setTimeout(() => { box.classList.remove('listo'); resolve(); }, 450); return; }
      box.textContent += texto[i++]; _narrarSkip = saltar; setTimeout(tick, 24);
    };
    const saltar = () => { box.textContent = texto; i = texto.length; };  // el listener de tap llama _narrarSkip
    tick();
  });
}
// listener global: tap en el área de combate saltea la línea actual
document.addEventListener('pointerdown', () => { if (_narrarSkip) _narrarSkip(); });
```
(Ajustar `bt-texto` al id real del cuadro de texto; el `▼` se hace con CSS sobre `.listo`.)
- [ ] **Step 2: Reemplazar `msg(...)`** de la narración de combate por `await narrar(...)` en práctica y en `animarRonda` (online). Subir las pausas (`esperar`) para un ritmo deliberado. Mantener `msg` para mensajes de UI no-narrativos si los hay.
- [ ] **Step 3:** CSS del `▼` parpadeante (`.bt-texto.listo::after`) + clase `.escribiendo`. Tema-aware/FireRed.
- [ ] **Step 4: Build + screenshot**: `cd web && npm run build` → OK. Verificar (Playwright, práctica): el texto se escribe y el ▼ aparece.
- [ ] **Step 5: Commit**:
```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/batalla.astro web/src/styles/global.css docs
git commit -m "batalla: texto que se escribe letra por letra (FireRed) + ritmo más lento, en práctica y PvP"
```

---

### Task 7: Verificación final + (owner) deploy

**Files:** Verify only.

- [ ] **Step 1: Suite completa**: `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest` → nest build OK, jest verde. `cd web && npm run build` → OK.
- [ ] **Step 2: Smoke práctica** (dev, Playwright): un combate vs CPU corre, el texto se escribe, el ritmo se siente más lento, no hay errores JS en consola.
- [ ] **Step 3:** Documentar en `web/src/pages/ayuda.astro` el nuevo PvP (ambos eligen a la vez; el más rápido pega primero; súper = reto en paralelo; timer). Build + commit.
- [ ] **Step 4 (owner-gated, lo corre el controlador, NO un subagente): merge a main + deploy a la Pi.** El protocolo PvP cambió (motor + gateway + cliente) → front y motor se despliegan JUNTOS: push a main (GitHub Pages) + cross-build arm64 + `docker save|ssh load` + `compose up` (ver CLAUDE.md / [[deploy-pi-config]]). Después, e2e real de 2 sesiones.

```bash
cd /home/felipe/Documents/Repositories/luca-journey
cd web && npm run build && cd ..
git add web/src/pages/ayuda.astro docs
git commit -m "docs: ayuda al día con el PvP simultáneo"
```

---

## Notas para el ejecutor
- **Sync obligatorio** del core antes de jest/build de la API. `api/src/batalla/combate-core.ts` es GENERADO.
- **Reusar** la lógica de daño existente del `case 'mover'`/`'superResuelto'` (no reinventar): extraerla a `ejecutarAtaque`.
- **No revelar** la acción del rival en el snapshot (solo "ya eligió" sí/no) — anti-info-leak.
- **Práctica vs CPU** sigue resolviéndose local; adoptar `narrar()` + ritmo, y (opcional) reusar `ordenLanzadores` para el orden por velocidad si hoy no lo hace.
- **Deploy** = owner-gated, lo corre el controlador al final (front + Pi juntos por el cambio de protocolo).
- **Sin atribución Claude** en commits.
