# Exponer el Postgres compartido a internet + monolito "La teca de los pibes"

**Fecha:** 2026-07-01 · **Estado:** implementado y verificado.

## Objetivo

Que una app en **Vercel** ("La teca de los pibes", repo aparte) use el **Postgres
compartido** de la Pi. Como la instancia estaba aislada (solo red Docker interna), hubo que
**exponerla a internet de forma segura**, y crear el monolito Next.js cableado a ella.

## Contexto / conflicto resuelto

Vercel es cloud + serverless; el Postgres vivía en una red Docker interna de la Pi (hogar,
IP dinámica, solo 80/443 forwardeados). No había camino. Se evaluaron 4 opciones (cloud
Postgres, API-proxy, exponer directo, correr en la Pi). El dueño eligió **exponer Postgres
directo** con `poke.servegame.com`.

## Parte A — Exposición segura (Pi)

- **Rol + base dedicados** `teca` (NO-superusuario, dueño de su base). `REVOKE CONNECT ... FROM
  PUBLIC` en `teca` y `luca` → aislamiento por base. `teca` tiene `CREATEDB` (para la shadow DB
  de `prisma migrate dev`).
- **TLS obligatorio**: `pg_hba.conf` solo acepta `hostssl` + `scram-sha-256` en TCP; socket
  local en `trust` (mantenimiento). Cert = el de Let's Encrypt de `poke.servegame.com`,
  copiado a un dir con owner uid 999 por `refresh-pg-certs.sh`.
- **`luca` endurecido**: al exponer la instancia, su password trivial era inaceptable → password
  random fuerte, movido a `DATABASE_URL` en el `.env` de la Pi (sale del compose commiteado),
  con `?sslmode=require`. Api de luca-journey redeployada.
- **Puerto 5432 publicado** al host vía `docker-compose.expose.yml` (Pi-only). Base y dev quedan
  sin exponer nada.
- **Renovación**: hook `/etc/letsencrypt/renewal-hooks/deploy/restart-postgres.sh` recopia el
  cert y reinicia el contenedor.

**Postura de seguridad (honesta):** el 5432 queda abierto al mundo aceptando auth. Defensa =
TLS + passwords fuertes scram + aislamiento por base. No se filtra por IP (el proxy de Docker
enmascara el origen; Vercel rota IPs). Endurecimiento futuro opcional: `userland-proxy=false`
+ IP-allowlist.

## Parte B — El monolito (repo `la-teca-de-los-pibes`)

- Next.js 16 (App Router, TS, Tailwind) + Prisma 7 con adapter `@prisma/adapter-pg`.
- Modelo `Nota` de ejemplo; migración `init` aplicada en la base `teca` **sobre la LAN**.
- Página que lista/crea notas (server action) → prueba el round-trip.
- `DATABASE_URL` por entorno. **Detalle clave de TLS**: `pg` v8.21 trata `sslmode=require`
  como `verify-full`. Por eso:
  - LAN (por IP, no matchea el cert): `?sslmode=require&uselibpqcompat=true` (cifra sin verificar).
  - Vercel (por `poke.servegame.com`): `?sslmode=verify-full` (verificación completa).
- `postinstall: prisma generate` para el build de Vercel.

## Lo que hace el dueño (fuera de código)

- **Modem**: forward `5432` externo → `192.168.1.112:5432` (necesario solo para que Vercel llegue;
  migración y test local se hicieron por LAN).
- **Vercel**: importar el repo + setear `DATABASE_URL` con hostname público y `verify-full`.

## Verificación

- Sin SSL → rechazado; password viejo de `luca` → falla; `teca` no puede entrar a la base `luca`
  (aislamiento); `teca` conecta por SSL a su base (no-superuser).
- luca-journey api reconecta con `sslmode=require`, `/auth/me` 401.
- `prisma migrate dev` creó la tabla en la Pi sobre la LAN.
- `next build` OK; `next start` + curl → HTTP 200 y la página renderiza una nota leída de la Pi
  (round-trip runtime por el mismo camino que Vercel).
