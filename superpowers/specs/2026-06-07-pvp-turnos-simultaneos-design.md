# PvP turnos simultáneos (fiel) + UX/UI + typewriter — diseño

**Fecha:** 2026-06-07
**Estado:** diseño aprobado, pendiente plan + implementación (autónomo, subagent-driven).
**Tema:** rehacer el combate PvP de **ping-pong** (un jugador por turno) a **selección simultánea**
estilo Pokémon: ambos eligen, se resuelve por prioridad/velocidad. + UX/UI clara de los flujos +
texto "escribiéndose" (FireRed) + ritmo más lento. Relacionado: [[coleccion-v2-batalla]].

## Problema actual

`api/src/batalla/motor.ts`: `aplicarAccion(estado, uid, accion)` resuelve UNA acción y `pasarTurno`
(alterna). El más rápido solo decide quién **empieza**; después es ping-pong fijo (el que empezó pega
primero todas las rondas, aunque sea más lento). No hay selección simultánea ni re-evaluación de
velocidad. Se siente "raro". El texto (`msg()` en `batalla.astro`) aparece instantáneo y el ritmo es
muy rápido.

## Decisiones (brainstorming 2026-06-07)

- **A. Motor simultáneo:** ambos eligen en secreto; se resuelve por orden fiel cuando los dos bloquearon.
- **B. Súper en paralelo:** SÚPER es una acción; el reto de código aparece inline y se resuelve MIENTRAS
  el rival elige; su calidad escala el golpe; resuelve en el slot de velocidad.
- **C. Timeout:** ~30s; si no elegís, **auto-movimiento** (mejor daño, `elegirCPU`); **3 timeouts
  seguidos = derrota por inactividad**.
- **D. Prioridad de movimientos:** mapa curado (~15-20) en `combate-core`; orden = prioridad → velocidad → random.
- **E. UX/UI:** banner de estado (Elegí / Esperando / Resolviendo), timer visible, jugada bloqueada
  (cambiable hasta que el rival bloquee), reveal con "▶ primero", reemplazo claro tras debilitarse.
- **F. Typewriter + ritmo:** cuadro de texto escribe letra por letra (FireRed) con ▼, tap para saltear;
  ritmo más lento y deliberado; helper `narrar()` compartido por práctica y PvP.

## Arquitectura

Reglas puras en `web/src/lib/combate-core.ts` (fuente única; `api/scripts/sync-batalla-data.mjs` la copia
a `api/src/batalla/`). La **máquina de estado de la ronda** vive en `motor.ts` (server-autoritativo).
El cliente (`batalla.astro` + `batalla-online.js` + gateway `salas.service.ts`/`batalla.gateway.ts`)
maneja selección, timer y animación. Tests en `api/src/batalla/*.spec.ts` (jest).

## A. Motor simultáneo (`motor.ts`)

### Estado
`EstadoCombate` gana, por ronda:
```ts
acciones: Record<string, Accion | null>;   // accionDe[uid] = lo que eligió cada uno (null = aún no)
timeouts: Record<string, number>;           // timeouts seguidos por uid (forfeit a 3)
fase: 'seleccion' | 'combate' | 'super' | 'resolviendo' | 'reemplazo' | 'fin';
```
(El `turno` único deja de usarse para "de quién es"; ahora ambos eligen. Se conserva `turnoN` como nº de ronda.)
`Accion = { tipo:'mover'|'cambiar'|'pocion'|'super'; i?:number; idx?:number; itemId?:number|string; calidad?:number }`.

### Flujo
- **`elegirAccion(estado, uid, accion, rng) → { estado, eventos, listo }`** (reemplaza `aplicarAccion`):
  valida (fase `combate`, no debilitado, etc.), guarda `acciones[uid] = accion`, marca `listo` si ya
  está pero **permite re-elegir** mientras `acciones[rival] == null`. Si **ambos** tienen acción → llama
  `resolverRonda`.
- **`resolverRonda(estado, rng) → { estado, eventos }`**:
  1. **Cambios** (`tipo:'cambiar'`) de ambos, en cualquier orden.
  2. **Ítems** (`tipo:'pocion'`) de ambos.
  3. **Movimientos/Súper**: armar la lista de los activos que tienen acción de tipo `mover`/`super`,
     ordenar con `ordenAccion(a, b)`:
     - mayor **prioridad** primero (súper = prioridad 0; mover = `prioridadMov(mov)`).
     - empate → mayor **Velocidad** (`spe` efectiva, con paralisis ×0.5 si la aplicamos — opcional v1: usar spe directa).
     - empate → **random** (rng).
     Ejecutar cada uno (reusar la lógica de daño/estado/contacto/súper actual), chequeando debilitado
     entre golpes (si el defensor cayó, el atacante igual ya pegó; si el atacante cayó por DOT entre
     acciones, salta su acción).
  4. **DOT** (veneno/quemadura) de ambos al final de la ronda; chequeo de fin.
  5. **Reemplazo**: si algún activo quedó debilitado y el jugador tiene banca viva → `fase:'reemplazo'`
     (ese jugador debe `elegirAccion {tipo:'reemplazo', idx}`); si los dos cayeron, ambos eligen. Si no
     tiene banca → fin (gana el otro).
  6. Limpiar `acciones` para la próxima ronda; `turnoN++`.
- **Súper:** `elegirAccion` con `{tipo:'super', calidad}` se acepta solo si `yo.super >= SUPER_MAX`. El
  reto se resuelve **en el cliente** durante la selección; la `calidad` (0..1) viaja en la acción. En
  `resolverRonda`, el súper resuelve como un golpe grande (`danoSuper(atk, def, calidad)`) en su slot de
  velocidad (prioridad 0). Consume la barra (`yo.super = 0`).
- **Timeout (server, en `salas.service`):** un timer por ronda; al expirar, para cada uid sin acción se
  setea `elegirCPU(activo, rival)` como acción y `timeouts[uid]++`; si `timeouts[uid] >= 3` → fin (gana
  el rival, abandono por inactividad). Resetear `timeouts[uid]=0` cuando el uid sí elige a tiempo.

### Pureza/orden (en `combate-core.ts`, testeable)
```ts
// prioridad de un movimiento (mapa curado; default 0).
export const PRIORIDAD_MOV: Record<string, number>;     // por nombre normalizado
export function prioridadMov(mov: Mov): number;          // PRIORIDAD_MOV[mov.nombre] ?? 0
// orden de dos "lanzadores" {prioridad, spe, rng-tiebreak}. Devuelve <0 si A va primero.
export function ordenLanzadores(a: {prio:number, spe:number}, b: {prio:number, spe:number}, rng): number;
```

## D. Prioridad de movimientos (data)
`PRIORIDAD_MOV` (nombre ES → prioridad), curado:
`Ataque Rápido +1, Aqua Jet +1, Sombra Vil +1, Bote +1, Pies Rápidos? n/a, As Aéreo? +1,
Velocidad Extrema +2, Protección +4, Detección +4, Anticipo +1, Viento Hielo? n/a, Mismo Destino +0`…
(El plan fija la lista final cruzando con los nombres reales en `movimientos.json`; default 0 para el resto.)

## E. UX/UI (`batalla.astro` modo En vivo + `batalla-online.js` + gateway)
- **Banner de estado** (`#bt-estado-online`): `🟢 Elegí tu acción` / `⏳ Esperando al rival…` /
  `⚔️ Resolviendo…` / `🔄 Elegí tu próximo Pokémon`. Siempre visible arriba del menú.
- **Timer:** barra que se vacía (~30s); el server emite el deadline; el cliente la anima. Al expirar el
  server auto-elige.
- **Jugada bloqueada:** al elegir, el menú muestra `✓ Elegiste: [X]` + `⏳ Esperando al rival…`. Botón
  **"Cambiar"** habilitado **hasta que el rival bloquee** (el gateway avisa `rivalListo`) o se acabe el
  timer. (Re-`elegirAccion` reemplaza la acción guardada.)
- **Reveal:** al estar ambos listos, breve `¡Listos!` + indicador **"▶ primero"** sobre el que pega antes;
  luego la resolución animada (con narración typewriter).
- **Súper inline:** elegir SÚPER abre el panel del reto (el ya existente) sin frenar; al resolverlo se
  envía `{tipo:'super', calidad}`; chip "resolviendo tu súper".
- **Reemplazo:** `fase:'reemplazo'` → modal "Tu X cayó, elegí el próximo" (banca); el otro ve
  "Esperando que [rival] elija". Si ambos caen, los dos eligen a la vez.
- **Menú de acción unificado** (Luchar / Mochila / Cambiar / Súper) como una ronda; deshabilitar lo que
  no aplique (Súper si la barra no está llena, etc.).
- **Eventos del gateway** (nuevos/ajustados): `ronda` (estado a elegir + deadline), `rivalListo`,
  `resolucion` (snapshot + eventos de la ronda para animar), `reemplazo`, `fin`. (Reemplazan/extienden
  `tuTurno`/`estado`.)

## F. Typewriter + ritmo (práctica + PvP, `batalla.astro`)
- **`narrar(texto, opts)`** (helper compartido): escribe el texto en el cuadro FireRed **letra por letra**
  (~24ms/char, configurable), muestra un **▼** parpadeando al terminar; un **tap/click** saltea a la línea
  completa. Devuelve una Promise que resuelve cuando la línea terminó (typewriter completo + pausa corta).
- Reemplaza los `msg(...)` instantáneos de la narración de combate (práctica y online) por
  `await narrar(...)`. Las pausas (`esperar(...)`) entre eventos suben para un ritmo **deliberado**
  (p.ej. golpe → narrar daño → pausa → efecto). En PvP auto-avanza (sincronía); el tap solo saltea el
  typewriter de la línea actual.
- Respetar `prefers-reduced-motion` (sin typewriter → texto directo).

## Testing
- **`api/src/batalla/combate-core.spec.ts`:** `prioridadMov` (mapa + default 0), `ordenLanzadores`
  (prioridad > velocidad > tiebreak determinista con rng fijo).
- **`api/src/batalla/motor.spec.ts`:** reescribir/extender para el modelo simultáneo:
  - `elegirAccion` guarda y no resuelve hasta que ambos eligen; permite re-elegir si el rival no eligió.
  - `resolverRonda`: orden cambios→ítems→moves; el más rápido pega primero; prioridad pega antes que
    velocidad; ambos mueven en una ronda; DOT al final; debilitado dispara `reemplazo`; sin banca → fin.
  - súper: `{tipo:'super',calidad}` resuelve como golpe grande en su slot, consume barra.
  - timeout/forfeit: 3 sin acción → fin (se testea la función pura de conteo; el timer en sí es del gateway).
- `cd api && node scripts/sync-batalla-data.mjs && npm run build && npx jest` verde.
- `cd web && npm run build` verde. Verificación visual (`/frontend-design`): banner/timer/bloqueo/typewriter
  en práctica y (mock) online — tema oscuro y claro.
- E2E real de 2 sesiones = owner-gated (tras el deploy).

## Compat / migración
- Sin migración de data. El cambio es de protocolo de combate (gateway + cliente + motor) — se despliega
  junto (front a Pages, motor a la Pi). Mientras no se deploye la Pi, el PvP online sigue con el motor
  viejo; el front nuevo debe tolerar ambos o desplegarse junto (el plan lo coordina: front + deploy juntos).
- Práctica (vs CPU) NO usa el gateway; su flujo se adapta para usar `narrar()` + ritmo, pero su turno
  sigue resolviéndose localmente. (La selección simultánea aplica al PvP; en práctica el rival es la IA y
  resuelve en la misma ronda — se puede unificar la resolución reusando `resolverRonda`/`ordenLanzadores`.)

## Fuera de alcance
- Climas/terrenos, dobles, megaevolución. Priority de Protección con su mecánica completa (acá solo el
  bracket de prioridad; "fallar si se repite" = futuro). Re-pick infinito (se permite re-elegir solo
  hasta que el rival bloquea/timer).

## Archivos afectados (estimado)
- `web/src/lib/combate-core.ts` (PRIORIDAD_MOV, prioridadMov, ordenLanzadores) + sync + spec.
- `api/src/batalla/motor.ts` (estado simultáneo, elegirAccion, resolverRonda, reemplazo) + `motor.spec.ts`.
- `api/src/batalla/salas.service.ts` + `batalla.gateway.ts` (timer de ronda, eventos ronda/rivalListo/
  resolucion/reemplazo/fin, auto-move, forfeit).
- `web/src/lib/batalla-online.js` (emits/on nuevos).
- `web/src/pages/batalla.astro` (banner/timer/bloqueo/reveal/reemplazo online; `narrar()` typewriter +
  ritmo en práctica y online) + `web/src/styles/global.css`.
- `docs/` rebuild. Deploy a la Pi (owner-gated; lo corro al final).
