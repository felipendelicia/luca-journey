# Instrucciones del proyecto — Curso de Python con Pokémon

Curso de programación (Linux + Python) para un adolescente principiante, en
español argentino y con temática Pokémon. Incluye un sistema de gamificación
llamado **La Liga Pokémon** (`aventura.py`).

## 🌐 EN MIGRACIÓN: la plataforma web (Astro)

El proyecto se está migrando a una **app web con Astro** en la carpeta **`web/`**, que
va a ser la forma principal de usar el curso (libro, playground, ejercicios en vivo y
Liga web, todo en el navegador).

- **Ya NO se genera PDF.** El manual en PDF fue eliminado; no lo recrees.
- **El contenido teórico vive en `web/src/content/libro/*.md`** (content collections de
  Astro). Esa es la **única fuente** del libro: se edita ahí. Los `curso/semana-*/teoria.md`
  quedaron **obsoletos** (no los mantengas como fuente del libro).
- El sitio estático viejo (`manual/` → `docs/`) queda como legacy hasta que la app de
  Astro lo reemplace en el deploy. No le pongas más esfuerzo salvo necesidad puntual.
- Dev de la web: `cd web && npm run dev` (Astro, con hot-reload). Build: `npm run build`.

> El **curso en sí** (carpetas `curso/semana-*` con `ejercicios.py`, `soluciones.py`,
> `test_*.py`, `interactivo.py`) sigue siendo el código real del curso y la fuente de
> los ejercicios/tests. Eso NO se migra: la web lo consume.

## 🔁 Coherencia general

Cuando cambies contenido del curso, revisá que sigan coherentes:

- `README.md` — presentación y tabla de semanas.
- `ROADMAP.md` — mapa visual y checklist de progreso.
- `liga/datos.py` — registro de semanas y gimnasios de la Liga.
- `manual/manual_contenido.py` → `manual/manual.html` + `manual/manual.pdf` — el libro-manual.

## ✅ Tests

Antes de dar por terminado un cambio, corré `pytest` desde la raíz y dejá todo
en verde. Los tests de cada semana prueban `soluciones.py` por defecto; la Liga
los corre contra `ejercicios.py` con la variable `CURSO_MODULO=ejercicios`.

## 🧱 Convenciones técnicas

- `pytest.ini` usa `--import-mode=importlib` para permitir nombres de archivo
  repetidos entre semanas (`interactivo.py`, `test_ejercicios.py`, etc.).
- Los paquetes (semanas 11-12, proyectos, `liga/`) usan **nombres únicos** para
  no chocar al importar (`agenda`, `agenda_entrenador`, `pokedex_web`,
  `pokedex_app`, `liga`, etc.). Mantené esa unicidad si agregás paquetes.
- Archivos generados (no versionar, ya están en `.gitignore`): `venv/`,
  `__pycache__/`, `progreso.json`, `*.db`. **Excepción:** `manual.pdf` SÍ se versiona.
