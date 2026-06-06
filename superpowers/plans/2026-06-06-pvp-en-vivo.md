# Batalla PvP en vivo — Plan de implementación

> **For agentic workers:** REQUIRED SUB-SKILL: superpowers:subagent-driven-development o executing-plans.
> **OWNER-GATED:** no va live sin redeploy del server NestJS a la Pi + test de 2 sesiones con login
> Google real (el gateway valida JWT). El motor (Task 1) SÍ se testea solo (jest). El resto se
> construye y compila, pero el e2e real lo corre el owner tras el redeploy.

**Goal:** Duelos 2 jugadores en vivo por turnos, server-autoritativo, reusando el motor de la práctica.

> **ESTADO (2026-06-06):** Tasks 1–5 DEPLOYADAS. Tasks 1–4 commiteadas+pusheadas a main; Task 5 deploy
> hecho: imagen arm64 a la Pi + `compose up` (Nest started, `/auth/me`→401, gateway `/batalla` live por
> `wss://poke.servegame.com`), front en GitHub Pages. **Único pendiente: el e2e MANUAL de 2 sesiones**
> con login Google real (2 cuentas) — no autónomo.

**Architecture:** NestJS gateway socket.io (`/batalla` o el `EventsGateway` existente extendido) con
estado autoritativo por sala; motor de combate portado a TS; matchmaking (cola + código + invitar
amigo). Cliente: lobby + sala de selección + combate sincronizado (reusa arena/animaciones/cries).

**Tech Stack:** NestJS 10 + socket.io + JWT (mismo patrón que `realtime/events.gateway.ts`). Front: Astro + socket.io-client (`realtime.js`).

**Spec:** `superpowers/specs/2026-06-06-pvp-en-vivo-design.md`

---

## Task 1: Motor de combate en TS + tests (server, VERIFICABLE)

**Files:** Create `api/src/batalla/motor.ts` · `api/src/batalla/motor.spec.ts`

Portar la lógica de `web/src/lib/batalla.js` + `tipos.js` a TS puro (sin DOM): `combatiente`,
`calcularDano` (tipo/STAB/atkMod/defMod), `esEstado`/`aplicarEstado`, `danoSuper`, `elegirCPU` (no
hace falta en PvP pero útil), y la **máquina de estado de la sala**: `crearCombate(jugadores)`,
`aplicarAccion(estado, uid, accion)` → nuevo estado + eventos, `chequearFin(estado)`. Tipos: copiar
`tipos.json`/`movimientos.json`/`learnsets.json`/`pokemon.json` (o leerlos del front via build step).

- [ ] **Step 1:** Escribir `motor.ts` (port de batalla.js a TS + la máquina de estado de sala:
  turnos, acciones `mover`/`cambiar`/`pocion`/`super`/`rendirse`, validación de que la acción viene
  del jugador cuyo turno es, daño server-side, fin).
- [ ] **Step 2:** Escribir `motor.spec.ts` con casos: daño con tipo super-eficaz; estado baja stat;
  turno alterna; cambio cuesta turno; súper aplica daño grande; fin cuando un equipo llega a 0;
  rendirse → gana el otro; acción fuera de turno se rechaza.
- [ ] **Step 3:** `cd api && npm test -- motor` → todo verde.
- [ ] **Step 4: Commit** `pvp: motor de combate en TS + máquina de estado de sala (tests jest)`

## Task 2: Gateway + salas + matchmaking (server)

**Files:** Create `api/src/batalla/batalla.gateway.ts` · `batalla.module.ts` · `salas.service.ts` · Modify `api/src/app.module.ts`

Mirror de `events.gateway.ts` (auth JWT en handshake). `salas.service.ts` mantiene las salas en
memoria: `Map<roomId, EstadoCombate>` + la **cola** (uids esperando) + **códigos** (code→roomId).

- [ ] Eventos cliente→server: `buscar` (entra a la cola; si hay otro, empareja), `invitar(uid)`
  (emite invitación a `progreso:<uid>`), `aceptar(roomId)`, `crearCodigo`→code, `unirseCodigo(code)`,
  `elegirEquipo(payload)`, `mover/cambiar/pocion/super`, `superResuelto(calidad)`, `rendirse`.
- [ ] Eventos server→cliente: `emparejado`, `seleccion`, `estado`, `tuTurno`, `retoSuper`,
  `fin(ganador, premios)`, `rivalDesconectado(graciaSeg)`, `rivalVolvio`, `error`.
- [ ] **Anti-trampa:** al `elegirEquipo`, validar contra la DB (`progreso` del uid) que tiene esas
  instancias y niveles. El daño lo calcula el server (Task 1), nunca el cliente.
- [ ] **Reconexión:** en `handleDisconnect`, si el uid está en una sala activa → arrancar timer de
  30s + emitir `rivalDesconectado`; si reconecta (nuevo socket, mismo uid) → re-join + `rivalVolvio`;
  si expira → `fin` (gana el que queda) + premios + persistir.
- [ ] **Commit** `pvp: gateway socket.io + salas + matchmaking (cola/codigo/invitar) + reconexion`

## Task 3: Premios + insignias (server)

**Files:** Modify `api/src/batalla/salas.service.ts` · Create `api/src/batalla/insignias.ts`

- [ ] Al `fin`: ganador += caramelos (de los que pelearon) en su `progreso`; perdedor += Pokébolas;
  ambos: chequear/otorgar **insignias** (`primer-duelo`, `primera-victoria`, `racha-3`, `racha-10`,
  `10-victorias`, `mata-legendario`, `remontada`) y persistir. Penalización leve por abandono repetido
  (contador `pvp:abandonos`).
- [ ] **Commit** `pvp: premios (caramelos/pokebolas) + insignias + persistencia`

## Task 4: Cliente — lobby + selección + combate sincronizado (web)

**Files:** Create `web/src/lib/batalla-online.js` · Modify `web/src/pages/batalla.astro`

- [ ] `batalla-online.js`: conectar al gateway (reusa `realtime.js`), API: `buscar()`, `invitar(uid)`,
  `unirseCodigo(code)`, `elegirEquipo(iids)`, `mover(i)`, `cambiar(i)`, `usarPocion(id)`,
  `resolverSuper(calidad)`, `rendirse()`, y callbacks de los eventos server→cliente.
- [ ] `batalla.astro`: agregar **modo Online** (botón en la selección de modo: Práctica | En vivo).
  El lobby (cola / invitar amigo de la lista / código). La **sala de selección** de equipo (3) en vivo.
  El **combate** usa la MISMA UI (arena, animaciones, cries, textbox), pero el estado lo manda el
  server (no se calcula local); las acciones se mandan por socket. El **súper por código en pausa**:
  cuando el server manda `retoSuper`, abrís TU reto (de tus temas vistos); el rival ve "el rival está
  resolviendo…"; mandás `superResuelto(calidad)`.
- [ ] **Commit** `pvp: cliente — lobby, seleccion de equipo en vivo, combate sincronizado, super en pausa`

## Task 5: Deploy + e2e (OWNER)

- [x] Cross-build arm64 + `docker save|ssh load` a la Pi + `docker compose up -d` (2026-06-06).
  Verificado: Nest started, `poke.servegame.com/auth/me`→401, gateway `/batalla` montado (handshake wss OK).
- [x] Front pusheado a `main` → GitHub Pages live (tienda piedras tipadas + modo En vivo).
- [ ] **Test de 2 sesiones** (2 navegadores/cuentas Google) — MANUAL, pendiente: cola, invitar, código,
  combate completo, súper, cambio, poción, abandono+reconexión, premios+insignias.

---

## Notas

- Reusar el `EventsGateway` existente extendiéndolo (agregar los `@SubscribeMessage` de batalla) es
  válido y más simple que un namespace aparte; decidir en Task 2 según acoplamiento.
- El motor (Task 1) duplica `batalla.js` en TS: a futuro se puede compartir un paquete, pero por
  ahora duplicar es aceptable (el server NO puede confiar en el cliente).
- Datos: el server necesita `tipos.json`/`movimientos.json`/`learnsets.json`/`pokemon.json`. Copiarlos
  a `api/src/batalla/data/` en el build, o leerlos de `web/src/data/` con un path relativo.
