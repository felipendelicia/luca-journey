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
  - `src/pages/` — `index`, `libro/[...slug]`, `ejercicios/[slug]/[ex]`, `liga`,
    `playground`, `recursos`.
  - `src/lib/runner.py` — corre **pytest en Pyodide** para corregir ejercicios.
  - `src/lib/url.ts` (`u()`) — prefija los links con el base path de Pages.
  - `scripts/sync-ejercicios.mjs` — divide cada `ejercicios.py` por función/clase, mapea
    los tests por símbolo, y arma `src/data/ejercicios.json` (corre solo en dev/build).
- **`docs/`** — el build publicado en GitHub Pages. **NO se edita a mano**; lo genera el build.
- **`screenshots/`** — capturas usadas en el README.

## Comandos (desde `web/`)

- `npm run dev` — dev server (base `/`, hot-reload), en `http://localhost:4321`.
- `npm run build` — build a `../docs` con base `/luca-journey` (lo que sirve GitHub Pages).

## Reglas

- **Teoría:** editá `web/src/content/libro/*.md`. No dupliques contenido en otro lado.
- **Ejercicios:** editá los `.py` en `web/src/ejercicios/<tema>/`; el build regenera el JSON.
- **Links internos:** usá `u('/ruta')` (de `src/lib/url.ts`), nunca hardcodees `/...`,
  porque en Pages el sitio vive bajo `/luca-journey/`. En scripts de cliente usá `window.__BASE`.
- **Deploy:** `npm run build` actualiza `docs/`; commiteá `docs/` junto con los cambios de `web/`.
- **Correr Python en el navegador** es siempre vía Pyodide (CDN). Los ejercicios usan
  `loadPackage('pytest')`; el código del libro/playground usa CodeMirror + Pyodide.
- Tras tocar la UI, verificá con un screenshot del dev server antes de dar por hecho un cambio.
