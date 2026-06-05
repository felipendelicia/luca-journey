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
- **Correr localmente:**
  ```
  docker compose up -d --build
  ```
  Levanta los servicios `db` (Postgres, puerto host **5433**) y `api` (NestJS). El contenedor
  `api` corre `prisma migrate deploy` al arrancar.
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

## Reglas

- **Teoría:** editá `web/src/content/libro/*.md`. No dupliques contenido en otro lado.
- **Ejercicios:** editá los `.py` en `web/src/ejercicios/<tema>/`; el build regenera el JSON.
- **Consignas (ejercicios y proyectos): NO incluir pistas que revelen la solución.** Las
  consignas pueden ser explicativas y tener **ejemplos** (entrada → salida esperada), pero
  **nunca** una "Pista:" con el código/solución. El alumno tiene que pensarla.
- **Ayuda:** mantené `web/src/pages/ayuda.astro` al día cuando agregues o cambies features
  (desafíos de la comunidad, líderes de gimnasio, intercambios, etc.).
- **Aprovechá las features nuevas:** al autorar/diseñar contenido o proponer ideas, contemplá
  las capacidades de la plataforma (desafíos de comunidad estilo CodeWars, líderes de gimnasio
  = proyectos por pasos, ▶ Ejecutar, logros, ranking) para no quedarnos atrás.
- **Links internos:** usá `u('/ruta')` (de `src/lib/url.ts`), nunca hardcodees `/...`,
  porque en Pages el sitio vive bajo `/luca-journey/`. En scripts de cliente usá `window.__BASE`.
- **Deploy:** `npm run build` actualiza `docs/`; commiteá `docs/` junto con los cambios de `web/`.
- **Correr Python en el navegador** es siempre vía Pyodide (CDN). Los ejercicios usan
  `loadPackage('pytest')`; el código del libro usa CodeMirror + Pyodide.
- Tras tocar la UI, verificá con un screenshot del dev server antes de dar por hecho un cambio.
