# shared-postgres — Postgres compartido de la Pi

Instancia **Postgres 17 única** que sirve a varios proyectos en la Raspberry Pi
(luca-journey y futuros). Reemplaza al `db` que antes vivía dentro del compose de
luca-journey.

## Por qué

Con ~900 MB de RAM en la Pi no conviene un contenedor Postgres por proyecto. En su
lugar corre **una instancia compartida**, con **una base + un rol por proyecto**
(aislamiento real: cada rol solo ve su base).

## Topología

- Los proyectos NO ven a Postgres por puerto de host. Se conectan por la red Docker
  **`shared-db`** (`external: true`), usando el hostname interno **`postgres:5432`**.
- No hay `ports:` publicados en la Pi → cero superficie de ataque en la LAN.
- La data vive en el volumen histórico **`luca-journey_dbdata`** (referenciado como
  `external`), donde el cluster ya tiene el rol/DB superusuario `luca`.

## Correr

### En la Pi (producción, EXPUESTO a internet con TLS)

La Pi corre con el override `docker-compose.expose.yml`, que publica el `5432`, fuerza SSL
y usa el `pg_hba` endurecido. Requiere el cert copiado en `./certs/` (lo deja
`refresh-pg-certs.sh`).

```bash
docker network create shared-db                       # una sola vez
sudo ~/shared-postgres/refresh-pg-certs.sh            # copia el cert LE con perms de postgres (uid 999)
cd ~/shared-postgres && docker compose -f docker-compose.yml -f docker-compose.expose.yml up -d
```

Ver **Exposición a internet** más abajo.

### En dev (local), exponiendo 5433 al host

```bash
docker network create shared-db          # una sola vez
docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
```

Luego cada proyecto (p.ej. `luca-journey`) se levanta aparte y se une a `shared-db`.

## Agregar un proyecto nuevo

1. Crear rol + base aislados (NO superusuario):

   ```sql
   -- conectado como superusuario luca:
   CREATE ROLE miproyecto LOGIN PASSWORD 'una-clave';
   CREATE DATABASE miproyecto OWNER miproyecto;
   ```

   ```bash
   docker exec -i shared-postgres-postgres-1 \
     psql -U luca -d luca -c "CREATE ROLE miproyecto LOGIN PASSWORD 'una-clave';" \
                          -c "CREATE DATABASE miproyecto OWNER miproyecto;"
   ```

2. En el `docker-compose.yml` del proyecto, unir su servicio a la red `shared-db`:

   ```yaml
   services:
     api:
       networks: [shared-db]
   networks:
     shared-db:
       external: true
   ```

3. Usar `DATABASE_URL=postgres://miproyecto:una-clave@postgres:5432/miproyecto`.

El rol `miproyecto` es NO-superusuario y dueño solo de su base → no ve las bases de
otros proyectos.

## Exposición a internet

La instancia está publicada en `poke.servegame.com:5432` (port-forward del modem →
`192.168.1.112:5432`) para que apps en la nube (p.ej. Vercel) la usen. Blindaje:

- **TLS obligatorio**: `pg_hba.conf` solo acepta `hostssl` (SSL) en TCP; sin SSL se rechaza.
  El cert es el de Let's Encrypt de `poke.servegame.com` (mismo que la API en 443).
- **Passwords fuertes scram** por rol. El superusuario `luca` dejó su password trivial.
- **Aislamiento por base**: cada proyecto tiene rol NO-superusuario dueño solo de su base,
  y `REVOKE CONNECT ... FROM PUBLIC` en cada DB.
- **Renovación**: el hook `/etc/letsencrypt/renewal-hooks/deploy/restart-postgres.sh` corre
  `refresh-pg-certs.sh` y reinicia el contenedor al renovar el cert (si no, el TLS queda
  con cert viejo en ~60 días).

Strings de conexión:
- **Desde la LAN** (dev/migraciones): `...@192.168.1.112:5432/<db>?sslmode=require`
  (la IP no matchea el cert → `require`, no `verify-full`).
- **Desde internet / Vercel**: `...@poke.servegame.com:5432/<db>?sslmode=verify-full`
  (el hostname matchea el cert → verificación completa).

> Postura honesta: el `5432` queda abierto al mundo aceptando intentos de auth. La defensa
> es TLS + passwords fuertes. Endurecimiento opcional futuro: `userland-proxy=false` +
> allowlist de IPs (Vercel rota IPs, así que requiere su feature de IP fija).

## Backup

```bash
docker exec shared-postgres-postgres-1 pg_dump -U luca luca > backup-luca-$(date +%F).sql
```
