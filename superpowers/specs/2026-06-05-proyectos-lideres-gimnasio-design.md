# Diseño — Proyectos / Líderes de Gimnasio

Fecha: 2026-06-05
Estado: aprobado

> Ubicación `superpowers/` (raíz), NO `docs/`.

## Objetivo
Mini-proyectos guiados (Approach A: pasos auto-corregidos + capstone) que funcionan como
**líderes de gimnasio**: uno por tema/medalla (48) + un **integrador** por región (6). Se
encaran tras los ejercicios del tema; vencerlos es **obligatorio** para la medalla (tema) y
para ser Campeón (integrador de la región). Construimos el **motor + 1 piloto**; los 54
proyectos se autoran después.

## Modelo del proyecto
Un proyecto = secuencia de **pasos**. Cada paso es como un mini-ejercicio: `consigna`,
`starter`, `tests` (pytest). El código del alumno **se acumula** en un solo programa: el
módulo para corregir el paso N = `preamble` + el código escrito por el alumno en los pasos
1..N. El último paso (**capstone**) corre el programa entero. Pasos **secuenciales**: hay
que aprobar el paso N para desbloquear el N+1. Aprobar todos = **líder vencido**.

## Contenido (file-based, espeja ejercicios)
`web/src/proyectos/<slug>/`:
- `proyecto.py` — solución de referencia, una función por paso (como `ejercicios.py`).
- `test_proyecto.py` — tests por paso (como `test_ejercicios.py`).
- `meta.json` — `{ tipo:'lider'|'integrador', tema, region, titulo, lider, premio:<pokeId>,
  intro, preamble, packages, pasos:[{id, titulo, consigna, starter}] }`.

Script `web/scripts/sync-proyectos.mjs` (corre en dev/build, como `sync-ejercicios.mjs`):
arma `web/src/data/proyectos.json` con cada proyecto `{ slug, tipo, tema, region, titulo,
lider, premio, intro, preamble, packages, pasos:[{id, titulo, consigna, starter, tests}] }`.
La **solución NO se emite** (anti-trampa). Engancharlo al `prebuild`/`dev` igual que el de
ejercicios (revisar `web/package.json`).

## Páginas / UI
- **Índice `/ejercicios`** (`web/src/pages/ejercicios/index.astro`): después de los
  ejercicios de cada tema, una **card dorada "🏟️ Líder de Gimnasio: <lider>"**, **bloqueada
  🔒** hasta completar los ejercicios del tema (todas las `ej:<slug>:<id>:ok`). Al final de
  cada región, una **card "👑 Integrador"**, bloqueada hasta vencer a los líderes de la región.
- **`/proyectos/<slug>`** — NO se puede prerenderizar por id desconocido, pero los slugs SÍ
  se conocen en build (vienen de `proyectos.json`) → usar `getStaticPaths` (como
  `ejercicios/[slug]`). Muestra: intro, pasos secuenciales (cada uno con editor + "Corregir
  paso", reusa `editor.js` + el patrón Pyodide/pytest de `ejercicios/[slug]/[ex].astro`),
  y al vencer al líder, animación + premio.

## Corrección
Reusa `web/src/lib/runner.py` (`correr(slug, ejercicios_code, test_code, extra, solo)`).
Por paso N: `ejercicios_code` = `preamble + "\n\n" + (código guardado de pasos 1..N)`;
`test_code` = el test del paso N; corre pytest. El código por paso se guarda en
`proy:<slug>:<pasoId>` (localStorage); `proy:<slug>:<pasoId>:ok = '1'` al aprobarlo.

## Progreso + sync
- Nuevas claves localStorage con prefijo **`proy:`** → agregar `'proy:'` a `PREFIJOS` en
  `web/src/lib/nube.js` (para que sincronice a la nube como `ej:`/`col:`).
- `proy:<slug>:ok = '1'` cuando se vencen TODOS los pasos del proyecto.

## Recompensa + gating (obligatorio, con grandfather)
- **Líder de tema vencido** (`proy:<temaSlug>:ok`): otorga la **medalla** del tema + el
  Pokémon insignia.
- **Integrador vencido** (`proy:<region>-integrador:ok`): **Campeón de la región** + el
  legendario.
- **Cambios en la progresión** (en `coleccion.js` `sincronizar` y `liga.astro`):
  - "tema completo" (para medalla/insignia) pasa a requerir: ejercicios del tema hechos **Y**
    `proy:<slug>:ok`. **Grandfather:** si la medalla ya estaba ganada (`col:hitos` tiene
    `tema:<slug>`), se conserva aunque no haya proyecto.
  - "región completa" (legendario/Campeón) pasa a requerir: todos los temas completos **Y**
    todos los líderes **Y** `proy:<region>-integrador:ok`. Grandfather análogo con
    `region:<region>` en `col:hitos`.

## Piloto
`web/src/proyectos/python-introduccion/` — **"Líder Brock: Pokédex de consola"** (tipo
`lider`, tema `python-introduccion`, region `kanto`, premio = insignia de Kanto). ~4 pasos:
1) `buscar(nombre)` devuelve un dict de datos; 2) `mostrar(poke)` lo imprime lindo;
3) `menu(pokedex)` loop de consola; 4) capstone: arma y corre el programa.

## Bordes
- El sitio es estático: `/proyectos/[slug]` usa `getStaticPaths` con los slugs de
  `proyectos.json` (no `?query`, porque los slugs se conocen en build — distinto de
  `/desafios` que son dinámicos de la DB).
- Sin DB nueva: todo es contenido file-based + progreso en `progreso` (vía `proy:` en la nube).
- Pyodide sin timeout real (loops congelan la pestaña) — igual que ejercicios; aceptado.

## Verificación
`npm run build` (corre `sync-proyectos.mjs`) + prueba manual: completar los ejercicios de
python-introducción → se desbloquea el líder → resolver los 4 pasos → ganar la medalla.

## Fases (para el plan)
1. **Motor + piloto**: `sync-proyectos.mjs` + `proyectos.json`, `src/proyectos/python-introduccion/`,
   página `/proyectos/[slug]`, card en `/ejercicios`, `proy:` en la sync, gating+grandfather
   en `coleccion.js`/`liga.astro`.
2. **Contenido**: los otros 47 líderes + 6 integradores (incremental, fuera de este ciclo).
