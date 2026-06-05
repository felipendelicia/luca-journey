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

## Supabase (login Google + progreso en la nube + intercambios)

El backend es **Supabase** (Postgres + Auth + Realtime). El schema vive en
`supabase/migrations/*.sql` (cada cambio = una migración nueva; no editar las viejas).
La CLI ya está **linkeada** a este proyecto:

- **Project ref:** `cvknrqphepwzpdqdyegv` (org `juxovbtolkdxooccvngp`), nombre `luca-journey`.
- **Config:** `supabase/config.toml` (`project_id = "luca-journey"`); el link cacheado en
  `supabase/.temp/` (no se commitea).
- **Ver estado:** `supabase migration list` (compara local vs remoto; read-only).
- **Aplicar migraciones al remoto:** `supabase db push --yes` (las credenciales están
  cacheadas; no pide password). El `build` **no** corre migraciones — esto es aparte.
- **Cliente:** `src/lib/supa.js` (cliente), `src/lib/nube.js` (sync del progreso),
  `src/lib/social.js` (perfiles/amigos/ofertas), `src/lib/trades.js` (RPCs + Realtime de
  intercambios).
- **Sync = nube pura (login obligatorio):** la **nube es la única fuente de verdad**.
  `Base.astro` muestra un **overlay de arranque** (pantalla de login si no hay sesión;
  loader mientras hidrata). `nube.js` `boot()` baja `progreso` y **pisa** el cache local
  (localStorage = espejo descartable, nunca manda); las escrituras son write-through y los
  cambios externos llegan por realtime. `coleccion.js` y las páginas leen el cache síncrono
  (no se reescribió a async). Diseño: `superpowers/specs/2026-06-04-nube-pura-design.md`.
- Las tablas/RPC se acceden con la **anon key**; el cliente lee `PUBLIC_SUPABASE_URL` y
  `PUBLIC_SUPABASE_ANON_KEY` (env con prefijo `PUBLIC_`, Astro las expone al navegador). Si
  faltan, `supa` queda en `null` y la app corre en modo solo-localStorage. Las mutaciones
  sensibles van por **RPCs `security definer`** (ver `intercambios.sql`), no por escritura directa.

## Reglas

- **Teoría:** editá `web/src/content/libro/*.md`. No dupliques contenido en otro lado.
- **Ejercicios:** editá los `.py` en `web/src/ejercicios/<tema>/`; el build regenera el JSON.
- **Consignas (ejercicios y proyectos): NO incluir pistas que revelen la solución.** Las
  consignas pueden ser explicativas y tener **ejemplos** (entrada → salida esperada), pero
  **nunca** una "Pista:" con el código/solución. El alumno tiene que pensarla.
- **Links internos:** usá `u('/ruta')` (de `src/lib/url.ts`), nunca hardcodees `/...`,
  porque en Pages el sitio vive bajo `/luca-journey/`. En scripts de cliente usá `window.__BASE`.
- **Deploy:** `npm run build` actualiza `docs/`; commiteá `docs/` junto con los cambios de `web/`.
- **Correr Python en el navegador** es siempre vía Pyodide (CDN). Los ejercicios usan
  `loadPackage('pytest')`; el código del libro usa CodeMirror + Pyodide.
- Tras tocar la UI, verificá con un screenshot del dev server antes de dar por hecho un cambio.
