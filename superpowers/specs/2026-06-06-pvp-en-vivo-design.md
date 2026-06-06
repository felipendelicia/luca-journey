# Diseño — Batalla PvP en vivo

Fecha: 2026-06-06
Estado: alcance definido con el owner; pendiente review. **Owner-gated para ir live** (necesita
redeploy del server NestJS a la Pi + test de 2 sesiones con login real).

> Sub-proyecto 2 de 2 (el otro: `2026-06-06-tienda-items-design.md`). Se construye DESPUÉS de la Tienda.
> Reusa el motor `batalla.js` (puro, ya hecho y testeado) y el patrón del gateway de **intercambios**
> (socket.io + auth JWT + salas), que ya está deployado y funcionando con login real.

## Objetivo

Duelos **2 jugadores reales en vivo**, por turnos, con el mismo motor que la práctica vs CPU
(tipos, niveles, 4 ataques, súper por código). El **servidor es la fuente de verdad** del estado
(HP, turnos, equipos) para evitar trampas.

## Decisiones (del owner)

- **Matchmaking: los tres** — invitar a un **amigo** (de la lista), **código de sala** (privado), y
  **cola pública** (el server empareja con cualquiera online).
- **Alcance: completo** — 3v3, tipos, cambios, súper por código, recompensas.
- **Súper por código = PAUSA:** cuando un jugador llena la barra y desata el súper, se abre **su**
  reto (de un tema que YA vio) y **el rival espera** con un timeout. Por turnos, ordenado.
- **Recompensas:** ganador → **caramelos** de los Pokémon que pelearon; perdedor → algunas
  **Pokébolas**; **+ insignias/logros** por hitos. (Sin ELO/ladder ni moneda nueva por ahora.)
- **Abandono/desconexión:** ventana de **reconexión ~30s**; si no vuelve, **gana el que queda** y
  cobra recompensa; **penalización leve** por abandonar seguido.
- **Timeout de turno:** ya existe en práctica (30s → movimiento auto); en PvP el server lo arbitra.

## Arquitectura

```
Cliente A ─┐                        ┌─ NestJS BatallaGateway (socket.io, namespace /batalla)
           ├─ WebSocket (JWT) ──────┤   - salas (roomId), matchmaking (cola + código + invitación)
Cliente B ─┘                        │   - estado AUTORITATIVO del combate por sala
                                    │   - valida cada acción, avanza turnos, calcula daño (server)
                                    └─ emite 'estado' a ambos tras cada acción
```

- **Server (NestJS, `api/src/batalla/`):** nuevo módulo + gateway, **mirror** de `intercambios`
  (auth JWT en el handshake, salas por `roomId`, presencia). El **motor de combate** (tipos, daño,
  stats, estado) se porta a TypeScript en el server (o se comparte la lógica) — el server es quien
  resuelve, no el cliente. Estado por sala: `{ jugadores:[{uid, equipo, activo, ...}], turno, fase }`.
  - Eventos cliente→server: `buscar` (cola), `invitar(uid)`, `unirseCodigo(code)`, `elegirEquipo(iids+nivel/movs)`,
    `mover(movIdx)`, `cambiar(idx)`, `superResuelto(calidad)`, `rendirse`.
  - Eventos server→cliente: `emparejado(rival)`, `seleccion`, `estado(snapshot)`, `tuTurno`, `retoSuper`,
    `fin(ganador, premios)`, `rivalDesconectado(graciaSeg)`, `error`.
- **Cliente (`web/`):** `src/lib/batalla-online.js` (socket.io del namespace /batalla) + reusa la UI
  de `batalla.astro` (misma arena/animaciones/cries), pero el estado lo manda el server (no se calcula
  local). Una pantalla de **lobby** (buscar / invitar amigo / pegar código) y **sala de selección de equipo**.
- **El equipo viaja con datos mínimos** (id, nivel, shiny, movs) — el server reconstruye el combatiente
  y valida que el jugador realmente tiene esas instancias (anti-trampa, contra su progreso en DB).

## Flujo

1. **Lobby:** elegís *Cola pública* (entrás a la cola) / *Invitar amigo* (de tu lista, le llega la
   invitación por realtime) / *Código* (creás o pegás un código de sala).
2. **Emparejado:** ambos entran a la **sala de selección de equipo** (3 Pokémon, en tiempo real;
   ves cuando el rival está listo). Timeout de selección.
3. **Combate:** por turnos. Cada acción va al server, que valida + resuelve + emite el nuevo estado a
   ambos. Animaciones/cries en cliente al recibir el estado.
4. **Súper (código):** al desatarlo, el server abre **tu** reto (filtrado a tus temas vistos) y pausa
   al rival (con timeout). Acertar rápido = golpe grande; el server aplica el daño.
5. **Fin:** server declara ganador, reparte premios (caramelos/pokébolas), otorga insignias, persiste.

## Insignias (set inicial, default)

`primer-duelo` (jugar 1 PvP), `primera-victoria`, `racha-3`, `racha-10`, `10-victorias`,
`mata-legendario` (vencer a un legendario rival), `remontada` (ganar con 1 Pokémon vivo).

## Manejo de casos borde

- **Desconexión:** el server detecta el `disconnect`; arranca gracia de 30s; emite `rivalDesconectado`.
  Si vuelve (mismo uid, reune al socket a la sala) → sigue. Si no → `fin(ganador=el que queda)`.
- **Abandono (rendirse / cerrar):** cuenta como derrota; **penalización leve** (ej. cooldown de cola
  o un contador de abandonos visible) si es repetido.
- **Timeout de turno / de reto:** el server fuerza un movimiento auto / súper fallido.
- **Anti-trampa:** el server NO confía en el cliente para el estado; valida la propiedad de las
  instancias contra la DB y recalcula el daño.

## Owner-gated (lo que necesita TU mano)

- **Redeploy del server** a la Pi (cross-build arm64 + transferir imagen + `docker compose up`).
- **Test de 2 sesiones** con login Google real (el gateway valida JWT; no se puede testear full e2e
  en autónomo sin auth real). Lo que SÍ se testea solo: unit del motor/estado en TS, y la UI/lobby
  con mocks.

## Componentes / archivos

| Archivo | Responsabilidad |
|---|---|
| `api/src/batalla/batalla.module.ts` · `.gateway.ts` · `motor.ts` · `salas.service.ts` | gateway socket.io + estado autoritativo + motor TS + matchmaking. |
| `api/src/batalla/motor.spec.ts` | unit del motor + máquina de estado (daño, turnos, fin, súper, abandono). |
| `web/src/lib/batalla-online.js` | cliente socket.io /batalla + API para la UI. |
| `web/src/pages/batalla.astro` | agrega modo **online** (lobby + sala + combate sincronizado) además de la práctica. |
| `web/src/lib/realtime.js` | reusar/extender para el namespace /batalla. |

## Decomposición sugerida (orden de build)

1. **Motor en TS + unit tests** (server) — la lógica autoritativa, sin red.
2. **Gateway + salas + matchmaking** (server) — mirror de intercambios, con auth.
3. **Cliente lobby + selección de equipo** (web).
4. **Combate sincronizado** (web) — recibe estado, manda acciones, anima.
5. **Súper por código en PvP** (pausa + timeout, server-arbitrado).
6. **Abandono/reconexión + insignias + recompensas.**

## Testing

- **Unit (jest, server):** `motor.spec` (daño con tipos/stats, turnos, súper, fin, timeout, abandono).
- **Integración local:** correr `docker compose up` local + 2 clientes con JWT de test (si se puede
  inyectar un secret de test) o un mock del guard, para validar el flujo de salas.
- **e2e real:** owner, 2 sesiones, post-redeploy.

## Fuera de alcance (v2+)

- ELO/ladder + temporadas. Torneos. Espectadores. Chat en duelo. Reincorporación a media cola.
