# Retención/Onboarding (A) + Intercambio por instancia (C) + Cura/Revivir PvP (B1) — Diseño

> Aprobado (brainstorm 2026-06-06). A es frontend puro (sale ya). C y B1 son **owner-gated**
> (redeploy NestJS a la Pi + test de 2 sesiones); se bundlean en un solo redeploy.

## A — Retención + Onboarding (frontend, verificable ya)

### A1 · Racha diaria
- Estado nuevo `col:racha = { dias: number, ultima: 'YYYY-MM-DD' }` en el blob de progreso (sincroniza solo).
- Al cargar (una vez por día): si `ultima` == hoy → nada; si == ayer → `dias++`; si más viejo → `dias = 1`.
  Bonus de Pokébolas al reclamar el día: `+5 × min(dias, 5)` (tope 25). Se guarda que ya se reclamó hoy.
- Indicador 🔥 con los días en el home (y/o header). Helper en `coleccion.js`: `rachaHoy()` → `{dias, bonus, nuevo}`.

### A2 · Tutorial guiado (coachmarks)
- Overlay de primer uso que recorre las features clave (Libro → Ejercicios → Safari → Pokédex → Batalla)
  con un tooltip por paso (resalta el nav-link correspondiente). Flag `tuto:visto` en localStorage; saltable;
  relanzable desde `ayuda.astro` ("Ver tutorial de nuevo"). Componente en el layout `Base.astro` (está en todas
  las páginas) + `src/lib/tutorial.js`. Tema-aware, cohesivo con la estética CRT.

### A3 · Logros ampliados
- `logros.js` (sistema existente, `evaluar(temas)`): sumar `racha-7` (7 días), `primera-evolucion`,
  `primer-shiny`, `primer-duelo` (reusa `col:pvp`/`col:insignias`/`col:racha`/`col:pc`). Sin tocar la estructura.

## C — Intercambio por instancia única (server + cliente, owner-gated)

**Problema actual:** el trade intercambia **cantidades** (`col:atrapados`/`col:shiny`) vía `swapColeccion`, NO
toca `col:pc` (las instancias). El cliente luego corre `reconciliarPC`, que **recrea instancias a nivel 1** según
el conteo → tradear un Charizard Nv50 shiny entrega un Nv1 y se pierde la instancia real. Hay que tradear la
**instancia exacta**.

### Server (`api/src/coleccion/coleccion.ts` + `social/ofertas.service.ts`)
- Nuevo `swapInstancias(estadoA, iidsA, estadoB, iidsB)`:
  - lee `col:pc` (array de instancias) de cada blob.
  - valida que cada `iid` de A esté en el PC de A (y de B), y que A≠B no compartan target.
  - **mueve el objeto instancia** (id, nivel, exp, shiny, movs, mote, creado) del PC del dueño al del receptor;
    reasigna `iid` nuevo al recibir (evita colisiones).
  - recomputa los derivados del receptor desde el nuevo `col:pc`: `col:atrapados` (conteo por id),
    `col:shiny` (ids con alguna instancia shiny), `col:vistos` (agrega las especies recibidas).
  - puro; devuelve `{estadoA, estadoB}`. Reemplaza a `swapColeccion` en `ofertas.responder`.
- `Oferta.doy`/`pido` (JSON) pasan a `{ iid, id, nivel, shiny, mote }[]` (iid = qué instancia; el resto = snapshot
  para mostrar/validar). `crear` valida que el oferente sea dueño de los `iid` de `doy`.

### Cliente (`web/src/lib/social.js`, `trades.js`, `intercambio.astro`, `amigos.astro`, `coleccion.js`)
- `snapshotPublico` del perfil expone las **instancias** del PC: `pcPub = [{iid,id,nivel,shiny,mote}]` (además de lo
  actual). Así el que oferta puede **elegir la instancia específica del amigo** que pide.
- UI de oferta: elegís **qué instancia das** (de tu PC, con nivel/shiny/mote) y **cuál pedís** (del PC público del
  amigo). `crearOferta(aUserId, doy, pido)` manda los arrays de instancias.
- Al aceptar: el server swapea y emite `progreso`; el cliente aplica el blob (col:pc ya correcto). Se **elimina el
  uso de `reconciliarPC` para trades** (ya no hay reconciliación por cantidad).

## B1 — Cura de estado / Revivir en PvP (server, owner-gated)

- `motor.ts`: la acción `pocion` se generaliza a **item** (`{itemId}`): pociones HP (ya está), curas de estado
  (`curaEstado`: limpia `estado`/`estadoT` del activo si corresponde) y `revivir` (revive un debilitado del equipo
  al 50% HP). Validación server-side de aplicabilidad (igual que la práctica). Cuesta el turno.
- `salas.service`/`batalla.gateway`: el evento `pocion(itemId)` ya existe; pasa el `itemId` tal cual.
- Cliente `batalla.astro` `abrirMochilaOnline`: ofrecer también cat `estado` + Revivir (consume inventario local +
  emite `pocion(itemId)`), igual que la práctica.
- Tests en `motor.spec.ts`: curar estado en PvP, revivir un caído.

> **Nota anti-trampa (B1/C):** el server valida contra la DB (propiedad de instancias en C; el HP/estado lo
> calcula el motor en B1). El consumo de inventario de items en PvP queda del lado cliente por ahora (v1,
> owner-gated); endurecerlo es follow-up.

## Orden
1. **A** (A1→A2→A3) → build + screenshots + push (frontend).
2. **C** (server swapInstancias + ofertas; cliente snapshot+picker) + **B1** (motor item + online mochila) → nest
   build + jest + cross-build arm64 + transferir Pi + `compose up` + push docs.
3. **e2e 2 sesiones** (owner): intercambio por instancia + curas/revivir en PvP.

## No-objetivos (YAGNI)
- Ranking/ELO PvP (B2, diferido). Trade en vivo (sigue async). Multi-instancia masiva por oferta (igual permite
  varias, pero el foco es 1×1). Endurecer inventario de items PvP server-side (follow-up).
