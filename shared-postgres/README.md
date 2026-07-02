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

### En la Pi (producción)

```bash
docker network create shared-db          # una sola vez
cd ~/shared-postgres && docker compose up -d
```

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

## Backup

```bash
docker exec shared-postgres-postgres-1 pg_dump -U luca luca > backup-luca-$(date +%F).sql
```
