# Instrucciones del proyecto — Python con Pokémon (plataforma web)

App web del curso de **Linux + Python** (temática Pokémon, español argentino, para
principiantes absolutos). Todo corre **en el navegador con Pyodide**. El proyecto es
**solo la app Astro en `web/`**: el curso Python viejo, el manual estático y la Liga de
consola fueron migrados a la web y eliminados (quedan en el historial de git).

## Estructura

- **`web/`** — la app Astro (lo único que se mantiene).
  - `src/content/libro/*.md` — la **teoría del libro**. ÚNICA fuente: se edita acá.
    Orden por frontmatter `order`; la agrupación del índice/riel está en `src/lib/grupos.mjs`.
  - `src/ejercicios/<tema>/` — `ejercicios.py`, `soluciones.py`, `test_ejercicios.py`
    (+ helpers) de cada tema. Son la fuente real de los ejercicios.
  - `src/pages/` — `index`, `libro/[...slug]`, `ejercicios/[slug]/[ex]`, `liga`, `safari`,
    `pokedex`, `intercambio`, `amigos`, `u` (perfil público), `recursos`.
  - `src/lib/runner.py` — corre **pytest en Pyodide** para corregir ejercicios.
  - `src/lib/url.ts` (`u()`) — prefija los links con el base path de Pages.
  - `scripts/sync-ejercicios.mjs` — divide cada `ejercicios.py` por función/clase, mapea
    los tests por símbolo, y arma `src/data/ejercicios.json` (corre solo en dev/build).
- **`docs/`** — el build publicado en GitHub Pages. **NO se edita a mano**; lo genera el build.
- **`screenshots/`** — capturas usadas en el README.

## Comandos (desde `web/`)

- `npm run dev` — dev server (base `/`, hot-reload), en `http://localhost:4321`.
- `npm run build` — build a `../docs` con base `/luca-journey` (lo que sirve GitHub Pages).

## API self-hosted (NestJS + Prisma + Docker)

El backend es **NestJS 10 + Prisma v7 + Postgres**, corriendo en Docker. Reemplaza a Supabase
(`supabase/` queda en el repo solo como historial; ya no se usa).

- **Ubicación:** `api/` (NestJS). Módulos: `auth` (Google OAuth → JWT), `progreso`,
  `intercambios`, `social` (perfiles / amigos / ofertas), `desafios`, `realtime` (gateway
  socket.io).
- **Postgres compartido:** el `db` ya **no** vive en este compose. Corre como instancia
  **compartida** en `shared-postgres/` (red Docker externa `shared-db`), reutilizable por
  varios proyectos. La `api` se conecta por el hostname interno `postgres:5432`. Ver
  `shared-postgres/README.md`.
- **Correr localmente:**
  ```
  docker network create shared-db                                   # una vez
  cd shared-postgres && docker compose -f docker-compose.yml -f docker-compose.dev.yml up -d
  cd .. && docker compose up -d --build
  ```
  Primero levanta `shared-postgres` (Postgres, expone **5433** solo en dev vía su override),
  después la `api` (NestJS), que corre `prisma migrate deploy` al arrancar.
- **Env del servidor** (`api/.env`): `DATABASE_URL`, `JWT_SECRET`, `GOOGLE_CLIENT_ID`,
  `GOOGLE_CLIENT_SECRET`, `GOOGLE_CALLBACK_URL`, `FRONTEND_URL`, `CORS_ORIGINS`.
  La API necesita `GOOGLE_*` no vacíos para arrancar.
- **Migraciones:** Prisma en `api/prisma/` (`prisma migrate dev` en local; `migrate deploy`
  en el contenedor). Ya **no** se usa `supabase/migrations/`.
- **Data migration:** `api/prisma/seed-import.ts` importa un CSV dump del proyecto Supabase
  original (preserva UUIDs). El dueño corre el export con su connection string de Supabase.
- **Cliente web:** `src/lib/api.js` (fetch + JWT, auth Google) y `src/lib/realtime.js`
  (socket.io). `src/lib/supa.js` es un shim de compatibilidad que re-exporta `haySupabase`
  (= `hayApi`); `supa` queda `null`.
- **Env del frontend** (`web/.env`): `PUBLIC_API_URL` (reemplaza `PUBLIC_SUPABASE_*`).
  Sin esta variable la web corre en modo solo-localStorage.
- **Deploy:** el build de producción (`npm run build` desde `web/`) debe correrse con el
  valor real de `PUBLIC_API_URL`. El CORS de la API debe permitir el origen de GitHub Pages.

### Servidor (Raspberry Pi)

El proyecto corre en una **Raspberry Pi** en la LAN, vía **SSH**:

- **Host:** `192.168.1.112` · **Usuario:** `felipe` · **Acceso:** `ssh felipe@192.168.1.112`
- La contraseña SSH **no se versiona** (vive en la memoria local de Claude, fuera del repo).
- La Pi es **ARM64 (aarch64)**, Debian 13, **~900 MB RAM**. Docker + compose ya instalados.
- Deploy en `~/luca-journey/` en la Pi: `docker-compose.yml` + `api/` (fuente) + `.env`
  (con `JWT_SECRET`, `GOOGLE_*`, `FRONTEND_URL`, `CORS_ORIGINS`; **no versionado**).

#### Deploy: buildear local + transferir la imagen (NO buildear en la Pi)

Los ~900 MB de RAM de la Pi no alcanzan para `npm ci` + `tsc` sin riesgo de OOM. Por eso la
imagen se **buildea en otra máquina** (cross-build arm64) y se **transfiere** ya armada. El
`api` del `docker-compose.yml` tiene `image: luca-journey-api:latest` además de `build:`, así
en la Pi `docker compose up` usa la imagen cargada **sin** rebuildear.

```bash
# 1) (una vez) habilitar emulación arm64 en la máquina de build
docker run --privileged --rm tonistiigi/binfmt --install arm64
# 2) cross-build de la imagen arm64
docker buildx build --platform linux/arm64 -t luca-journey-api:latest --load ./api
# 3) transferir la imagen a la Pi
docker save luca-journey-api:latest | gzip -1 | ssh felipe@192.168.1.112 'gunzip | docker load'
# 4) sincronizar compose + fuente (liviano; el build real no se corre en la Pi)
rsync -az --exclude node_modules --exclude dist --exclude .env --exclude '*.tsbuildinfo' \
  docker-compose.yml api felipe@192.168.1.112:luca-journey/
rsync -az shared-postgres felipe@192.168.1.112:                       # compose del Postgres compartido
# 5) levantar en la Pi: PRIMERO el Postgres compartido, después la api
ssh felipe@192.168.1.112 'docker network create shared-db 2>/dev/null; \
  cd ~/shared-postgres && docker compose up -d && \
  cd ~/luca-journey && docker compose up -d'
```

Verificación: `curl http://192.168.1.112:3000/auth/me` → `401`. La API necesita `GOOGLE_*`
no vacíos para arrancar (con placeholders arranca, pero el login Google no funciona hasta
poner credenciales reales). La Pi está en LAN: para que el frontend de GitHub Pages la
alcance hace falta exponerla (túnel/port-forward/dominio) y ajustar `GOOGLE_CALLBACK_URL`,
`FRONTEND_URL` y `CORS_ORIGINS`.

## Reglas

- **Teoría:** editá `web/src/content/libro/*.md`. No dupliques contenido en otro lado.
- **Ejercicios:** editá los `.py` en `web/src/ejercicios/<tema>/`; el build regenera el JSON.
- **Consignas (ejercicios y proyectos): NO incluir pistas que revelen la solución.** Las
  consignas pueden ser explicativas y tener **ejemplos** (entrada → salida esperada), pero
  **nunca** una "Pista:" con el código/solución. El alumno tiene que pensarla.
- **Ayuda:** mantené `web/src/pages/ayuda.astro` al día cuando agregues o cambies features
  (desafíos de la comunidad, líderes de gimnasio, intercambios, etc.).
- **Landing pública:** mantené `web/src/pages/conocer.astro` (la landing en `/conocer`, sin login) al día
  cuando agregues/cambies features importantes: la grilla de features, los stats (Pokémon, regiones,
  ejercicios), las "capturas" y el texto. Es la puerta de entrada para gente nueva — tiene que reflejar
  lo que el proyecto ofrece HOY.
- **Aprovechá las features nuevas:** al autorar/diseñar contenido o proponer ideas, contemplá
  las capacidades de la plataforma (desafíos de comunidad estilo CodeWars, líderes de gimnasio
  = proyectos por pasos, ▶ Ejecutar, logros, ranking) para no quedarnos atrás.
- **Links internos:** usá `u('/ruta')` (de `src/lib/url.ts`), nunca hardcodees `/...`,
  porque en Pages el sitio vive bajo `/luca-journey/`. En scripts de cliente usá `window.__BASE`.
- **Deploy:** `npm run build` actualiza `docs/`; commiteá `docs/` junto con los cambios de `web/`.
- **Correr Python en el navegador** es siempre vía Pyodide (CDN). Los ejercicios usan
  `loadPackage('pytest')`; el código del libro usa CodeMirror + Pyodide.
- Tras tocar la UI, verificá con un screenshot del dev server antes de dar por hecho un cambio.
- **Frontend / diseño visual:** todo lo que requiera trabajo de UI o diseño visual (páginas,
  componentes, modales, layouts, estilos) se hace con el skill **`/frontend-design`**. Apuntá a
  interfaces distintivas y pulidas, cohesivas con la estética retro-Pokédex/CRT del proyecto
  (no genéricas), y tema-aware (modo oscuro y claro).
- **Sprites, NO emojis para items característicos de Pokémon:** los items propios del universo
  Pokémon (pociones, antídoto/antiquemar/etc., revivir, piedras evolutivas, pokeballs, medallas…)
  se dibujan como **sprites SVG** en `src/lib/sprites.js` (`itemSvg`/`ballSvg`/`badgeSvg`), nunca
  con emoji. El emoji queda solo para acentos de UI genéricos (🍬 caramelos, 🔴 contador, etc.).
  Los sprites deben ser **MUY fieles a la saga y congruentes entre sí**: cada familia comparte
  silueta y estilo (p.ej. la línea de Pociones = misma botella spray, color-coded; las curas de
  estado = misma botella/vial, color por estado), con el mismo grosor de contorno, brillo y
  acabado. Verificá el set junto (screenshot) para que se vea coherente.
