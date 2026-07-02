# Postgres compartido en la Pi — diseño

**Fecha:** 2026-07-01 · **Estado:** implementado y verificado en producción (Pi).

## Objetivo

Sacar Postgres de adentro del compose de luca-journey y convertirlo en una **instancia
compartida standalone** en la Raspberry Pi, reutilizable por varios proyectos, sin exponer
puertos a la LAN.

## Motivación

- Con ~900 MB de RAM en la Pi, un contenedor Postgres por proyecto no escala → **una sola
  instancia compartida**, con **base + rol por proyecto** (aislamiento real).
- El `db` embebido publicaba `0.0.0.0:5433` → superficie de ataque innecesaria en la LAN.

## Arquitectura

- **`shared-postgres/`**: compose propio (`postgres:17`, lifecycle independiente).
- **Red Docker `shared-db`** (`external: true`): única vía de acceso. Postgres tiene alias
  `postgres` → los proyectos conectan a `postgres:5432`.
- **Volumen reusado** `luca-journey_dbdata` (`external`): cero movimiento de datos; el cluster
  ya tenía el rol/DB superusuario `luca`.
- **Sin `ports:` en la Pi**: Postgres solo alcanzable desde contenedores en `shared-db`. En dev,
  `docker-compose.dev.yml` (opt-in) publica `5433:5432`.

## Cambios en luca-journey

- Se elimina el servicio `db` y la declaración del volumen del `docker-compose.yml`.
- La `api` se une a `shared-db` (external) y su `DATABASE_URL` pasa a `@postgres:5432`
  (mismo user/pass/base `luca`). Sin cambios de código ni de imagen.

## Trade-off aceptado

luca-journey deja de ser self-contained: depende de que `shared-postgres` esté arriba primero.
Es el costo correcto de compartir la instancia.

## Onboarding de un proyecto futuro

```sql
CREATE ROLE x LOGIN PASSWORD '…';
CREATE DATABASE x OWNER x;   -- x NO-superusuario, solo ve su base
```
El proyecto se une a `shared-db` y usa `postgres://x:…@postgres:5432/x`. Detalle en
`shared-postgres/README.md`.

## Migración ejecutada (Pi, 2026-07-01)

1. `pg_dump` de respaldo (597 KB).
2. `docker network create shared-db`.
3. `docker compose down` de luca-journey **sin `-v`** (volumen preservado).
4. Levantar `shared-postgres` (adopta el volumen external).
5. Nuevo compose de luca-journey + `docker compose up -d`.

## Verificación

- Row counts pre/post idénticos: users=21, progreso=20, perfiles=19, intercambios=9, desafios=1.
- `prisma migrate deploy` conectó a `postgres:5432` ("No pending migrations to apply").
- API arrancó OK; `/auth/me` → 401.
- Puerto 5433 cerrado al host (solo 443 escucha).

## Rollback

La data nunca se movió → revertir el compose de luca-journey al servicio `db` apuntando al
mismo volumen `luca-journey_dbdata` y `docker compose up -d`.
